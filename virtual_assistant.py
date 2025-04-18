import whisper
import pyttsx3
import datetime
import sounddevice as sd
import scipy.io.wavfile as wav
import noisereduce as nr
import soundfile as sf

# Initialize Whisper model
model = whisper.load_model("base")

# Initialize TTS engine
engine = pyttsx3.init()

def listen():
    try:
        print("Listening...")
        # Record audio
        fs = 16000  # Sample rate
        duration = 5  # Duration in seconds
        print("Speak now...")
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        wav.write("temp.wav", fs, audio)

        # Reduce noise
        data, rate = sf.read("temp.wav")
        reduced_noise = nr.reduce_noise(y=data, sr=rate)
        sf.write("cleaned_audio.wav", reduced_noise, rate)

        # Transcribe the audio
        result = model.transcribe("cleaned_audio.wav")
        text = result["text"]
        print(f"You said: {text}")
        return text.lower()
    except Exception as e:
        print(f"Error: {e}")
        return None

def respond(text):
    if text:
        if "hello" in text:
            engine.say("Hello! How can I help you?")
        elif "time" in text:
            now = datetime.datetime.now()
            engine.say(f"The time is {now.strftime('%H:%M')}")
        elif "date" in text:
            today = datetime.date.today()
            engine.say(f"Today's date is {today.strftime('%B %d, %Y')}")
        else:
            engine.say("I didn't understand that.")
        engine.runAndWait()

while True:
    user_input = listen()
    if user_input and "hey assistant" in user_input:
        engine.say("Yes? How can I help you?")
        engine.runAndWait()
        user_input = listen()
        if user_input:
            respond(user_input)