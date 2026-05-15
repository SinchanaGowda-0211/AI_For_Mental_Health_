import asyncio
import speech_recognition as sr
import librosa
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
import edge_tts
import os

# -------------------- Load the model --------------------
try:
    emotion_model = joblib.load('emotion_model.joblib')
except:
    emotion_model = None
    print("⚠️ Emotion model not found — using default 'neutral' emotion.")

# -------------------- Record Audio --------------------
def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Speak something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    return audio

# -------------------- Extract Features --------------------
def extract_features(audio_data):
    y = np.array(audio_data.get_array_of_samples(), dtype=np.float32)
    sr_rate = audio_data.sample_rate
    mfccs = librosa.feature.mfcc(y=y, sr=sr_rate, n_mfcc=13)
    return np.mean(mfccs.T, axis=0).reshape(1, -1)

# -------------------- Predict Emotion --------------------
def recognize_emotion(audio_data):
    if emotion_model is None:
        return "neutral"
    features = extract_features(audio_data)
    features = StandardScaler().fit_transform(features)
    emotion = emotion_model.predict(features)[0]
    return emotion

# -------------------- Speak Back --------------------
async def speak_text(text):
    communicate = edge_tts.Communicate(text, voice="en-US-JennyNeural")
    await communicate.stream_async()

def talk(text):
    asyncio.run(speak_text(text))

# -------------------- Main Chat Loop --------------------
if __name__ == "__main__":
    audio_file = record_audio()
    emotion = recognize_emotion(audio_file)
    print(f"🧠 Detected Emotion: {emotion}")

    reply = f"I can sense that you sound {emotion}. How are you feeling today?"
    print("💬 Bot:", reply)
    talk(reply)
