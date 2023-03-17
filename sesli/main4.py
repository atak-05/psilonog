

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


nltk.download('averaged_perceptron_tagger')
nltk.download('vader_lexicon')

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

def translator_en(text):
    translator = Translator()
    translation = translator.translate(text , src='tr' ,dest='en')
    return text

def translator_tr(text):
    translator = Translator()
    translation = translator.translate(text , src='en' ,dest='tr')
    return text

def bot_cevap(mesaj):
    sorular = [
        "Nasılsın?",
        "Bugün nasıl hissediyorsun?",
        "Son zamanlarda ne yaptın?",
        "Dün nasıldı?",
        "Senin için neyin önemli?",
        "Sana ne yapmaktan hoşlanırsın?",
        "Bugün neler yapmayı planlıyorsun?",
        "Hafta sonu ne yapacaksın?",
        "Hayatında en çok neyin önemli olduğunu düşünüyorsun?",
        "En sevdiğin yemek nedir?",
        "En sevdiğin film nedir?",
        "Hangi hobilerin var?",
        "En son hangi kitabı okudun?",
        "Senin için hayatın amacı nedir?",
        "Hayatta en büyük hayalin nedir?"
    ]

    cevaplar = [
        "İyiyim, teşekkür ederim. Sen nasılsın?",
        "Bugün kendimi harika hissediyorum, sen nasıl hissediyorsun?",
        "Geçen hafta sonu seyahat ettim ve çok eğlendim. Sen son zamanlarda ne yaptın?",
        "Dün işe gittim ve oldukça yoğundu. Senin dün nasıl geçti?",
        "Ailem, arkadaşlarım ve sağlığım benim için önemlidir. Senin için neyin önemli olduğunu düşünüyorsun?",
        "Kitap okumaktan, yürüyüş yapmaktan ve arkadaşlarımla zaman geçirmekten hoşlanırım. Sana ne yapmaktan hoşlandığınızı sorsam?",
        "Bugün arkadaşlarımla buluşacağım ve piknik yapacağız. Sen bugün neler yapacaksın?",
        "Hafta sonu deniz kenarında yürüyüş yapmayı planlıyorum. Sen ne yapacaksın?",
        "Ailem ve sevdiklerimle birlikte vakit geçirmek, yeni şeyler öğrenmek ve insanlara yardım etmek benim için önemli. Peki ya senin için hayatın amacı nedir?",
        "En sevdiğim yemek spagetti carbonara. Senin favori yemeğin nedir?",
        "En sevdiğim film 'The Shawshank Redemption'. Senin favori filmin nedir?",
        "Müzik dinlemek, yüzmek ve yoga yapmak gibi hobilerim var. Senin hobilerin neler?",
        "En son 'Beyaz Diş' adlı kitabı okudum. Senin en son okuduğun kitap nedir?",
        "Hayatın amacı insanlara yardım etmek ve dünyayı daha iyi bir yer haline getirmek. Senin için hayatta en büyük hayal nedir?",
        "Bir gün dünya barışını sağlamak benim en büyük hayalim. Peki ya senin hayatta en büyük hayalin nedir?"
    ]
    sid = SentimentIntensityAnalyzer()
    mesaj = translator_en(mesaj)
    mesaj_duygusu = sid.polarity_scores(mesaj)
    print(mesaj_duygusu)
    if mesaj_duygusu['compound'] >= 0.05:
        cevap = cevaplar[0]
    elif mesaj_duygusu['compound'] <= -0.05:
        cevap = cevaplar[1]
    else:
        cevap = cevaplar[2]
    mesaj= translator_tr(mesaj)
    kelimeler = word_tokenize(mesaj)
    kelimeler = [kelime.lower() for kelime in kelimeler]
    print(kelimeler)
    yeni_kelimeler = []
    for kelime in kelimeler:
        if kelime.isalnum():
            yeni_kelimeler.append(kelime_lemmatize_et(kelime))
    print(yeni_kelimeler)

    if any(kelime in yeni_kelimeler for kelime in ['mutlu', 'sevinçli', 'keyifli', 'güzel']):
        cevap = cevaplar[0]
    elif any(kelime in yeni_kelimeler for kelime in ['üzgün', 'kötüyüm', 'moralli']):
        cevap = cevaplar[1]

    return speak(cevap)




import os
def speak(string):
    tts= gTTS(text=string, lang="tr")
    file1 = "./voice/answer"+str(random.randint(0,10000000000000000000000))+ ".mp3"
    tts.save(file1)
    playsound(sound = file1)
    

       
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





greetings = ["selam", "merhaba", "hey"]
bye = ["bay bay","sonra görüşürüz","kapat"]


while True:
    text = save_voice().lower()
    
    if any(word in text for word in greetings):
        for item in greetings:
            speak(item)
            break

    if any(word in text for word in bye):
        for item in bye:
            speak(item)
            break
        break        
    else:
        bot_cevap(text)
# chat = Chat(ciftler, reflections)
# chat.converse(quit="bitti")

# with open('./data/data_set.txt', 'r') as file:
#     text = file.read()





