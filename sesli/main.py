import main5 as m


greetings = ["selam", "merhaba", "hey"]

hAU = ["nasılsın", "nasıl gidiyor", "napıyorsun", "neler yapıyorsun", "ne yapıyorsun"]

hAU_answer_bad=["kötüyüm", "igrencim","kötü hissediyorum" ]
hAU_answer_good=["iyiyim", "mükemmelim","iyi gidiyor" ]
hAU_answer_neut=["bilmiyorum", "idare eder" ]

while True:
    text = m.save_voice().lower()
    if any(word in text for word in greetings):
        for item in greetings:
            m.speak(item)
            break

    elif "bay bay" in text:
        m.speak("Kendine iyi bak!")
        break
    
    else:
        m.bot_cevap(text)
        