from gtts import gTTS
import os
from generate_response import generate_response, recognize_speech  # Import recognize_speech

def text_to_speech(text):
    tts = gTTS(text=text, lang="en")
    tts.save("response.mp3")
    print("Playing response...")
    os.system("start response.mp3")  # For Windows, use 'mpg321' on Linux

if __name__ == "__main__":
    user_input = recognize_speech()  # Use recognize_speech instead of capture_audio
    if user_input:
        bot_reply = generate_response(user_input)
        text_to_speech(bot_reply)
