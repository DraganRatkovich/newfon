# -*- coding: utf-8 -*-

import re

options = {}

letters = {
	'a': u"эй",
	'b': u"би",
	'c': u"си",
	'd': u"ди",
	'e': u"и",
	'f': u"эф",
	'g': u"джи",
	'h': u"эйчь",
	'i': u"ай",
	'j': u"джей",
	'k': u"кей",
	'l': u"эл",
	'm': u"эм",
	'n': u"эн",
	'o': u"оу",
	'p': u"пи",
	'q': u"къю",
	'r': u"ар",
	's': u"эс",
	't': u"ти",
	'u': u"ю",
	'v': u"ви",
	'w': u"да+блъю",
	'x': u"экс",
	'y': u"вай",
	'z': u"зэт",
}

latin = {
	'a': u"а",
	'b': u"бэ",
	'c': u"цэ",
	'd': u"дэ",
	'e': u"е",
	'f': u"эф",
	'g': u"гэ",
	'h': u"ха",
	'i': u"и",
	'j': u"ёт",
	'k': u"ка",
	'l': u"эл",
	'm': u"эм",
	'n': u"эн",
	'o': u"о",
	'p': u"пи",
	'q': u"ку",
	'r': u"эр",
	's': u"эс",
	't': u"тэ",
	'u': u"у",
	'v': u"вэ",
	'w': u"дубль вэ",
	'x': u"икс",
	'y': u"игрек",
	'z': u"зэт",
}


pronunciation = {
	'x': u"кс",
	'ee': u"е е",
	'e': u"е",
	'y': u"ы",
	'j': u"дж",
}

pseudoEnglishPronunciation = {
	'x': u"кс",
	'ee': u"э э",
	'e': u"э",
	'y': u"ы",
	'j': u"дж",
}

re_englishLetters = re.compile(r"\b([a-zA-Z])\b")
re_stress = re.compile(u"([аеёиоуыэюяіѣѵ])́", re.U|re.I)

def subEnglishLetters(match):
	letter = match.group(1).lower()
	return letters[letter]

def preprocessText(text):
	englishPronunciation = pseudoEnglishPronunciation if options.get("pseudoEnglishPronunciation") == True else pronunciation
	text = re_englishLetters.sub(subEnglishLetters, text)
	for s in englishPronunciation:
		text = text.replace(s, englishPronunciation[s])
	return text
