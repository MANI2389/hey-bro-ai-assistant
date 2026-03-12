import tkinter as tk
from threading import Thread
import speech_recognition as sr
import pyttsx3
import ollama
import json
import psutil

engine = pyttsx3.init()
engine.setProperty("rate",170)

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        print("You:", command)
        return command.lower()
    except:
        return "none"


def ask_ai(question):

    response = ollama.chat(
        model='llama3',
        messages=[{"role": "user", "content": question}]
    )

    return response['message']['content']


def main_loop():

    speak("Jarvis started")

    while True:

        cmd = listen()

        if "hello" in cmd:
            speak("Hello bro")

        elif "stop" in cmd:
            speak("Goodbye bro")
            break

        else:
            answer = ask_ai(cmd)
            speak(answer[:200])


def start_jarvis():
    Thread(target=main_loop).start()


root = tk.Tk()
root.title("HEY BRO JARVIS")
root.geometry("500x300")
root.configure(bg="black")

title = tk.Label(
    root,
    text="HEY BRO JARVIS",
    font=("Arial",24),
    fg="cyan",
    bg="black"
)
title.pack(pady=20)

button = tk.Button(
    root,
    text="Start Jarvis",
    font=("Arial",16),
    command=start_jarvis
)
button.pack(pady=40)

root.mainloop()