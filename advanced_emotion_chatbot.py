import speech_recognition as sr
import librosa
import numpy as np
import pyttsx3
import random
import csv
import os
import matplotlib.pyplot as plt

# ---------------- Setup ----------------
PHRASE_TIME_LIMIT = 8  # max time to listen for each turn
CSV_FILE = "stress_report.csv"

# Fixed baseline for all users
BASE_PITCH = 0.85
BASE_ENERGY = 0.02

# Ensure csv exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Pitch", "Energy", "Emotion", "Stress_Level", "Text"])

# Initialize TTS
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 160)
engine.setProperty('volume', 1.0)

def speak(text):
    print("🤖 Bot:", text)
    time.sleep(0.5)  # short delay before talking
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.5)

def record_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙 Speak something (3–5 sec)...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source, phrase_time_limit=5)
    with open("voice.wav", "wb") as f:
        f.write(audio.get_wav_data())
    return "voice.wav"

def extract_features(file):
    try:
        y, sr_rate = librosa.load(file, duration=3, offset=0.5)
        mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr_rate, n_mfcc=13).T, axis=0)
        chroma = np.mean(librosa.feature.chroma_stft(y=y, sr=sr_rate).T, axis=0)
        mel = np.mean(librosa.feature.melspectrogram(y=y, sr=sr_rate).T, axis=0)
        features = np.hstack([mfcc, chroma, mel])
        return features
    except Exception as e:
        print("Error extracting features:", e)
        return np.zeros(180)

def predict_emotion(features):
    emotions = ["happy", "sad", "angry", "neutral", "stressed"]
    return random.choice(emotions)

# Main loop
speak("Hey Swati, how are you feeling today?")

while True:
    try:
        audio_file = record_audio()
        features = extract_features(audio_file)
        emotion = predict_emotion(features)
        print(f"🎯 Detected Emotion: {emotion}")

        if emotion == "happy":
            speak("You sound cheerful! Keep smiling, Swati! 😄")
        elif emotion == "sad":
            speak("You sound a bit low. I’m here for you 💙")
        elif emotion == "angry":
            speak("It’s okay to feel angry sometimes. Take a deep breath.")
        elif emotion == "stressed":
            speak("I sense stress... maybe take a short break 🌿")
        else:
            speak("You sound calm and relaxed. That’s great!")

        speak("Would you like to continue talking?")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("🎧 Listening for reply...")
            audio = r.listen(source, phrase_time_limit=4)
            try:
                reply = r.recognize_google(audio)
                print("🗣 You said:", reply)
                if "no" in reply.lower() or "stop" in reply.lower():
                    speak("Okay, take care Swati 💙 Stay strong and positive!")
                    break
            except sr.UnknownValueError:
                speak("Sorry, I didn’t catch that.")
    except KeyboardInterrupt:
        speak("Goodbye Swati 💖")
        break