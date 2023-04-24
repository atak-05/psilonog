from gtts import gTTS
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import random
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from nltk.chat.util import Chat, reflections
from playsound import playsound


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

hAU = ["nasılsın", "nasıl gidiyor", "napıyorsun", "neler yapıyorsun", "ne yapıyorsun"]

hAU_answer_bad=["kötüyüm", "igrencim","kötü hissediyorum" ]
hAU_answer_good=["iyiyim", "mükemmelim","iyi gidiyor" ]
hAU_answer_neut=["bilmiyorum", "idare eder" ]
while True:
    text = save_voice().lower()

    if any(word in text for word in greetings):
        for item in greetings:
            speak(item)
            break

    if any(word in text for word in hAU):
        speak("İdare eder sen nasılsın?")    
    if any(word in text for word in hAU_answer_bad):
        speak("Bunu duyduğuma üzüldüm.")
    if any(word in text for word in hAU_answer_good):
        speak("Bunu duyduğuma sevindim.")
    if any(word in text for word in hAU_answer_neut):
        speak(" bence mutlu olmalısın.")
    
    

    if "bay bay" in text:
        speak("Kendine iyi bak!")
        break