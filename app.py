from flask import Flask, render_template, jsonify
import speech_recognition as sr
import pyttsx3
import requests

# Initialize Flask app
app = Flask(__name__)

# Hugging Face API configuration
HUGGINGFACE_API_KEY = ""  # Replace with your Hugging Face API key
API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

# Function to generate AI response
def generate_response(user_input):
    prompt = f"Conversation between a user and an AI assistant. The user says: '{user_input}'. The AI assistant responds:"
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 50,
            "temperature": 0.9,
            "top_k": 50,
            "top_p": 0.95
        }
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        generated_text = response.json()[0]['generated_text']
        return generated_text.replace(prompt, "").strip()
    else:
        return f"Error: {response.json().get('error', 'Unknown error')}"

# Function to convert text to speech
def text_to_speech(bot_reply):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Adjust speed
    engine.setProperty('volume', 1.0)  # Set volume
    engine.say(bot_reply)
    engine.runAndWait()

# Speech-to-text route
@app.route("/speak", methods=["POST"])
def speak():
    try:
        # Recognize speech
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5)  # 5-second timeout
            user_input = recognizer.recognize_google(audio)
            print(f"You said: {user_input}")

        # Generate response
        bot_reply = generate_response(user_input)
        print(f"Bot reply: {bot_reply}")

        # Speak response
        text_to_speech(bot_reply)

        return jsonify({"user_input": user_input, "bot_reply": bot_reply})

    except sr.UnknownValueError:
        return jsonify({"error": "Sorry, I couldn't understand that."})
    except sr.RequestError as e:
        return jsonify({"error": f"Speech recognition error: {e}"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
