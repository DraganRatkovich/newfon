# -*- coding: utf-8 -*-
# A part from newfon speech synthesizer
# Copyright (C) 2019/2022 Sergey Shishmintsev, Alexy Sadovoi, Sergey A.K.A. Electrik, Kvark and other developers

import re
try:
	from . import ru,pl_numbers
except ImportError: # for NVDA below 2019.3
	import ru,pl_numbers

letters = {
'a': "а",
'b' : "бэ",
'c': "цэ",
'd': "дэ",
'e': "э",
'f': "эф",
'g': "ге",
'h': "ха",
'i': "и",
'j': "йот",
'k': "ка",
'l': "эль",
'm': "эм",
'n': "эн",
'o': "о",
'p': "пэ",
'q': "ку",
'r': "эр",
's': "эс",
't': "тэ",
'u': "у",
'v': "фау",
'w': "ву",
'x': "икс",
'y': "игрэк",
'z': "зэт",
"ą": "а носовэ",
"ę": "э носовэ",
"ć": "тьсе",
"ł": "эл",
"ż": "жет",
"ź": "зет",
"ó": "у крэска",
"ń": "энь",
"ś": "эсь",
}

exceptions = {
re.compile("(supe|hipe|cybe)r(z)", re.U|re.I): "\\1р\\2",
re.compile("(ma)r(zn)", re.U|re.I): "\\1р\\2",
re.compile("(ta)r(zan)", re.U|re.I): "\\1р\\2",
re.compile("(e)r(zac)", re.U|re.I): "\\1р\\2",
re.compile("(\\bspe)c(z)", re.U|re.I): "\\1ц\\2",
}

pronunciation= {
'e': "э",
'ń': "нь",
'x': "кс",
'y': "ы",
"ś": "сь",
"ć": "тьсь",
"ł": "л",
"l": "ль",
"dź": "дьзь",
"ż": "ж",
"ź": "зь",
"ó": "у",
"ch": "х",
"cz": "тш",
"rz": "ж",
"sz": "ш",
"qu": "кв",
"v": "ф",
}

rules = {
re.compile("r(zi)", re.U|re.I): "р\\1",
re.compile("([td])([rs]z)", re.U|re.I): "\\1\\1\\2",
re.compile("([ptkfschść]|[cs]z)rz", re.U|re.I): "\\1ш",
re.compile("l(i)", re.U|re.I): "л\\1",
re.compile("([pbfvwszcmn])i([aeouąęó])", re.U|re.I): "\\1ь\\2",
re.compile("([kgh])i(e)", re.U|re.I): "\\1ь\\2",
re.compile("c([iь])", re.U|re.I): "тьс\\1",
re.compile("dz([iь])", re.U|re.I): "дьз\\1",
re.compile("ą([pbfvwm]|\\b)", re.U|re.I): "om\\1",
re.compile("ę([pbfvwm]|\\b)", re.U|re.I): "em\\1",
re.compile("ą", re.U|re.I): "on",
re.compile("ę", re.U|re.I): "en",
}

re_words = re.compile(r"\b(\w+)\b", re.U)
re_letters = re.compile("\\b([bcdfghjlmnpqrstvxyBCDFGHJLMNPQRSTVXYśżźćłńŚŻŹĆŁŃ])\\b", re.U)
abbreviationsLength = 5
re_abbreviations = re.compile("\\b([bcdfghjklmnpqrstvwxzčćđšžłżśźńбвгджзйклмнпрстфхцчшщѳђјљњћџ]{2,})\\b", re.U)
re_capAbbreviations = re.compile("([bcdfghjklmnpqrstvwxzčćđšžłżśźńбвгджзйклмнпрстфхцчшщѳђјљњћџ]{3,})",re.U|re.I)
re_decimalFractions = re.compile(r"\d+(\.)\d+")
re_numbers = re.compile(r"(\d+)", re.U)
re_afterNumber = re.compile(r"(\d+)([^\.\:\-\/\!\?\d])", re.U)
re_omittedCharacters = re.compile("['\\(\\)\\*„_\\\"‘’«»‚]+", re.U)
re_zeros = re.compile(r"\b\a?\.?(0+)")
zeros = {
'ru': u'ноль ',
'uk': u'нуль ',
}
re_stress = re.compile("([аеёиоуыэюяіѣѵ])́", re.U|re.I)

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
	text = text.replace("ьi", "и") # Еще один костыль.
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
	text = re_stress.sub("\\1\\+", text)
	text = re_afterNumber.sub(r"\1-\2", text)
	return text
