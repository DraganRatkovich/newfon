# -*- coding: utf-8 -*-
# A part from newfon speech synthesizer
# Copyright (C) 2019/2022 Sergey Shishmintsev, Alexy Sadovoi, Sergey A.K.A. Electrik, Kvark and other developers

import re

SAY_SERBO_CROATIAN_NUMBERS=True

re_jat = re.compile(r"vi?je")

def dajDlugoscNapisu(napis):
 dlugosc=len(napis)
 return dlugosc

def dajZnakNapisu(napis, indeks):
 if (indeks>0) and (indeks<=len(napis)):
  znak=napis[(indeks-1)]
 else:
  znak=chr(0)
 return znak

def dajFragmentNapisu(napis, indeks, dlugoscFragmentu):
 dlugoscNapisu=len(napis)
 fragment=''
 if (indeks>0) and (indeks<=dlugoscNapisu):
  if ((indeks+dlugoscFragmentu-1)>0) and ((indeks+dlugoscFragmentu-1)<=dlugoscNapisu):
   if (indeks<=(indeks+dlugoscFragmentu-1)):
    fragment=napis[(indeks-1):((indeks-1)+dlugoscFragmentu)]
 return fragment

def dajPolaczoneNapisy(napisPierwszy, napisDrugi):
 napis=napisPierwszy+napisDrugi
 return napis

def napisySaTakieSame(napisPierwszy, napisDrugi):
 dlugoscPierwsza=len(napisPierwszy)
 dlugoscDruga=len(napisDrugi)
 takieSame=False
 indeks=0
 if dlugoscPierwsza==dlugoscDruga:
  takieSame=True
  indeks=1
  while (indeks<=dlugoscPierwsza) and takieSame:
   if dajZnakNapisu(napisPierwszy, indeks)==dajZnakNapisu(napisDrugi, indeks):
    indeks=indeks+1
   else:
    takieSame=False
 return takieSame

def wartosciaNapisuJestPoprawnaLiczbaNaturalna(napis):
 indeks=0
 dlugosc=dajDlugoscNapisu(napis)
 jestLiczba=False
 znak=chr(0)
 if dlugosc>0:
  indeks=1
  jestLiczba=True
  while (indeks<=dlugosc) and jestLiczba:
   znak=dajZnakNapisu(napis, indeks)
   if (znak>='0') and (znak<='9'):
    indeks=indeks+1
   else:
    jestLiczba=False
 return jestLiczba

def dajLiczbeBezNieznaczacychZerNaPoczatku(napis):
 napis_1=''
 indeks=0
 dlugosc=dajDlugoscNapisu(napis)
 jeszcze=False
 if wartosciaNapisuJestPoprawnaLiczbaNaturalna(napis):
  indeks=1
  jeszcze=True
  while (indeks<dlugosc) and jeszcze:
   if (dajZnakNapisu(napis, indeks)=='0'):
    indeks=indeks+1
   else:
    jeszcze=False
  napis_1=dajFragmentNapisu(napis, indeks, dlugosc-indeks+1)
 return napis_1

def dajPostacSlownaJednejCyfry(znak):
 napis=''
 if znak=='0':
  napis=u'nula'
 if znak=='1':
  napis=u'jedan'
 if znak=='2':
  napis=u'dva'
 if znak=='3':
  napis=u'tri'
 if znak=='4':
  napis=u'četiri'
 if znak=='5':
  napis=u'pet'
 if znak=='6':
  napis=u'šest'
 if znak=='7':
  napis=u'sedam'
 if znak=='8':
  napis=u'osam'
 if znak=='9':
  napis=u'devet'
 return napis

def dajPostacSlownaDziesiatki(znak):
 napis=''
 if znak=='1':
  napis=u'deset'
 if znak=='2':
  napis=dajPolaczoneNapisy(dajPostacSlownaJednejCyfry(znak), u'deset')
 if znak=='3':
  napis=dajPolaczoneNapisy(dajPostacSlownaJednejCyfry(znak), u'deset')
 if znak=='4':
  napis=dajPolaczoneNapisy(dajFragmentNapisu(dajPostacSlownaJednejCyfry(znak), 1, dajDlugoscNapisu(dajPostacSlownaJednejCyfry(znak))-1).replace("i", "", 1), u'deset')
 if (znak>='5') and (znak<='9'):
  napis=dajPolaczoneNapisy(dajPostacSlownaJednejCyfry(znak), u'deset')
 return napis

def dajPostacSlownaNascie(znak):
 napis=''
 if (znak=='1'):
  napis=dajPolaczoneNapisy(dajPostacSlownaJednejCyfry(znak), u'aest')
 if (znak=='4'):
  napis=dajPolaczoneNapisy(dajFragmentNapisu(dajPostacSlownaJednejCyfry(znak), 1, dajDlugoscNapisu(dajPostacSlownaJednejCyfry(znak))-1).replace("i", "", 1), u'naest')
 if (znak=='2') or (znak=='3') or (znak=='7') or (znak=='8'):
  napis=dajPolaczoneNapisy(dajPostacSlownaJednejCyfry(znak), u'naest')
 if znak=='6':
  napis=u'šesnaest'
 if (znak=='5') or (znak=='9'):
  napis=dajPolaczoneNapisy(dajFragmentNapisu(dajPostacSlownaJednejCyfry(znak), 1, dajDlugoscNapisu(dajPostacSlownaJednejCyfry(znak))-1), u'tnaest')
 return napis

def dajPostacSlownaLiczbyDwucyfrowej(napis):
 napis_1=''
 napis_2=''
 napis_3=''
 znak_1=chr(0)
 znak_2=chr(0)
 if dajDlugoscNapisu(napis)==2:
  if wartosciaNapisuJestPoprawnaLiczbaNaturalna(napis):
   znak_1=dajZnakNapisu(napis, 1)
   znak_2=dajZnakNapisu(napis, 2)
   if (znak_1>='1') and (znak_1<='9') and (znak_2=='0'):
    napis_1=dajPostacSlownaDziesiatki(znak_1)
   else:
    if (znak_2>='1') and (znak_2<='9'):
     if (znak_1=='0'):
      napis_1=dajPostacSlownaJednejCyfry(znak_2)
     if (znak_1=='1'):
      napis_1=dajPostacSlownaNascie(znak_2)
     if (znak_1>='2') and (znak_1<='9'):
      napis_2=dajPostacSlownaDziesiatki(znak_1)
      napis_3=dajPostacSlownaJednejCyfry(znak_2)
      if (dajDlugoscNapisu(napis_2)==0) or (dajDlugoscNapisu(napis_3)==0):
       napis_1=dajPolaczoneNapisy(napis_2, napis_3)
      else:
       napis_1=dajPolaczoneNapisy(dajPolaczoneNapisy(napis_2, ' '), napis_3)
 return napis_1

def dajPostacSlownaSetki(znak):
 napis=''
 if znak=='1':
  napis=u'sto'
 if znak=='2':
  napis=u'dvjesto'
 if (znak=='3') or (znak=='4'):
  napis=dajPolaczoneNapisy(dajPostacSlownaJednejCyfry(znak), u'sto')
 if (znak>='5') and (znak<='9'):
  napis=dajPolaczoneNapisy(dajPostacSlownaJednejCyfry(znak), u'sto')
 return napis

def dajPostacSlownaLiczbyTrzycyfrowej(napis):
 napis_1=''
 znak=chr(0)
 if dajDlugoscNapisu(napis)==3:
  if wartosciaNapisuJestPoprawnaLiczbaNaturalna(napis):
   znak=dajZnakNapisu(napis, 1)
   napis_1=dajPostacSlownaLiczbyDwucyfrowej(dajFragmentNapisu(napis, 2, 2))
   if (znak>='1') and (znak<='9'):
    if dajDlugoscNapisu(napis_1)==0:
     napis_1=dajPostacSlownaSetki(znak)
    else:
     napis_1=dajPolaczoneNapisy(dajPolaczoneNapisy(dajPostacSlownaSetki(znak), ' '), napis_1)
 return napis_1

def dajOdmianeTysiaca(znak):
 odmiana=''
 if znak=='1':
  odmiana=u'hiljada'
 if (znak>='2') and (znak<='4'):
  odmiana=u'hiljada'
 if (znak=='0') or ((znak>='5') and (znak<='9')):
  odmiana=u'hiljada'
 return odmiana

def dajOdmianeLiona(napis, znak):
 odmiana=''
 if dajDlugoscNapisu(napis)>0:
  if znak=='1':
   odmiana=u'lion'
  if (znak>='2') and (znak<='4'):
   odmiana=u'liona'
  if (znak=='0') or ((znak>='5') and (znak<='9')):
   odmiana=u'liona'
  if dajDlugoscNapisu(odmiana)>0:
   odmiana=dajPolaczoneNapisy(napis, odmiana)
 return odmiana

def dajOdmianeLiarda(napis, znak):
 odmiana=''
 if dajDlugoscNapisu(napis)>0:
  if znak=='1':
   odmiana=u'lijarda'
  if (znak>='2') and (znak<='4'):
   odmiana=u'lijarde'
  if (znak=='0') or ((znak>='5') and (znak<='9')):
   odmiana=u'lijardi'
  if dajDlugoscNapisu(odmiana)>0:
   odmiana=dajPolaczoneNapisy(napis, odmiana)
 return odmiana

def dajOdmianeMiliona(znak):
 odmiana=''
 odmiana=dajOdmianeLiona(u'mi', znak)
 return odmiana

def dajOdmianeMiliarda(znak):
 odmiana=''
 odmiana=dajOdmianeLiarda(u'mi', znak)
 return odmiana

def dajOdmianeBiliona(znak):
 odmiana=''
 odmiana=dajOdmianeLiona(u'bi', znak)
 return odmiana

def dajOdmianeBiliarda(znak):
 odmiana=''
 odmiana=dajOdmianeLiarda(u'bi', znak)
 return odmiana

def dajOdmianeTryliona(znak):
 odmiana=''
 odmiana=dajOdmianeLiona(u'tri', znak)
 return odmiana

def dajOdmianeTryliarda(znak):
 odmiana=''
 odmiana=dajOdmianeLiarda(u'tri', znak)
 return odmiana

def dajOdmianeKwadryliona(znak):
 odmiana=''
 odmiana=dajOdmianeLiona(u'kwadri', znak)
 return odmiana

def dajOdmianeKwadryliarda(znak):
 odmiana=''
 odmiana=dajOdmianeLiarda(u'kwadri', znak)
 return odmiana

def dajOdmianeKwintyliona(znak):
 odmiana=''
 odmiana=dajOdmianeLiona(u'kwinti', znak)
 return odmiana

def dajOdmianeKwintyliarda(znak):
 odmiana=''
 odmiana=dajOdmianeLiarda(u'kwinti', znak)
 return odmiana

def dajOdmianeSekstyliona(znak):
 odmiana=''
 odmiana=dajOdmianeLiona(u'seksti', znak)
 return odmiana

def dajOdmianeSeptyliona(znak):
 odmiana=''
 odmiana=dajOdmianeLiona(u'septi', znak)
 return odmiana

def dajOdmianeOktyliona(znak):
 odmiana=''
 odmiana=dajOdmianeLiona(u'okti', znak)
 return odmiana

def dajOdmianeNonyliona(znak):
 odmiana=''
 odmiana=dajOdmianeLiona(u'noni', znak)
 return odmiana

def dajOdmianeDecyliona(znak):
 odmiana=''
 odmiana=dajOdmianeLiona(u'deci', znak)
 return odmiana

def dajOdmianeUndecyliona(znak):
 odmiana=''
 odmiana=dajOdmianeLiona(u'undeci', znak)
 return odmiana

def dajOdmianeDuodecyliona(znak):
 odmiana=''
 odmiana=dajOdmianeLiona(u'duodeci', znak)
 return odmiana

def dajOdmianeCentyliona(znak):
 odmiana=''
 odmiana=dajOdmianeLiona(u'centi', znak)
 return odmiana

def dajOdmianeTysiecy(znak, licznik):
 odmiana=''
 if (znak>='0') and (znak<='9'):
  if licznik==0:
   odmiana=dajOdmianeTysiaca(znak)
  if licznik==1:
   odmiana=dajOdmianeMiliona(znak)
  if licznik==2:
   odmiana=dajOdmianeMiliarda(znak)
  if licznik==3:
   odmiana=dajOdmianeBiliona(znak)
  if licznik==4:
   odmiana=dajOdmianeBiliarda(znak)
  if licznik==5:
   odmiana=dajOdmianeTryliona(znak)
  if licznik==6:
   odmiana=dajOdmianeTryliarda(znak)
  if licznik==7:
   odmiana=dajOdmianeKwadryliona(znak)
  if licznik==8:
   odmiana=dajOdmianeKwadryliarda(znak)
  if licznik==9:
   odmiana=dajOdmianeKwintyliona(znak)
  if licznik==10:
   odmiana=dajOdmianeKwintyliarda(znak)
  if licznik==11:
   odmiana=dajOdmianeSekstyliona(znak)
  if licznik==12:
   odmiana=dajOdmianeSeptyliona(znak)
  if licznik==13:
   odmiana=dajOdmianeOktyliona(znak)
  if licznik==14:
   odmiana=dajOdmianeNonyliona(znak)
  if licznik==15:
   odmiana=dajOdmianeDecyliona(znak)
  if licznik==16:
   odmiana=dajOdmianeUndecyliona(znak)
  if licznik==17:
   odmiana=dajOdmianeDuodecyliona(znak)
  if licznik==18:
   odmiana=dajOdmianeCentyliona(znak)
 return odmiana

def dajGrupe(wartoscGrupy):
 napis=''
 dlugosc=dajDlugoscNapisu(wartoscGrupy)
 if dlugosc==1:
  napis=dajPostacSlownaJednejCyfry(dajZnakNapisu(wartoscGrupy, 1))
 if dlugosc==2:
  napis=dajPostacSlownaLiczbyDwucyfrowej(wartoscGrupy)
 if dlugosc==3:
  napis=dajPostacSlownaLiczbyTrzycyfrowej(wartoscGrupy)
 return napis

def podpiszGrupe(numerGrupy, wartoscGrupy):
 napis=''
 znak=chr(0)
 dlugosc=dajDlugoscNapisu(wartoscGrupy)
 if (dlugosc>0) and (dlugosc<=3):
  znak=dajZnakNapisu(wartoscGrupy, dajDlugoscNapisu(wartoscGrupy))
  if (not (napisySaTakieSame(wartoscGrupy, '1'))) and (znak=='1'):
   znak='0'
  napis=dajOdmianeTysiecy(znak, numerGrupy-2)
 return napis

def dajNapisZLiczbaWPostaciSlownej(napis):
 napis_1=''
 dlugosc=0
 numerGrupy=0
 ileGrup=0
 wartoscGrupy=''
 dlugosc=dajDlugoscNapisu(napis)
 if wartosciaNapisuJestPoprawnaLiczbaNaturalna(napis):
  ileGrup=int((dlugosc-1)/3)+1
  for numerGrupy in range(1, (ileGrup+1)):
   if napisySaTakieSame(napis, '0'):
    wartoscGrupy=napis
   else:
    if numerGrupy==1:
     wartoscGrupy=dajFragmentNapisu(napis, 1, dlugosc-((ileGrup-1)*3))
    else:
     wartoscGrupy=dajFragmentNapisu(napis, dlugosc-((ileGrup-numerGrupy+1)*3)+1, 3)
    wartoscGrupy=dajLiczbeBezNieznaczacychZerNaPoczatku(wartoscGrupy)
    if napisySaTakieSame(wartoscGrupy, '0'):
     wartoscGrupy=''
   if (not napisySaTakieSame(wartoscGrupy, '1')) or (numerGrupy==ileGrup) or (numerGrupy<=(ileGrup-20)):
    if (not napisySaTakieSame(wartoscGrupy, '')) and (numerGrupy>1):
     napis_1=dajPolaczoneNapisy(napis_1, ' ')
    napis_1=dajPolaczoneNapisy(napis_1, dajGrupe(wartoscGrupy))
   if (not napisySaTakieSame(wartoscGrupy, '')) and (numerGrupy<ileGrup):
    if ((not napisySaTakieSame(wartoscGrupy, '1')) and (numerGrupy>(ileGrup-20))) or (numerGrupy>1):
     napis_1=dajPolaczoneNapisy(napis_1, ' ')
    napis_1=dajPolaczoneNapisy(napis_1, podpiszGrupe((ileGrup-numerGrupy+1), wartoscGrupy))
 return napis_1

def dajNapisZLiczbamiWPostaciSlownej(napis):
 napis_1=''
 poprzedni=0
 indeks=1
 dlugosc=dajDlugoscNapisu(napis)
 znak=chr(0)
 jeszcze=False
 if dlugosc == 1: return " "+dajPostacSlownaJednejCyfry(napis)+" "
 while indeks<=dlugosc:
  poprzedni=indeks
  jeszcze=True
  while (indeks<=dlugosc) and jeszcze:
   znak=dajZnakNapisu(napis, indeks)
   if (znak>='0') and (znak<='9'):
    jeszcze=False
   else:
    indeks=indeks+1
  napis_1=dajPolaczoneNapisy(napis_1, dajFragmentNapisu(napis, poprzedni, indeks-poprzedni))
  poprzedni=indeks
  jeszcze=True
  while (indeks<=dlugosc) and jeszcze:
   znak=dajZnakNapisu(napis, indeks)
   if (znak>='0') and (znak<='9'):
    indeks=indeks+1
   else:
    jeszcze=False
  if (indeks-poprzedni)==1:
   napis_1=dajPolaczoneNapisy(napis_1, (dajFragmentNapisu(napis, poprzedni, (indeks-poprzedni))))
  else:
   napis_1=dajPolaczoneNapisy(napis_1, dajNapisZLiczbaWPostaciSlownej(dajFragmentNapisu(napis, poprzedni, (indeks-poprzedni)))).replace("dva hil", "dvije hil")
 return " "+napis_1+" "

def numbersToWords(numbers, variant=""):
	text = dajNapisZLiczbamiWPostaciSlownej(numbers)
	if variant == "hr":
		text = text.replace(u"hiljad", u"tisuć")
		text = text.replace(u"lion", u"lijun")
	elif variant == "sr":
		text = re_jat.sub("ve", text)
	elif variant == "sr_ije":
		pass
	else:
		raise ValueError
	return text
