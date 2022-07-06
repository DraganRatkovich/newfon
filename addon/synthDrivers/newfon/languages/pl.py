# -*- coding: utf-8 -*-
# A part from newfon speech synthesizer
# Copyright (C) 2019/2022 Sergey Shishmintsev, Alexy Sadovoi, Sergey A.K.A. Electrik, Kvark and other developers

import re
try:
	from . import ru,pl_numbers
except ImportError: # for NVDA below 2019.3
	import ru,pl_numbers

letters = {
'a': u"а",
'b' : u"бэ",
'c': u"цэ",
'd': u"дэ",
'e': u"э",
'f': u"эф",
'g': u"ге",
'h': u"ха",
'i': u"и",
'j': u"йот",
'k': u"ка",
'l': u"эль",
'm': u"эм",
'n': u"эн",
'o': u"о",
'p': u"пэ",
'q': u"ку",
'r': u"эр",
's': u"эс",
't': u"тэ",
'u': u"у",
'v': u"фау",
'w': u"ву",
'x': u"икс",
'y': u"игрэк",
'z': u"зэт",
u"ą": u"а носовэ",
u"ę": u"э носовэ",
u"ć": u"тьсе",
u"ł": u"эл",
u"ż": u"жет",
u"ź": u"зет",
u"ó": u"у крэска",
u"ń": u"энь",
u"ś": u"эсь",
}

exceptions = {
re.compile(u"(supe|hipe|cybe)r(z)", re.U|re.I): u"\\1р\\2",
re.compile(u"(ma)r(zn)", re.U|re.I): u"\\1р\\2",
re.compile(u"(ta)r(zan)", re.U|re.I): u"\\1р\\2",
re.compile(u"(e)r(zac)", re.U|re.I): u"\\1р\\2",
re.compile(u"(\\bspe)c(z)", re.U|re.I): u"\\1ц\\2",
}

pronunciation= {
'e': u"э",
u'ń': u"нь",
'x': u"кс",
'y': u"ы",
u"ś": u"сь",
u"ć": u"тьсь",
u"ł": u"л",
u"l": u"ль",
u"dź": u"дьзь",
u"ż": u"ж",
u"ź": u"зь",
u"ó": u"у",
"ch": u"х",
"cz": u"тш",
"rz": u"ж",
"sz": u"ш",
"qu": u"кв",
"v": u"ф",
}

rules = {
re.compile(u"r(zi)", re.U|re.I): u"р\\1",
re.compile(u"([td])([rs]z)", re.U|re.I): u"\\1\\1\\2",
re.compile(u"([ptkfschść]|[cs]z)rz", re.U|re.I): u"\\1ш",
re.compile(u"l(i)", re.U|re.I): u"л\\1",
re.compile(u"([pbfvwszcmn])i([aeouąęó])", re.U|re.I): u"\\1ь\\2",
re.compile(u"([kgh])i(e)", re.U|re.I): u"\\1ь\\2",
re.compile(u"c([iь])", re.U|re.I): u"тьс\\1",
re.compile(u"dz([iь])", re.U|re.I): u"дьз\\1",
re.compile(u"ą([pbfvwm]|\\b)", re.U|re.I): u"om\\1",
re.compile(u"ę([pbfvwm]|\\b)", re.U|re.I): u"em\\1",
re.compile(u"ą", re.U|re.I): u"on",
re.compile(u"ę", re.U|re.I): u"en",
}

re_words = re.compile(r"\b(\w+)\b", re.U)
re_letters = re.compile(u"\\b([bcdfghjlmnpqrstvxyBCDFGHJLMNPQRSTVXYśżźćłńŚŻŹĆŁŃ])\\b", re.U)
abbreviationsLength = 5
re_abbreviations = re.compile(u"\\b([bcdfghjklmnpqrstvwxzčćđšžłżśźńбвгджзйклмнпрстфхцчшщѳђјљњћџ]{2,})\\b", re.U)
re_capAbbreviations = re.compile(u"([bcdfghjklmnpqrstvwxzčćđšžłżśźńбвгджзйклмнпрстфхцчшщѳђјљњћџ]{3,})",re.U|re.I)
re_decimalFractions = re.compile(r"\d+(\.)\d+")
re_numbers = re.compile(r"(\d+)", re.U)
re_afterNumber = re.compile(r"(\d+)([^\.\:\-\/\!\?\d])", re.U)
re_omittedCharacters = re.compile(u"['\\(\\)\\*„_\\\"‘’«»‚]+", re.U)
re_zeros = re.compile(r"\b\a?\.?(0+)")
zeros = {
'ru': u'ноль ',
'uk': u'нуль ',
}
re_stress = re.compile(u"([аеёиоуыэюяіѣѵ])́", re.U|re.I)

AllLetters = {}
AllLetters.update(letters)
AllLetters.update(ru.letters)

def expandAbbreviation(match):
	loweredText = match.group(1).lower()
	l = len(match.group(1))
	if (match.group(1).isupper() and (l <= abbreviationsLength and l > 1) and re_capAbbreviations.match(match.group(1))) or re_abbreviations.match(loweredText):
		expandedText = ""
		for letter in loweredText:
			expandedText += AllLetters[letter] if letter in AllLetters else letter
			if letter.isalpha(): expandedText+=" "
		return expandedText
	return loweredText

def subLetters(match):
	letter = match.group(1).lower()
	return letters[letter]

def preprocessText(text):
	for rule in exceptions:
		text = rule.sub(exceptions[rule], text)
	for rule in rules:
		text = rule.sub(rules[rule], text)
	text = re_letters.sub(subLetters, text)
	for s in pronunciation:
		text = text.replace(s, pronunciation[s])
	text = text.replace(u"ьi", u"и") # Еще один костыль.
	return text

def preprocessNumbers(text, language):
	text = re_decimalFractions.sub(lambda m: m.group(0).replace(m.group(1), ","), text)
	text = re_numbers.sub(lambda m: pl_numbers.numbersToWords(m.group(1)), text)
	return text

def process(text,language):
	if len(text) == 1:
		char = text.lower()
		if char in letters: return letters[char]
		elif char.isdigit(): return preprocessText(preprocessNumbers(char, language))
		elif char in ru.letters: return ru.letters[char]
		else: return char
	text = re_omittedCharacters.sub(" ", text)
	text = preprocessNumbers(text, language)
	text = re_words.sub(expandAbbreviation,text) #this also lowers the text
	text = preprocessText(text)
	text = ru.preprocessText(text)
	text = re_stress.sub(u"\\1\\+", text)
	text = re_afterNumber.sub(r"\1-\2", text)
	return text
