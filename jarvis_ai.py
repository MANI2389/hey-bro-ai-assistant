import tkinter as tk
from threading import Thread
import speech_recognition as sr
import pyttsx3
import ollama
import psutil
import webbrowser
import json
import requests
import os
import subprocess
import datetime
import pyautogui
import math
import random

# ---------------- GLOBAL ----------------
running=True

# ---------------- MEMORY ----------------
MEMORY_FILE="memory.json"

def load_memory():
    try:
        with open(MEMORY_FILE,"r") as f:
            return json.load(f)
    except:
        return {}

def save_memory(data):
    with open(MEMORY_FILE,"w") as f:
        json.dump(data,f)

memory=load_memory()

# ---------------- VOICE ----------------
engine=pyttsx3.init()
engine.setProperty('rate',170)

assistant_name="cro"

# ---------------- GUI ----------------

root=tk.Tk()
root.title("MANI'S ASSISTANT")
root.geometry("800x650")
root.configure(bg="black")

canvas=tk.Canvas(root,width=800,height=250,bg="black",highlightthickness=0)
canvas.pack()

bars=[]
for i in range(10):
    bar=canvas.create_rectangle(200+i*40,200,220+i*40,200,fill="cyan")
    bars.append(bar)

# ---------------- ANIMATION ----------------
angle=0

def animate():

    global angle

    canvas.delete("core")

    x=400
    y=120
    r=80

    for i in range(8):

        a=angle+i*45

        x1=x+r*math.cos(math.radians(a))
        y1=y+r*math.sin(math.radians(a))

        canvas.create_line(x,y,x1,y1,fill="cyan",width=2,tags="core")

    canvas.create_oval(x-40,y-40,x+40,y+40,outline="cyan",width=3,tags="core")

    angle+=5

    root.after(50,animate)

def animate_talking():

    for bar in bars:
        height=random.randint(120,200)
        canvas.coords(bar,canvas.coords(bar)[0],height,canvas.coords(bar)[2],200)

# ---------------- SPEAK ----------------
def speak(text):

    print(assistant_name + ":", text)

    output_box.insert(tk.END, f"{assistant_name}: {text}\n")
    output_box.see(tk.END)

    status_label.config(text="Speaking...")

    engine.say(text)
    engine.runAndWait()

    status_label.config(text="Waiting...")

# ---------------- LISTEN ----------------
def listen():

    r=sr.Recognizer()
    r.energy_threshold=300

    with sr.Microphone() as source:

        try:

            status_label.config(text="Listening...")

            r.adjust_for_ambient_noise(source,duration=0.5)

            audio=r.listen(source,timeout=5,phrase_time_limit=5)

            text=r.recognize_google(audio).lower()

            print("User:",text)

            output_box.insert(tk.END,f"You: {text}\n")
            output_box.see(tk.END)

            return text

        except:
            return ""

# ---------------- WAKE WORD ----------------
def wake_word_detect():

    r=sr.Recognizer()
    r.energy_threshold=300

    with sr.Microphone() as source:

        try:

            audio=r.listen(source,phrase_time_limit=3)

            text=r.recognize_google(audio).lower()

            print("Wake:",text)

            if "hey bro" in text:

                speak("yes boss cro is here")

                return True

        except:
            return False

    return False

# ---------------- AI ----------------
def ask_ai(question):

    response=ollama.chat(
        model="llama3",
        messages=[{"role":"user","content":question}]
    )

    return response["message"]["content"]

# ---------------- WEATHER ----------------
def get_weather(city):

    api="YOUR_API_KEY"

    url=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric"

    data=requests.get(url).json()

    temp=data["main"]["temp"]
    desc=data["weather"][0]["description"]

    return f"{city} temperature is {temp} degree with {desc}"

# ---------------- COMMAND SYSTEM ----------------
def run_command(cmd):

    global running
    global memory

    if "open youtube" in cmd:
        webbrowser.open("https://youtube.com")
        speak("Opening youtube")

    elif "open google" in cmd:
        webbrowser.open("https://google.com")
        speak("Opening google")

    elif "open notepad" in cmd:
        subprocess.Popen("notepad.exe")
        speak("Opening notepad")

    elif "open calculator" in cmd:
        subprocess.Popen("calc.exe")
        speak("Opening calculator")

    elif "open chrome" in cmd:
        subprocess.Popen("start chrome",shell=True)
        speak("Opening chrome")

    elif "open whatsapp" in cmd:
        webbrowser.open("https://web.whatsapp.com")

    elif "take screenshot" in cmd:

        file=f"screenshot_{datetime.datetime.now().strftime('%H%M%S')}.png"

        pyautogui.screenshot(file)

        speak("Screenshot saved")

    elif "time" in cmd:
        speak(datetime.datetime.now().strftime("%I:%M %p"))

    elif "date" in cmd:
        speak(datetime.datetime.now().strftime("%d %B %Y"))

    elif "weather in" in cmd:

        city=cmd.split("weather in")[-1]

        speak(get_weather(city))

    elif "cpu usage" in cmd:
        speak(str(psutil.cpu_percent())+" percent")

    elif "ram usage" in cmd:
        speak(str(psutil.virtual_memory().percent)+" percent")

    elif "remember" in cmd:

        try:

            data=cmd.replace("remember","").strip()

            key,value=data.split(" is ")

            memory[key.strip()]=value.strip()

            save_memory(memory)

            speak("I will remember that")

        except:
            speak("say remember something is something")

    elif cmd in memory:

        speak(memory[cmd])

    elif "stop" in cmd:

        speak("shutting down assistant")

        running=False

    else:

        try:

            answer=ask_ai(cmd)

            speak(answer[:300])

        except:
            speak("AI not available")

# ---------------- SYSTEM STATUS ----------------
def update_system():

    cpu=psutil.cpu_percent()
    ram=psutil.virtual_memory().percent

    try:
        battery=psutil.sensors_battery().percent
    except:
        battery="N/A"

    cpu_label.config(text=f"CPU: {cpu}%")
    ram_label.config(text=f"RAM: {ram}%")
    battery_label.config(text=f"Battery: {battery}%")

    root.after(2000,update_system)

# ---------------- MAIN LOOP ----------------
def jarvis_loop():

    global running

    speak("cro online")

    while running:

        wake=wake_word_detect()

        if wake:

            cmd=listen()

            if cmd!="":

                run_command(cmd)

# ---------------- START THREAD ----------------
def start_jarvis():

    t=Thread(target=jarvis_loop)

    t.daemon=True

    t.start()

# ---------------- GUI ----------------
title=tk.Label(root,text="MANI'S ASSISTANT",font=("Arial",28),fg="cyan",bg="black")
title.pack(pady=10)

status_label=tk.Label(root,text="System Ready",font=("Arial",14),fg="white",bg="black")
status_label.pack()

output_box=tk.Text(root,height=15,width=90,bg="black",fg="cyan")
output_box.pack(pady=10)

cpu_label=tk.Label(root,text="CPU:0%",fg="lime",bg="black")
cpu_label.pack()

ram_label=tk.Label(root,text="RAM:0%",fg="lime",bg="black")
ram_label.pack()

battery_label=tk.Label(root,text="Battery:0%",fg="lime",bg="black")
battery_label.pack()

start_button=tk.Button(root,text="Start Assistant",font=("Arial",14),command=start_jarvis)
start_button.pack(pady=20)

update_system()
animate()

root.mainloop()