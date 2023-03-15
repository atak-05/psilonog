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





# while True:
#     # Kelimenin sinonimleri bulunuyor
#     text = save_voice().lower()
#     synonyms = ["Anlamadım"]
#     for syn in wordnet.synsets(text):
#         for lemma in syn.lemmas():
#             synonyms.append(lemma.name())
#     # Kelimenin karşılığı bulunuyor
#     output = ""
#     for word in word_list:
#         if text in word[0]:
#             output = word[1]
#     # Eğer kelime ile eşleşen karşılık yoksa, sinonimlerden biri seçiliyor
#     if not output:
#         output = [synonyms[0]]
    
#     # Sonuç rastgele bir karşılık seçilerek gösteriliyor
#     speak(random.choice(output))
    
    
import nltk
import random
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Veri seti oluşturma
konuşmalar = ['Merhaba!', 'Nasılsın?', 'Benimle konuşmak ister misin?', 'Seni anlıyorum.',
              'Ne yaptın bugün?', 'Hava nasıl?', 'Güzel bir gün, değil mi?', 'Senin adın ne?',
              'Ben bir chatbotum.', 'Sen nelerden hoşlanırsın?', 'Bana bir şaka anlat.', 'Görüşürüz!']

# Veri setini NLTK kütüphanesi ile işleme
nltk.download('punkt')
nltk.download('stopwords')

def tokenize(text):
    """
    Text verisini küçük harflere çevirir ve kelimeleri ayrıştırır.
    """
    tokens = nltk.word_tokenize(text.lower())
    return tokens

def remove_stopwords(tokens):
    """
    Kelimeler arasında anlamsız olanları çıkarır.
    """
    stop_words = set(stopwords.words('turkish') + list(string.punctuation))
    filtered_tokens = [token for token in tokens if token not in stop_words]
    return filtered_tokens

def process_text(text):
    """
    Verilen metni NLTK araçları kullanarak işler.
    """
    tokens = tokenize(text)
    filtered_tokens = remove_stopwords(tokens)
    processed_text = ' '.join(filtered_tokens)
    return processed_text

processed_konuşmalar = [process_text(konuşma) for konuşma in konuşmalar]

# TF-IDF vektörleştirme
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(processed_konuşmalar)

# Botu kullanıcının yanıtlarına göre eğitme
def bot_cevap(text):
    """
    Kullanıcının mesajına göre botun cevabını oluşturur.
    """
    processed_text = process_text(text)
    tfidf_text = vectorizer.transform([processed_text])
    similarities = cosine_similarity(tfidf_text, tfidf_matrix)
    closest = similarities.argsort()[0][-2]
    return konuşmalar[closest]

print('Bot: Merhaba, ben bir chatbotum. Sana nasıl yardımcı olabilirim?')

while True:
    kullanıcı_girdisi = input('Kullanıcı: ')
    if kullanıcı_girdisi.lower() == 'görüşürüz':
        print('Bot: Görüşmek üzere!')
        break
    else:
        cevap = bot_cevap(kullanıcı_girdisi)
        print('Bot:', cevap)
