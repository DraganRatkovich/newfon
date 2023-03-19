# -*- coding: utf-8 -*-
# A part from newfon speech synthesizer
# Copyright (C) 2019/2022 Sergey Shishmintsev, Alexy Sadovoi, Sergey A.K.A. Electrik, Kvark and other developers

import re
try:
	from . import ru,sh_numbers
except ImportError: # for NVDA below 2019.3
	import ru,sh_numbers

options = {}

letters = {
'a': "а",
'b': "бэ",
'c': "цэ",
'd': "дэ",
'e': "э",
'f': "эф",
'g': "гэ",
'h': "ха",
'i': "и",
'j': "йот",
'k': "ка",
'l': "эл",
'm': "эм",
'n': "эн",
'o': "о",
'p': "пэ",
'q': "квэ",
'r': "эр",
's': "эс",
't': "тэ",
'u': "у",
'v': "вэ",
'w': "дупло вэ",
'x': "икс",
'y': "ипсилон",
'z': "зэ",
"č": "тшэ",
"ć": "че",
"đ": "дье",
"š": "шэ",
"ž": "жэ",
}

pronunciation= {
'e': "э",
'qu': "кв",
'x': "кс",
'y': "и",
"č": "тш",
"ć": "ч",
"đ": "дьй",
'lj': "ль",
'nj': "нь",
"š": "ш",
"ž": "ж",
}

rules = {
re.compile("([vw])([ptkcčćfsšhqx])", re.U|re.I): "\\1ъ\\2",
}

re_words = re.compile(r"\b(\w+)\b", re.U)
re_letters = re.compile("\\b([bcdfghjlmnpqrtvwxyzBCDFGHJLMNPQRTVWXYZčćđšžČĆĐŠŽ])\\b", re.U)
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
	for rule in rules:
		text = rule.sub(rules[rule], text)
	text = re_letters.sub(subLetters, text)
	for s in pronunciation:
		text = text.replace(s, pronunciation[s])
	return text

def preprocessNumbers(text, language):
	text = re_decimalFractions.sub(lambda m: m.group(0).replace(m.group(1), ","), text)
	text = re_numbers.sub(lambda m: sh_numbers.numbersToWords(m.group(1), variant=language), text)
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
