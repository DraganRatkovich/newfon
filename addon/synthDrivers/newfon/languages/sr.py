# -*- coding: utf-8 -*-
# A part from newfon speech synthesizer
# Copyright (C) 2019/2022 Sergey Shishmintsev, Alexy Sadovoi, Sergey A.K.A. Electrik, Kvark and other developers

import re
try:
	from . import hr,ru,sh_numbers
except ImportError: # for NVDA below 2019.3
	import hr,ru,sh_numbers

options = {}

letters = {
"е": "э",
"л": "эл",
"ч": "тше",
"ђ": "дьйе",
"ј": "йот",
"љ": "эль",
"њ": "энь",
"ћ": "че",
"џ": "дже",
}

pronunciation = {
"е": "э",
"ч": "тш",
"ђ": "дьй",
"ј": "й",
"љ": "ль",
"њ": "нь",
"ћ": "ч",
"џ": "дж",
}

rules = {
re.compile("([в])([пткцчћфсшх])", re.U|re.I): "\\1ъ\\2",
}

re_words = re.compile(r"\b(\w+)\b", re.U)
re_letters = re.compile("\\b([елчђјљњћџЕЛЧЂЈЉЊЋЏ])\\b", re.U)
abbreviationsLength = 5
re_abbreviations = re.compile("\\b([bcdfghjklmnpqrstvwxzčćđšžłżśźńбвгджзйклмнпрстфхцчшщѳђјљњћџ]{2,})\\b", re.U)
re_capAbbreviations = re.compile("([bcdfghjklmnpqrstvwxzčćđšžłżśźńбвгджзйклмнпрстфхцчшщѳђјљњћџ]{3,})",re.U|re.I)
re_decimalFractions = re.compile(r"\d+(\.)\d+")
re_numbers = re.compile(r"(\d+)", re.U)
re_afterNumber = re.compile(r"(\d+)([^\.\:\-\/\!\?\d])", re.U)
re_omittedCharacters = re.compile("['\\(\\)\\*„_\\\"‘’«»‚]+", re.U)
re_stress = re.compile("([аеёиоуыэюяіѣѵ])́", re.U|re.I)

allLetters = {}
allLetters.update(ru.letters)
allLetters.update(hr.letters)
allLetters.update(letters)

def expandAbbreviation(match):
	loweredText = match.group(1).lower()
	l = len(match.group(1))
	if (match.group(1).isupper() and (l <= abbreviationsLength and l > 1) and re_capAbbreviations.match(match.group(1))) or re_abbreviations.match(loweredText):
		expandedText = ""
		for letter in loweredText:
			expandedText += allLetters[letter] if letter in allLetters else letter
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
	text = re.sub("([лн])ьо", "\\1ё", text) # Глуповатый такой хак.
	return text

def preprocessNumbers(text, language):
	text = re_decimalFractions.sub(lambda m: m.group(0).replace(m.group(1), ","), text)
	text = re_numbers.sub(lambda m: sh_numbers.numbersToWords(m.group(1), variant=language), text)
	return text

def process(text,language):
	if len(text) == 1:
		char = text.lower()
		if char in hr.letters: return hr.letters[char]
		elif char.isdigit(): return preprocessText(preprocessNumbers(char, language))
		elif char in letters: return letters[char]
		elif char in ru.letters: return ru.letters[char]
		else: return char
	text = re_omittedCharacters.sub(" ", text)
	text = preprocessNumbers(text, language)
	text = text.replace("р", "r") # Криво, но работает.
	text = re_words.sub(expandAbbreviation,text) #this also lowers the text
	text = preprocessText(text)
	text = hr.preprocessText(text)
	text = ru.preprocessText(text)
	text = re_afterNumber.sub(r"\1-\2", text)
	return text
