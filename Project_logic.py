# Project_logic.py

import speech_recognition as sr
import re
from gtts import gTTS
import os
import pywhatkit
from datetime import datetime, timedelta
import time
import pygame
from word2number import w2n
from hugchat import hugchat
from hugchat.login import Login
import threading
import queue
import Plot_a_graph

##EMAIL = "priyanshupratik07@gmail.com"
##PASSWD = "@eAL&^mN/2FA.yi"
##sign = Login(EMAIL, PASSWD)
##cookies = sign.login()
##chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

output_queue = queue.Queue()

def clean_for_speech(text):
    return (
        text.replace("*", "")
            .replace("_", "")
            .replace("'", "")
            .replace('"', "")
            .replace("`", "")
    )

def print_gui(text, source="bot"):
    output_queue.put((text, source))

def record_voice():
    microphone = sr.Recognizer()
    with sr.Microphone() as live_phone:
        microphone.adjust_for_ambient_noise(live_phone)
        print_gui("I'm trying to hear you:", source="bot")
        audio = microphone.listen(live_phone)
        try:
            phrase = microphone.recognize_google(audio, language='en')
            print_gui(phrase, source="user")
            return phrase
        except sr.UnknownValueError:
            return "I didn't understand what you said"
        except sr.RequestError:
            return "Could not request results, check your network connection"

def speak(text):
    speech = gTTS(text=text, lang='en', slow=False)
    timestamp = int(time.time())
    filename = f"voice_{timestamp}.mp3"
    speech.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue

    pygame.mixer.music.unload()
    os.remove(filename)

def send_whatsapp_message():
    speak("Please provide the phone number of the receiver, including country code.")
    phone_number = record_voice().replace("plus", "+")
    print_gui(f"Receiver's phone number: {phone_number}")

    speak("Now, please provide the message you want to send.")
    message = record_voice()
    print_gui(f"Message to send: {message}")

    speak("By how many minutes from now would you like to schedule the message?")
    minutes_str = record_voice()

    try:
        minutes_ahead = int(minutes_str)
    except ValueError:
        try:
            minutes_ahead = w2n.word_to_num(minutes_str)
        except ValueError:
            minutes_ahead = 2
            speak("I couldn't understand the minutes, setting it to 2 minute.")

    now = datetime.now()
    send_time = now + timedelta(minutes=minutes_ahead)
    hour, minute = send_time.hour, send_time.minute

    speak(f"Sending message: '{message}' to {phone_number} at {hour}:{minute}.")
    pywhatkit.sendwhatmsg(phone_number, message, hour, minute)
    speak("Your message has been scheduled and sent.")

def play_YouTube_video():
    speak("Which YouTube video do you want me to play?")
    Title = record_voice()
    if Title == "I didn't understand what you said":
        print_gui("I could not catch that. Please try again later")
    else:
        pywhatkit.playonyt(Title)

def Playing_games():
    speak("Which game would you like to play, out of these choices")
    print_gui("""
You only have limited games on this device:
What would you like to play: 
    1) Snake game
    2) Shooting in space
    3) Hangman
""")
    user_input = record_voice()

    if "snakes" in user_input.lower() or "snake" in user_input.lower():
        os.system("Snakes.py")
    elif "space" in user_input.lower() or "shooting" in user_input.lower() or "shooter" in user_input.lower():
        os.system("shooting_game.py")
    elif "hangman" in user_input.lower() or "hang" in user_input.lower() or "man" in user_input.lower():
        os.system("Hangman_GUI_v2.py")
    else:
        speak("Sorry, I didn't understand that choice. Please try again.")

def Hugchat_LLM():
    pass
##    speak("Okay! Ask your question!")
##    prompt = record_voice()
##    print_gui(f"Your prompt was: {prompt}", source="user")
##    response = chatbot.chat(prompt)
##    print_gui("thinking...and...searching...")
##    response_text = getattr(response, 'text', "Sorry, I couldn't get a valid response from the chatbot.")
##    clean_text = clean_for_speech(response_text)
##    print_gui(clean_text)
##    speak(clean_text)

def main():
    speak("Say the task name, you want me to perform: ")
    print_gui("""
What do you want me to perform?
    1) Send a WhatsApp message to a mobile number
    2) Play a certain YouTube video
    3) Play a certain game
    4) Visualise a graph/function
    5) Ask a general question
""")
    user_input = record_voice()

    if "whatsapp" in user_input.lower():
        send_whatsapp_message()
    elif "youtube" in user_input.lower():
        play_YouTube_video()
    elif "game" in user_input.lower():
        Playing_games()
    elif "question" in user_input.lower():
        Hugchat_LLM()
    elif "graph" in user_input.lower() or "function" in user_input.lower() or "visualise" in user_input.lower():
        Plot_a_graph.main()
    else:
        pass
##        print_gui(f"Your prompt was: {user_input}", source="user")
##        response = chatbot.chat(user_input)
##        print_gui("thinking...and...searching...")
##        response_text = getattr(response, 'text', "Sorry, I couldn't get a valid response from the chatbot.")
##        clean_text = clean_for_speech(response_text)
##        print_gui(clean_text)
##        speak(clean_text)

def run_main_threaded():
    threading.Thread(target=main, daemon=True).start()
