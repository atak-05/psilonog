from gtts import gTTS
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import random
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from nltk.chat.util import Chat, reflections
from playsound import playsound
from nltk.corpus import wordnet
import nltk
nltk.download('wordnet')


# chat = Chat(ciftler, reflections)
# chat.converse(quit="bitti")

# with open('./data/data_set.txt', 'r') as file:
#     text = file.read()




#*Speaking---------------------------------------------------------------------------------------


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

hAU = ["nasılsın", "nasıl gidiyor", "napıyorsun", "neler yapıyorsun"]


# while True:
#     text = save_voice().lower()

#     if any(word in text for word in greetings):
#         for item in greetings:
#             speak(item)

#     if any(word in text for word in hAU):
#         speak("İdare eder sen nasılsın?")

#     if "bay bay" in text:
#         speak("Kendine iyi bak!")
#         break








# Kelime ve karşılığı olan kelimelerin listesi
word_list = [["Selam", ["Aleykumselam", "Selam"]]]


# Kullanıcının girdiği kelime





while True:
    # Kelimenin sinonimleri bulunuyor
    text = save_voice().lower()
    synonyms = ["Anlamadım"]
    for syn in wordnet.synsets(text):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    # Kelimenin karşılığı bulunuyor
    output = ""
    for word in word_list:
        if text in word[0]:
            output = word[1]
    # Eğer kelime ile eşleşen karşılık yoksa, sinonimlerden biri seçiliyor
    if not output:
        output = [synonyms[0]]
    
    # Sonuç rastgele bir karşılık seçilerek gösteriliyor
    speak(random.choice(output))