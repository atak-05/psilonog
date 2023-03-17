import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
from gtts import gTTS
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import random
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from nltk.chat.util import Chat, reflections
from playsound import playsound
import googletrans
from googletrans import *
#Translators ==============================================================================================================

def translator_en(text):
    translator = Translator()
    translation = translator.translate(text , src='tr' ,dest='en')
    return translation.text


def translator_tr(text):
    translator = Translator()
    translation = translator.translate(text , src='en' ,dest='tr')
    return translation.text


#Speak ==============================================================================================================
import os
def speak(string):
    tts= gTTS(text=string, lang="tr")
    file1 = "./voice/answer"+str(random.randint(0,10000000000000000000000))+ ".mp3"
    tts.save(file1)
    playsound(sound = file1)
    
#Save ==============================================================================================================
    
    
def save_voice():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        voice = r.listen(source)
        
        talk_voice = " "
        try :
            talk_voice = r.recognize_google(voice, language="Tr-tr")
            print(talk_voice)
        except Exception as e:
            speak("Anlamadım")
    return talk_voice

#Tokenize ==============================================================================================================

def kelime_lemmatize_et(kelime):
    lemmatizer = WordNetLemmatizer()
    print(lemmatizer)
    lemma = lemmatizer.lemmatize(kelime, get_wordnet_pos(kelime))
    print("lemma"+ lemma)
    return lemma

def get_wordnet_pos(kelime):
    tag = nltk.pos_tag([kelime])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)


def bot_cevap(mesaj):
    mesaj = translator_en(mesaj)
    sid = SentimentIntensityAnalyzer()
    
    mesaj_duygusu = sid.polarity_scores(mesaj)
    print("=================================")
    print("Çeviriden önce "+ mesaj)
    mesaj = translator_tr(mesaj)
    print("=================================")
    mesaj = "Çeviriden sonra " + mesaj
    print(mesaj_duygusu)
    print("=================================")
    print(mesaj)
    print("=================================")
    if mesaj_duygusu['compound'] >= 0.05:
        cevap = "Mükemmel1"
    elif mesaj_duygusu['compound'] <= -0.05:
        cevap = "Bu çok üzücü"
    else:
        cevap = "Evet bazen herşey kafa karıştırıcı olabiliyor."
    kelimeler = word_tokenize(mesaj)
    worknet= [translator_en(kelime) for kelime in kelimeler]
    worknet = [get_wordnet_pos(kelime) for kelime in kelimeler]
    print(worknet)
    kelimeler = [kelime.lower() for kelime in kelimeler]
    print("Sonraki =================================")
    print(worknet)
    print("=================================")
    if any(kelime in kelimeler for kelime in ['mutlu', 'sevinçli', 'keyifli', 'güzel']):
         cevap = "Senin adına mutluyum"
    elif any(kelime in kelimeler for kelime in ['üzgün', 'kötüyüm', 'moralli']):
         cevap =" Bunun için üzgünüm"

    return speak(cevap)
    
