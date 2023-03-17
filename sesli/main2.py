import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('averaged_perceptron_tagger')
nltk.download('vader_lexicon')

def kelime_lemmatize_et(kelime):
    lemmatizer = WordNetLemmatizer()
    lemma = lemmatizer.lemmatize(kelime, get_wordnet_pos(kelime))
    return lemma

def get_wordnet_pos(kelime):
    tag = nltk.pos_tag([kelime])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

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
    # sid = SentimentIntensityAnalyzer()

    # duygu = sid.polarity_scores(mesaj)['compound']

    # if duygu > 0.5:
    #     cevap = "Sevindim, senin için iyi bir gün olmuş demektir."
    # elif duygu < -0.5:
    #     cevap = "Üzgünüm, umarım daha iyi bir gün geçirirsin."
    # else:
    #     cevap = ""

    # kelimeler = word_tokenize(mesaj)
    # kelimeler = [kelime_lemmatize_et(kelime) for kelime in kelimeler]

    # for soru in sorular:
    #     if soru in mesaj:
    #         cevap += cevaplar[sorular.index(soru)]
    #         break

    # if not cevap:
    #     cevap = "Anlamadım, başka bir şeyler söyleyebilir misin?"

    # return cevap
    sid = SentimentIntensityAnalyzer()

    mesaj_duygusu = sid.polarity_scores(mesaj)

    if mesaj_duygusu['compound'] >= 0.05:
        cevap = cevaplar[0]
    elif mesaj_duygusu['compound'] <= -0.05:
        cevap = cevaplar[1]
    else:
        cevap = cevaplar[2]

    kelimeler = word_tokenize(mesaj)
    kelimeler = [kelime.lower() for kelime in kelimeler]

    yeni_kelimeler = []
    for kelime in kelimeler:
        if kelime.isalnum():
            yeni_kelimeler.append(kelime_lemmatize_et(kelime))

    if any(kelime in yeni_kelimeler for kelime in ['mutlu', 'sevinçli', 'keyifli', 'güzel']):
        cevap = cevaplar[0]
    elif any(kelime in yeni_kelimeler for kelime in ['üzgün', 'kötü', 'moralli']):
        cevap = cevaplar[1]

    return cevap




