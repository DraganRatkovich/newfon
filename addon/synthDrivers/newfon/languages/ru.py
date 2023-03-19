# -*- coding: utf-8 -*-
# A part from newfon speech synthesizer
# Copyright (C) 2019/2022 Sergey Shishmintsev, Alexy Sadovoi, Sergey A.K.A. Electrik, Kvark and other developers

import re
try:
	from . import en
except ImportError: # for NVDA below 2019.3
	import en

options = {}

letters = {
	"б": "бэ",
	"в": "вэ",
	"г": "гэ",
	"д": "дэ",
	"ж": "же",
	"з": "зэ",
	"й": "и краткое",
	"к": "ка",
	"л": "эль",
	"м": "эм",
	"н": "эн",
	"п": "пэ",
	"р": "эр",
	"с": "эс",
	"т": "тэ",
	"ф": "эф",
	"х": "ха",
	"ц": "це",
	"ч": "че",
	"ш": "ша",
	"щ": "ща",
	"ъ": "твёрдый знак",
	"ь": "мягкий знак",
	"і": "и десятеричное",
	"ѣ": "ять",
	"ѳ": "фита",
	"ѵ": "ижица",
	"ў": "у краткое",
	"ґ": "гэ взрывное",
}

pronunciation = {
"ґ": "г",
"і": "и",
"ѣ": "е",
"ѳ": "ф",
"ѵ": "и",
"ў": "у",
}


rules = {
re.compile("ц([яюьё])", re.U|re.I): "тс\\1",
#re.compile("\\b([жз])\\b", re.U|re.I): "\\1ъ",
}


re_words = re.compile(r"\b(\w+)\b",re.U)

abbreviationsLength = 4
re_abbreviations = re.compile("\\b([\\d,bcdfghjklmnpqrstvwxzбвгджзклмнпрстфхцчшщѳ]{2,})\\b",re.U)
re_capAbbreviations = re.compile("([bcdfghjklmnpqrstvwxzбвгджзклмнпрстфхцчшщѳ]{3,})",re.U|re.I)
re_decimalFractions = re.compile(r"\d+(\.)\d")
re_afterNumber = re.compile(r"(\d+)([^\.\:\-\/\!\?\d])")
re_omittedCharacters = re.compile(r"[\(\)\*_\"]+")
zeros=["ноль ","ноля ","нолей "]
re_zeros = re.compile(r"\b\a?\.?(0+)")
re_stress = re.compile("([аеёиоуыэюяіѣѵ])́", re.U|re.I)

AllLetters = {}
AllLetters.update(en.letters)
AllLetters.update(letters)

def subLetters(match):
	letter = match.group(1).lower()
	return AllLetters[letter]

def preprocessText(text):
	for rule in rules:
		text = rule.sub(rules[rule], text)
	for s in pronunciation:
		text = text.replace(s, pronunciation[s])
	return text

def subZeros(match,zeros):
	l = len(match.group(1))
	if l == 1: return zeros[0]
	text = " " + str(l) + " "
	l = l%10
	if l == 1: return text+ zeros[0]
	elif l <5: return text+zeros[1]
	else: return text+zeros[2]

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

def process(text,language):
	if len(text) == 1:
		letter = text.lower()
		if letter in AllLetters: return AllLetters[letter]
		else: return letter
	text = re_omittedCharacters.sub(" ", text)
	text = re_zeros.sub(lambda match: subZeros(match,zeros),text)
	text = preprocessText(text)
	text = re_words.sub(expandAbbreviation,text) #this also lowers the text
	text = en.preprocessText(text)
	text = re_stress.sub("\\1\\+", text)
	text = re_afterNumber.sub(r"\1-\2", text)
	return text
