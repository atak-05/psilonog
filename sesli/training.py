import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer


from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
#1-SETTING UP INTENTS(look intents.json)
#2-LOAD TRAINING DATA
lemmatizer = WordNetLemmatizer

intents = json.loads(open('intents.json').read())

words = []
classes = []
documents = []
ignore_letters = ['?','!','.',',']


for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list,intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])
            
lemmatizer = WordNetLemmatizer()
words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]

"""
Üstteki kod parçası, bir JSON dosyasından (burada 'intents.json' olarak adlandırılır) yüklü olan bir dizi niyeti temsil eden verileri kullanarak bir NLP modeli oluşturur.

İlk olarak, json.loads(open('intents.json').read()) kodu, 'intents.json' dosyasındaki JSON verilerini yükler ve bu verileri Python sözlüklerine dönüştürür.

Daha sonra, words, classes ve documents adlı boş listeler oluşturulur ve ignore_letters adlı bir karakter dizisi tanımlanır.

for döngüleri, her bir niyet için patterns listesindeki her bir kalıp kelime listesi oluşturulur ve words listesi ile birleştirilir. documents listesi, her bir kelime listesi ve ilgili niyet etiketi ile bir demet olarak oluşturulur. classes listesi, sadece eşsiz niyet etiketlerini içerir.

Daha sonra, WordNetLemmatizer() sınıfından bir nesne oluşturulur ve words listesindeki her kelime lemmatize edilir. ignore_letters listesindeki herhangi bir işaretleyici kelime lemmatize edilmez. Bu adımdan sonra, words listesi, tüm kelimelerin lemmatize edilmiş hallerini içerir.

Bu kod parçası, bir NLP modeli için ön işleme adımlarını gerçekleştirir ve daha sonra bu verileri kullanarak bir model eğitmek için kullanılabilir.

Lemmatize etmek, bir kelimenin kökünü bulmak için uygulanan bir dil işleme tekniğidir. Bu işlem, kelimenin farklı biçimleri arasındaki ilişkiyi anlamak ve kelimenin anlamını daha iyi anlamak için yapılır.

Örneğin, "koştu", "koşuyor" ve "koşmak" kelimeleri aynı kök kelime olan "koş" kelimesine lemmatize edilebilir. Bu, bu kelimelerin aynı anlamı taşıdığını belirleyerek, kelime tabanlı analizlerde daha doğru sonuçlar verir.

Lemmatize işlemi genellikle doğal dil işleme (NLP) ve makine öğrenmesi modelleri gibi dil tabanlı uygulamalarda kullanılır.

Bu kod parçası, words ve classes listelerindeki benzersiz öğeleri sıralamak için kullanılır.
"""


words = sorted(set(words))

classes = sorted(set(classes))

print(classes)


"""
İlk olarak, set(words) ve set(classes) kodları, sırasıyla words ve classes listelerindeki benzersiz öğeleri içeren set'leri oluşturur.

Daha sonra, sorted() fonksiyonu, bu set'leri alfabetik sıraya göre sıralar.

Son olarak, sorted() fonksiyonunun sonucu tekrar listeye dönüştürülür ve sıralanmış benzersiz öğeler içeren yeni listeler oluşturulur.

Bu kod parçası, daha sonra kullanılacak olan benzersiz kelimeler ve niyet etiketlerinin sıralanmış listelerini oluşturur.

"""

pickle.dump(words,open('words.pk1','wb'))
pickle.dump(classes,open('classes.pk1','wb'))
""" 
Bu kod bloğu, words ve classes listelerini pickle modülü kullanarak diskteki dosyalara kaydetmek için kullanılır.

İlk satır, words listesini 'words.pk1' dosyasına pickle modülü ile kaydeder. open('words.pk1','wb') ifadesi, 'words.pk1' dosyasını yazma modunda açar.

İkinci satır, classes listesini 'classes.pk1' dosyasına pickle modülü ile kaydeder. open('classes.pk1','wb') ifadesi, 'classes.pk1' dosyasını yazma modunda açar.

Bu kod bloğu, words.pk1 ve classes.pk1 adlı iki ayrı dosyada, sıralanmış benzersiz kelimeler ve niyet etiketlerini depolar. Bu dosyalar daha sonra uygulamanın farklı yerlerinde kullanılabilir.

"""
#3-​‌‍‌PREPARE TRAINING DATA​
training = []
output_empty = [0] * len(classes)
lemmatizer = WordNetLemmatizer()

for document in documents:
    bag = []
    word_patterns =document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns ]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
        
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag,output_row])
"""
Bu kod bloğu, documents listesindeki her belge için bir öğrenme veri seti oluşturur.

İlk önce, word_patterns adlı bir liste oluşturulur. Bu liste, her belgedeki kelime örüntülerini içerir ve daha sonra lemmatize edilir.

Daha sonra, her belgedeki kelime örüntüleri ve words listesi karşılaştırılır ve bag adlı bir torba oluşturulur. Her kelime için bir "1" veya "0" değeri eklenir. Kelime, kelime örüntüsü içinde geçerse "1" olur, aksi takdirde "0" olur.

Son olarak, output_row adlı bir liste oluşturulur ve önceki kod parçasında oluşturulan classes listesindeki niyet etiketinin dizininde "1" olarak ayarlanır. Böylece, her bir öğrenme örneğinde, bag listesi kelime varlıklarını, output_row listesi ise niyet etiketini belirtir.

training listesi, tüm öğrenme örneklerini içerir ve her bir öğrenme örneği, bir bag listesi ve bir output_row listesi içeren bir listeyi temsil eder.

Bu kod bloğu, bir doğrusal regresyon modeli gibi bir makine öğrenmesi algoritması ile kullanılabilecek bir öğrenme veri seti oluşturur.
"""
random.shuffle(training)
training = np.array(training)

train_x = list(training[:,0])
train_y = list(training[:,1])


""" 
Bu kod bloğu, training listesini önce rasgele karıştırır ve ardından train_x ve train_y listelerini oluşturur.

training listesi, önceki kod bloğunda oluşturulan öğrenme örneklerini içerir ve her bir öğrenme örneği, bag listesi ve output_row listesi içeren bir liste içerir.

random.shuffle(training) ifadesi, training listesindeki öğeleri rasgele karıştırır.

training listesi daha sonra np.array() fonksiyonuyla numpy dizisine dönüştürülür. Bu, train_x ve train_y listeleri için daha sonra kullanılacak numpy dizilerini oluşturmak için gereklidir.

train_x ve train_y listeleri, training dizisinin sırasıyla ilk ve ikinci sütunlarından oluşur. [:,0] ifadesi, training dizisinin tüm satırlarını ve ilk sütununu seçer. [:,1] ifadesi, training dizisinin tüm satırlarını ve ikinci sütununu seçer.

train_x ve train_y listeleri, öğrenme veri setinin özelliklerini ve hedeflerini içerir ve daha sonra bir makine öğrenmesi modeli ile eğitilebilir.
"""
#4-​‌‍‌BUILD NEURAL NETWORK​
from keras.optimizers import Adam

model = Sequential()
model.add(Dense(128, input_shape= (len(train_x[0]),), activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]),activation = 'softmax'))

optimizer = Adam(learning_rate=0.01)
model.compile(loss = 'categorical_crossentropy', optimizer = optimizer , metrics =['accuracy'])

hist=model.fit(np.array(train_x), np.array(train_y), epochs = 200, batch_size = 5, verbose = 1 )

model.save('chatbotmodel.h5',hist)

print("Done")

"""  
Bu kod, Keras kütüphanesi kullanılarak bir yapay sinir ağı oluşturulmasını ve eğitim verilerine uygun şekilde eğitilmesini sağlar.

Öncelikle, Sequential sınıfı kullanılarak bir yapay sinir ağı modeli oluşturuluyor. Model, Dense sınıfı kullanılarak birbirinden bağımsız nöronların katman katman eklenmesiyle inşa ediliyor. İlk katman input_shape parametresiyle belirleniyor ve modele eğitim verilerindeki her bir özelliğin girdi olarak verileceği boyut belirleniyor.

Model, ardından bir Dropout katmanı ekleyerek aşırı uyumun önlenmesini sağlıyor. Dropout katmanları, ağın ezberlemesini engellemek için rastgele birimlerin belirli bir yüzdesini devre dışı bırakarak çalışırlar.

Modelin diğer katmanları da benzer şekilde ekleniyor. Son katman, softmax aktivasyon fonksiyonu kullanılarak çok sınıflı sınıflandırma için uygulanıyor.

Optimizasyon algoritması olarak, Adam seçilmiş. Eğitim verilerine göre model, compile metodu kullanılarak derleniyor. Kayıp fonksiyonu olarak categorical_crossentropy, metrik olarak da doğruluk oranı (accuracy) seçiliyor.

Model, fit metodu kullanılarak eğitiliyor. Eğitim işlemi için, epochs sayısı belirleniyor ve eğitim örnekleri belirli bir batch_size değerinde ağa sunuluyor.

Son olarak, eğitilmiş model kaydediliyor ve eğitim tamamlanıyor.
"""