# Newfon

* Authors: Sergey Shishmintsev, Alexy Sadovoi, Sergey A.K.A. Electrik, Kvark and other developers
* Download [stable version][1]
* NVDA Compatibility: 2019.2 to 2025.1

### About

Newfon is a speech synthesizer that supports Russian and Ukrainian for the first time since its release. Later Croatian, Polish and Serbian were added.

### General features:

* Ability to change languages;
* Changing the sampling rate;
* Sound interpolation to simulate the sound of old DOS screen readers and book readers;
* In order for the synthesizer to read the text as it is written, it is possible to disable the built-in accent dictionary. Option works only for Russian language;
* The synthesizer, in addition to the main rate from 0 to 100%, supports additional speech acceleration, which reduces the time of reading the text;
* To get a smoother reading at high speeds, it is possible to adjust the pauses between phrases.

### Note:

Numerous versions of Newfon have been released since it was first published on the NVDA official add-ons site, but unfortunately the lead developer Sergey Shishmintsev died, which delayed the update of the synthesizer on the site.

In 2017, the current developers of the Newfon speech synthesizer had the opportunity to get the source codes for Sergey's developments. His relatives, thanks to whom this happened, set them only one condition: if the development of his projects continues, they must become free.

The developers, in turn, decided that history should not forget Sergey Shishmintsev, as he was a unique programmer with an enormous amount of perseverance, hard work and knowledge.

## Changelog

###Version 2025.2

Updated compatibility with NVDA 2025.1, which is currently in beta testing. The add-on will be updated when NVDA 2025.1 becomes stable.

### Version 2025.1

* Added compatibility for NVDA 2025 (Co-authored-by Beqa Gozalishvili [beqabeqa473][4])
* Some unnecesary ordered dict removals and code simplifications (Co-authored-by Beqa Gozalishvili [beqabeqa473][4])

### Version 2023.4

* Removed a dictionary of accents containing many errors. Replaced by lexicon.test from rulex [commit67479e8][2] (Co-authored-by Sergey [Electrik-spb][3])
* Fixed dash handling (Co-authored-by Sergey [Electrik-spb][3])
* Reformat code (Co-authored-by Beqa Gozalishvili [beqabeqa473][4])
* Drop python2 support (Co-authored-by Beqa Gozalishvili [beqabeqa473][4])

### Version 2023.3

The GPL license is back in place of MIT. Now MIT is used for open source scripts and GPL is used for Newfon speech driver.

### Version 2023.2

Newfon license changed from GPL to MIT license.

### Version 2023.1

* Added compatibility with NVDA 2023.1 (backwards compatibility with NVDA 2019 is still supported);
* Added Newfon license agreement in English;
* Added documentation in Russian.

### Version 2022.04.16

Compatible with NVDA 2022 (backward compatibility with NVDA 2019.2 is still supported.).

### Version 2021.06.06

For compatibility with later versions of NVDA, the lastTestedNVDAVersion value has been changed.

### Version 2021.03.19

For compatibility with subsequent versions of NVDA, the internal mechanisms for the interaction of the synthesizer with NVDA drivers have been changed.

### Version 2021.01.16
#### Added:

speech.BreakCommand - This feature is required by some add-ons to pause speech for a while.

#### Fixed:

In Ukrainian, some capital letters were not read correctly.

### Version 2020.12.28

In this version, a significant processing of scripts, restructuring of the add-on, new languages (test opportunity) and much more was made.

#### Added:

* New languages: Croatian, Polish, Serbian. These scripts were taken from open sources and provided by beta testers. The author cannot be responsible for the operation of these scripts, so you use them as is - without any guarantees;
* Some old Russian characters have been added to the Russian language: "і": "и десятеричное", "ѣ": "ять", "ѳ": "фита", "ѵ": "ижица", "ў": "у краткое", "ґ": "гэ взрывное". Accordingly, if you read the old Russian word, it will be read correctly;
* Sound interpolation. Now you can imitate the sound of a newfon, just like in the old DOS screen readers and book readers. To implement this feature, the libsamplerate library is used;
* Now you can turn off reading decimal fractions (only for Russian and Ukrainian), which improves the reading of program versions.

#### Changed:

* The add-on has been completely reworked. now all the code is not in one __init__.py file, which makes maintaining the code and adding new languages much easier;
* Queues from DLLs have been ported to Python, which has a good effect on the stability of the add-on.

#### Fixed:

Sound out of sync bug that occasionally appeared on the latest versions of NVDA.

### Version 2020.09.12
#### Changed:

Due to a change in the way the audio subsystem works In new alpha versions of NVDA, the sample rate was not switched properly.

### Version 2020.03.12
#### Added:

* At the request of users, an optional ability has been added for English pronunciation, instead of the sound е, pronounce the sound э - like in the old add-ons;
* Now the add-on has localization, accordingly, on the Ukrainian NVDA interface, all additional parameters will be displayed in the corresponding language.

#### Changed

* Thanks to the programmer Kvark, the internal architecture of the add-on was rewritten to the third Python;
* For fans of non-standard voices, the list of sampling frequencies has been expanded.

[1]: https://www.nvaccess.org/addonStore/legacy?file=newfon

[2]: https://github.com/poretsky/rulex/commit/67479e859cd5955072dc5bbae8065c4417af52cc

[3]: https://github.com/Electrik-spb

[4]: https://github.com/beqabeqa473
