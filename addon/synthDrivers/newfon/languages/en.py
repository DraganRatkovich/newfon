# -*- coding: utf-8 -*-
# A part from newfon speech synthesizer
# Copyright (C) 2019/2022 Sergey Shishmintsev, Alexy Sadovoi, Sergey A.K.A. Electrik, Kvark and other developers

import re

options = {}

letters = {
	'a': "эй",
	'b': "би",
	'c': "си",
	'd': "ди",
	'e': "и",
	'f': "эф",
	'g': "джи",
	'h': "эйчь",
	'i': "ай",
	'j': "джей",
	'k': "кей",
	'l': "эл",
	'm': "эм",
	'n': "эн",
	'o': "оу",
	'p': "пи",
	'q': "къю",
	'r': "ар",
	's': "эс",
	't': "ти",
	'u': "ю",
	'v': "ви",
	'w': "да+блъю",
	'x': "экс",
	'y': "вай",
	'z': "зэт",
}

latin = {
	'a': "а",
	'b': "бэ",
	'c': "цэ",
	'd': "дэ",
	'e': "е",
	'f': "эф",
	'g': "гэ",
	'h': "ха",
	'i': "и",
	'j': "ёт",
	'k': "ка",
	'l': "эл",
	'm': "эм",
	'n': "эн",
	'o': "о",
	'p': "пи",
	'q': "ку",
	'r': "эр",
	's': "эс",
	't': "тэ",
	'u': "у",
	'v': "вэ",
	'w': "дубль вэ",
	'x': "икс",
	'y': "игрек",
	'z': "зэт",
}


pronunciation = {
	'x': "кс",
	'ee': "е е",
	'e': "е",
	'y': "ы",
	'j': "дж",
}

pseudoEnglishPronunciation = {
	'x': "кс",
	'ee': "э э",
	'e': "э",
	'y': "ы",
	'j': "дж",
}


re_englishLetters = re.compile(r"\b([a-zA-Z])\b")
re_stress = re.compile("([аеёиоуыэюяіѣѵ])́", re.U|re.I)
re_dash = re.compile(r"(\w)-(\w)")

def subEnglishLetters(match):
	letter = match.group(1).lower()
	return letters[letter]

def preprocessText(text):
	text = re_dash.sub(r"\1 - \2", text)
	englishPronunciation = pseudoEnglishPronunciation if options.get("pseudoEnglishPronunciation") == True else pronunciation
	text = re_englishLetters.sub(subEnglishLetters, text)
	for s in englishPronunciation:
		text = text.replace(s, englishPronunciation[s])
	return text
