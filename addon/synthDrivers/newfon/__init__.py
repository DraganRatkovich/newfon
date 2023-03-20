# -*- coding: utf-8 -*-
# Copyright (C) 2019/2022 Sergey Shishmintsev, Alexy Sadovoi, Sergey A.K.A. Electrik, Kvark and other developers
# This file is covered by the GNU General Public License.

import os.path
import queue
from collections import OrderedDict
from ctypes import *
import threading
from synthDriverHandler import SynthDriver, VoiceInfo, LanguageInfo, getSynth
try:
    from autoSettingsUtils.driverSetting import DriverSetting, BooleanDriverSetting, NumericDriverSetting
    from autoSettingsUtils.utils import StringParameterInfo
except ImportError:
    from driverHandler import DriverSetting, StringParameterInfo, BooleanDriverSetting, NumericDriverSetting
import config
import addonHandler
from synthDriverHandler import synthIndexReached, synthDoneSpeaking

from .languages import en, hr, ru, pl, sr, uk
import nvwave
try:
    from speech.commands import (IndexCommand, PitchCommand, BreakCommand, SpeechCommand)
except ImportError:  # for NVDA below 2021.1
    from speech import (IndexCommand, PitchCommand, BreakCommand, SpeechCommand)

import winKernel
from logHandler import log
addonHandler.initTranslation()


file_path = os.path.dirname(__file__)


newfon_audio_callback = WINFUNCTYPE(c_int, POINTER(c_char), POINTER(c_char), c_int)
newfon_index_callback = WINFUNCTYPE(None, c_int)
newfon_doneSpeaking_callback = WINFUNCTYPE(None)\

def freeLibrary(handle):
    if winKernel.kernel32.FreeLibrary(handle) == 0:
        raise WindowsError()
    return True

lngModule = None

def setLngModule(language):
    global lngModule
    if language in globals():
        lngModule = globals()[language]
    else:
        lngModule = ru

def setLngOption(option, value):
    global lngModule
    lngModule.options = {option: value}


class NewfonObject:
    def __init__(self, newfon_lib, player, pitch, inflection, voice):
        self.__newfon_lib = newfon_lib
        self.__player = player
        self.__pitch_min = 0
        self.__pitch_max = 1
        self.__nvda_pitch = pitch
        self.__inflection = inflection
        self.__pitchTable = [(90, 130), (190, 330), (60, 120), (220, 340)]
        self.__pitch_index = 0
        self.__voice = voice
        self.__index = None
        self.__pause = None
        self.__text = None
        self.__lock = threading.Lock()
        min, max = self.calculateMinMaxPitch(self.__nvda_pitch, self.__inflection)
        self.__pitch = [[min, max], [min, max]]

    def calculateMinMaxPitch(self, pitch, inflection):
        min, max = self.__pitchTable[int(self.__voice)]
        i = max-min
        i = int((i/50.0)*((inflection-50)/2))
        min -= i
        max += i
        i = int((pitch-50)/1.3)
        min += i
        max += i
        return min, max

    @property
    def text(self):
        with self.__lock:
            return self.__text

    @text.setter
    def text(self, value):
        with self.__lock:
            self.__text = value

    @property
    def index(self):
        with self.__lock:
            return self.__index

    @index.setter
    def index(self, value):
        with self.__lock:
            self.__index = value

    @property
    def pause(self):
        with self.__lock:
            return self.__pause

    @pause.setter
    def pause(self, value):
        with self.__lock:
            self.__pause = value

    def pitch(self, nvda_pitch):
        min, max = self.calculateMinMaxPitch(nvda_pitch, self.__inflection)
        self.__pitch_index ^= 1
        self.__pitch[self.__pitch_index][self.__pitch_min] = min
        self.__pitch[self.__pitch_index][self.__pitch_max] = max

    def __call__(self):
        text = self.text.encode("cp1251", errors="replace")
        self.__newfon_lib.set_pitch_min(self.__pitch[self.__pitch_index ^ 1][self.__pitch_min])
        self.__newfon_lib.set_pitch_max(self.__pitch[self.__pitch_index ^ 1][self.__pitch_max])
        self.__newfon_lib.set_pause(self.pause)
        self.__newfon_lib.speakText(text, self.index)
        self.__newfon_lib.set_pitch_min(self.__pitch[self.__pitch_index ^ 1][self.__pitch_min])
        self.__newfon_lib.set_pitch_max(self.__pitch[self.__pitch_index ^ 1][self.__pitch_max])
        self.__player.idle()


class AudioCallback:
    def __init__(self, is_silence):
        self.__is_silence = is_silence
        self.__player = None

    def set_player(self, player):
        self.__player = player

    def __call__(self, udata, buffer, length):
        if self.__is_silence.is_set():
            return 1
        self.__player.feed(string_at(buffer, length))
        return 0


class IndexCallback:
    def __init__(self, newfon_driver):
        self.__newfon_driver = newfon_driver

    def __call__(self, index):
        synth = getSynth()
        if index == -1:
            synthDoneSpeaking.notify(synth=self.__newfon_driver)
        else:
            synthIndexReached.notify(synth=self.__newfon_driver, index=index)


class DoneSpeakingCallback:
    def __init__(self, newfon_driver, player):
        self.__newfon_driver = newfon_driver
        self.__player = player

    def __call__(self):
        pass


class NewfonThread(threading.Thread):
    def __init__(self, newfon_lib, player, is_silence, newfon_queue, newfon_driver):
        self.__newfon_lib = newfon_lib
        self.__player = player
        self.__is_silence = is_silence
        self.__queue = newfon_queue
        threading.Thread.__init__(self)
        self.__newfon_driver = newfon_driver
        self.daemon = True

    def run(self):
        while True:
            newfon = self.__queue.get()
            if newfon is None:
                break
            elif newfon == ():
                self.__is_silence.clear()
            elif self.__is_silence.is_set():
                pass
            else:
                newfon()


class SynthDriver(SynthDriver):
    name = "newfon"
    description = "Newfon"

    supportedSettings = (
        SynthDriver.VoiceSetting(),
        SynthDriver.LanguageSetting(),
        SynthDriver.RateSetting(),
        DriverSetting("accel", _("&Acceleration"), True),
        DriverSetting("samplesPerSec", _("&Samples per second (hz)"), True),
        DriverSetting("interpolation", _("&Interpolation"), True),
        SynthDriver.PitchSetting(),
        SynthDriver.InflectionSetting(10),
        SynthDriver.VolumeSetting(),
        NumericDriverSetting("pauseBetweenPhrases", _("&Pause between phrases"), True),
        BooleanDriverSetting("useSynthDict", _("Use built-in &dictionary synthesizer (only for Russian language)"), True, defaultVal=True),
        BooleanDriverSetting("decimalFractions", _("Read decimal Fractions (only for Russian and ukrainian languages)"), True, defaultVal=True),
        BooleanDriverSetting("pseudoEnglishPronunciation", _("Include pseudo &english pronunciation"), True, defaultVal=True),
    )

    supportedCommands = {IndexCommand, PitchCommand, BreakCommand}
    supportedNotifications = {synthIndexReached, synthDoneSpeaking}

    @classmethod
    def check(cls):
        return True

    def __init__(self):
        self._volume = 100
        self._language = "ru"
        setLngModule(self._language)
        self._pitch = 50
        self._accel = "0"
        self._pauseBetweenPhrases = 50
        self._samplesPerSec = "10000"
        self._interpolation = "1"
        self._useSynthDict = True
        self._decimalFractions = True
        self._pseudoEnglishPronunciation = True
        self._inflection = 50
        self.pitchTable = [(90, 130), (190, 330), (60, 120), (220, 340)]
        self.lastIndex = None
        self.__samplerate_lib = WinDLL(os.path.join(file_path, "bin", "libsamplerate.dll"))
        self.__dictdb_lib = WinDLL(os.path.join(file_path, "bin", "dictdb.dll"))
        self.__dict_lib = WinDLL(os.path.join(file_path, "bin", "ndict.dll"))
        self.__newfon_lib = WinDLL(os.path.join(file_path, "bin", "newfon_nvda.dll"))
        if not self.__newfon_lib.initialize():
            raise RuntimeError("Newfon: initialization error")
        self.__is_silence = threading.Event()
        self.__audio_callback = AudioCallback(self.__is_silence)
        self.__newfon_audio_callback = newfon_audio_callback(self.__audio_callback)
        self.__index_callback = IndexCallback(self)
        self.__newfon_index_callback = newfon_index_callback(self.__index_callback)
        self.__player = nvwave.WavePlayer(channels=1, samplesPerSec=(int(self._samplesPerSec) * int(self._interpolation)), bitsPerSample=16, outputDevice=config.conf["speech"]["outputDevice"])
        self.__audio_callback.set_player(self.__player)
        self.__doneSpeaking_callback = DoneSpeakingCallback(self, self.__player)
        self.__newfon_doneSpeaking_callback = newfon_doneSpeaking_callback(self.__doneSpeaking_callback)
        self.__newfon_lib.set_callbacks(self.__newfon_audio_callback, self.__newfon_index_callback, self.__newfon_doneSpeaking_callback)
        self.__newfon_queue = queue.Queue()
        self.__newfon_thread = NewfonThread(self.__newfon_lib, self.__player, self.__is_silence, self.__newfon_queue, self)
        self.__newfon_thread.start()
        self.__newfon_lib.set_dictionary(True)

    def terminate(self):
        self.cancel()
        self.__newfon_queue.put(None)
        self.__newfon_thread.join()
        self.__player.close()
        self.__player = None
        self.__newfon_lib.terminate()
        try:
            freeLibrary(self.__newfon_lib._handle)
            freeLibrary(self.__dict_lib._handle)
            freeLibrary(self.__dictdb_lib._handle)
            freeLibrary(self.__samplerate_lib._handle)
        except WindowsError:
            log.exception("Can not unload dll")
        finally:
            del self.__newfon_lib
            del self.__dict_lib
            del self.__dictdb_lib
            del self.__samplerate_lib

    def speak(self, speechSequence):
        textList = []
        newfon = NewfonObject(self.__newfon_lib, self.__player, self._pitch, self._inflection, self.voice)
        for item in speechSequence:
            if isinstance(item, str):
                textList.append(lngModule.process(item, self._language))
            elif isinstance(item, IndexCommand):
                self.__newfon_lib.set_mark(item.index)
            elif isinstance(item, PitchCommand):
                newfon.pitch(self._pitch + item.offset)
            elif isinstance(item, BreakCommand):
                newfon.pause = item.time
                self._speak(newfon, textList)
                textList = []
            elif isinstance(item, SpeechCommand):
                log.debugWarning("Unsupported speech command: %s" % item)
            else:
                log.error("Unknown speech: %s" % item)
        newfon.pause = self._pauseBetweenPhrases
        self._speak(newfon, textList)

    def _speak(self, newfon, textList, index=-1):
        newfon.index = index
        newfon.text = ""
        newfon.text = "".join(textList)
        self.__newfon_queue.put(newfon)

    def cancel(self):
        try:
            while True:
                self.__newfon_queue.get_nowait()
        except queue.Empty:
            self.__is_silence.set()
            self.__newfon_queue.put(())
            self.__player.stop()

    def _set_voice(self, value):
        self.__newfon_lib.set_voice(int(value))
        self._set_pitch(self._pitch)

    def _get_voice(self):
        return str(self.__newfon_lib.get_voice())

    def _get_availableVoices(self):
        voices = [_("male 1"), _("female 1"), _("male 2"), _("female 2")]
        return OrderedDict((str(index), VoiceInfo(str(index), name)) for index, name in enumerate(voices))

    def _set_volume(self, value):
        self._volume = value
        self.__newfon_lib.set_volume(value)

    def _get_volume(self):
        return self._volume

    def _set_rate(self, value):
        self.__newfon_lib.set_rate(value)

    def _get_rate(self):
        return self.__newfon_lib.get_rate()

    def _set_pitch(self, value):
        self._pitch = value

    def _get_pitch(self):
        return self._pitch

    def pause(self, switch):
        self.__player.pause(switch)

    def _set_language(self, language):
        self._language = language
        self.useSynthDict = self._useSynthDict
        setLngModule(language)

    def _get_language(self):
        return self._language

    def _get_availableLanguages(self):
        return OrderedDict((
            ("hr", LanguageInfo("hr")),
            ("pl", LanguageInfo("pl")),
            ("ru", LanguageInfo("ru")),
            ("sr", LanguageInfo("sr")),
            ("uk", LanguageInfo("uk")),
        ))

    def _set_inflection(self, inflection):
        self._inflection = inflection
        self._set_pitch(self._pitch)

    def _get_inflection(self):
        return self._inflection

    def _set_accel(self, value):
        self._accel = value
        self.__newfon_lib.set_accel(int(value))

    def _get_accel(self):
        return self._accel

    def _get_availableAccels(self):
        return OrderedDict((str(x), StringParameterInfo(str(x), str(x))) for x in range(8))

    def _set_interpolation(self, value):
        self._interpolation = value
        self.cancel()
        self.__newfon_queue.put(())
        self.__player.close()
        self.__player = nvwave.WavePlayer(channels=1, samplesPerSec=(int(self._samplesPerSec) * int(self._interpolation)), bitsPerSample=16, outputDevice=config.conf["speech"]["outputDevice"])
        self.__audio_callback.set_player(self.__player)
        self.__newfon_lib.set_interpolation(int(self._interpolation))

    def _get_interpolation(self):
        if self.__player is not None:
            return self._interpolation
        return "1"

    def _get_availableInterpolations(self):
        interpolations = OrderedDict()
        interpolations["1"] = StringParameterInfo("1", _("Off"))
        interpolations["2"] = StringParameterInfo("2", _("2 X"))
        interpolations["4"] = StringParameterInfo("4", _("4 X"))
        return interpolations

    def _set_samplesPerSec(self, value):
        self._samplesPerSec = value
        self.cancel()
        self.__newfon_queue.put(())
        self.__player.close()
        self.__player = nvwave.WavePlayer(channels=1, samplesPerSec=int(self._samplesPerSec)*int(self._interpolation), bitsPerSample=16, outputDevice=config.conf["speech"]["outputDevice"])
        self.__audio_callback.set_player(self.__player)

    def _get_samplesPerSec(self):
        if self.__player is not None:
            return self._samplesPerSec
        return "10000"

    def _get_availableSamplespersecs(self):
        sampleRates = OrderedDict()
        for s in ("8000", "9025", "10000", "11025", "12000", "13025", "14000", "15025", "16000"):
            sampleRates[s] = StringParameterInfo(s, s)
        return sampleRates

    def _set_pauseBetweenPhrases(self, value):
        self._pauseBetweenPhrases = value
        self.__newfon_lib.set_pause(self._pauseBetweenPhrases)

    def _get_pauseBetweenPhrases(self):
        return self._pauseBetweenPhrases

    def _set_useSynthDict(self, value):
        self._useSynthDict = value
        if self.language == "ru":
            self.__newfon_lib.set_dictionary(value)
        else:
            self.__newfon_lib.set_dictionary(False)

    def _get_useSynthDict(self):
        return self._useSynthDict

    def _set_decimalFractions(self, value):
        self._decimalFractions = value
        if self._decimalFractions == True:
            self.__newfon_lib.enable_decimal_fractions(True)
        else:
            self.__newfon_lib.enable_decimal_fractions(False)

    def _get_decimalFractions(self):
        return self._decimalFractions

    def _set_pseudoEnglishPronunciation(self, value):
        self._pseudoEnglishPronunciation = value
        en.options["pseudoEnglishPronunciation"] = value

    def _get_pseudoEnglishPronunciation(self):
        return self._pseudoEnglishPronunciation
