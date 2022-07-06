# -*- coding: utf-8 -*-
# A part from newfon speech synthesizer
# Copyright (C) 2019/2022 Sergey Shishmintsev, Alexy Sadovoi, Sergey A.K.A. Electrik, Kvark and other developers

import re
try:
	from . import en
except ImportError: # for NVDA below 2019.3
	import en

options = {}

rules = {
	re.compile(u"\\b(й)\\s",re.U|re.I): U"й",
	re.compile(u"\\b(з)\\s",re.U|re.I): U"з",
	re.compile(u"\\s(ж)\\b",re.U|re.I): U"ж",
	re.compile(u"\\s(б)\\b",re.U|re.I): U"б",
	re.compile(u"'([яюєї])",re.I|re.U): u"ьй\\1",
	re.compile(u"ц([ьіяюєї])",re.U|re.I): U"тс\\1",
}

#ukrainian to russian character map
#ukrainian soft "g" is not supported, becouse synth does not contain this phonem :(
pronunciation = {
	u"и": u"ы",
	u"і": u"и",
	u"ї": u"ййи",
	u"е": u"э",
	u"є": u"е",
	u"ґ": u"г",
}

pronunciationOrder = [u"и",u"і", u"ї", u"е", u"є", u"ґ"]

letters = {
	u"б": u"бэ",
	u"в": u"вэ",
	u"г": u"гэ",
	u"д": u"дэ",
	u"ж": u"же",
	u"з": u"зэ",
	u"й": u"йот",
	u"к": u"ка",
	u"л": u"эль",
	u"м": u"эм",
	u"н": u"эн",
	u"п": u"пэ",
	u"р": u"эр",
	u"с": u"эс",
	u"т": u"тэ",
	u"ф": u"эф",
	u"х": u"ха",
	u"ц": u"це",
	u"ч": u"че",
	u"ш": u"ша",
	u"щ": u"ща",
	u"ъ": u"твэррдый знак",
	u"ь": u"мъякый знак",
	u"ґ": u"Твэрдэ+ гэ",
	u"и": u"ы",
	u"і": u"и",
	u"ї": u"ййи",
	u"е": u"э",
	u"є": u"е",
}

zeros=[u"нуль ",u"нулі ",u"нулів "]
re_zeros = re.compile(r"\b\a?\.?(0+)")
re_words = re.compile(r"\b(\w+)\b",re.U)

abbreviationsLength = 4
re_abbreviations = re.compile(u"\\b([\\d,bcdfghjklmnpqrstvwxzбвгджзклмнпрстфхцчшщ]{2,})\\b",re.U)
re_capAbbreviations = re.compile(u"([bcdfghjklmnpqrstvwxzбвгджзклмнпрстфхцчшщ]{3,})",re.U|re.I)
re_decimalFractions = re.compile(r"\d+(\.)\d+")
re_afterNumber = re.compile(r"(\d+)([^\.\:\-\/\!\?\d])")
re_omittedCharacters = re.compile(r"[\(\)\*_\"]+")
re_zeros = re.compile(r"\b\a?\.?(0+)")
re_stress = re.compile(u"([аеёиоуыэюяіѣѵ])́", re.U|re.I)

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
		#stupid python! replace() does not have ignore case, reg exprs also sucks
		text = text.replace(s.upper(), pronunciation[s])
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
#	text = re_stress.sub(u"\\1\\+", text)
	text = re_afterNumber.sub(r"\1-\2", text)
	return text
