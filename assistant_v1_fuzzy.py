import pandas as pd
from fuzzywuzzy import process
import speech_recognition as sr
import pyttsx3

# Sesli yanıt için motoru başlat
engine = pyttsx3.init()

# Türkçe sesi ayarlama
voices = engine.getProperty('voices')
for voice in voices:
    if 'tur' in voice.languages:  # Türkçe sesleri bul
        engine.setProperty('voice', voice.id)
        break

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Dinliyorum...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language='tr-TR')  # Türkçe için
            print("Kullanıcı: ", text)
            return text
        except sr.UnknownValueError:
            print("Anlayamadım, lütfen tekrar edin.")
            return None
        except sr.RequestError:
            print("Ses tanıma servisine ulaşılamıyor.")
            return None

# data.txt dosyasını oku
data_file = 'data.txt'
data = pd.read_csv(data_file, sep=':', header=None, names=['Soru', 'Cevap'], encoding='utf-8')

# Kullanıcıdan soru alma ve döngü
while True:
    speak("Merhaba ben senin 5. sınıf fen bilimleri asistanınım, sana hangi konuda yardımcı olabilirim. Çıkmak için 'çıkış' de.")

    user_question = listen()

    # Kullanıcı çıkış yapmak isterse döngüden çık
    if user_question and user_question.lower() == 'çıkış':
        speak("Görüşmek üzere!")
        print("Görüşmek üzere!")
        break

    # Benzer soruları bulma
    def find_similar_question(user_question, data):
        # Sadece soruları al
        questions = data['Soru'].tolist()

        # En benzer soruyu bul
        best_match = process.extractOne(user_question, questions)

        return best_match

    # Benzer soruyu bul
    similar_question = find_similar_question(user_question, data)

    if similar_question:
        matched_question = similar_question[0]
        matched_index = data[data['Soru'] == matched_question].index[0]
        answer = data['Cevap'][matched_index]

        # Benzerlik skoru kontrolü
        if similar_question[1] < 60:  # Eşik değer
            response = "Bu soru alakasız görünüyor. Lütfen fen bilimleri ile ilgili bir soru sorun."
            print(response)
            speak(response)
        else:
            response = f"Benzer Soru: {matched_question}. Cevap: {answer}"
            print(response)
            speak(response)
    else:
        response = "Benzer bir soru bulunamadı. Ben sadece 5. sınıf fen bilimleri asistanıyım, lütfen bana farklı sorular sorma, cevaplayamam."
        print(response)
        speak(response)