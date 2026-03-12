import tkinter as tk
from threading import Thread
import speech_recognition as sr
import pyttsx3
import psutil
import webbrowser
import json
import requests
import os
import pyautogui
import datetime
import math

# ---------------- AI MODE ----------------
AI_MODE = True

# ---------------- GUI ----------------
root = tk.Tk()
root.title("IRON MAN JARVIS")
root.geometry("900x700")
root.configure(bg="black")

canvas = tk.Canvas(root,bg="black",highlightthickness=0)
canvas.pack(fill="both",expand=True)

# ---------------- VOICE ENGINE ----------------
engine = pyttsx3.init('sapi5')
engine.setProperty("rate",170)

# ---------------- TEXT OUTPUT ----------------
output_box = tk.Text(root,height=10,bg="black",fg="cyan",insertbackground="white")
output_box.pack()

# ---------------- SYSTEM LABELS ----------------
cpu_label = tk.Label(root,text="CPU:0%",fg="cyan",bg="black")
cpu_label.pack()

ram_label = tk.Label(root,text="RAM:0%",fg="cyan",bg="black")
ram_label.pack()

battery_label = tk.Label(root,text="Battery:0%",fg="cyan",bg="black")
battery_label.pack()

# ---------------- SPEAK ----------------
def speak(text):

    output_box.insert(tk.END,"Jarvis: "+text+"\n")
    output_box.see(tk.END)

    engine.say(text)
    engine.runAndWait()

# ---------------- LISTEN ----------------
def listen():

    r = sr.Recognizer()

    with sr.Microphone() as source:

        try:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source,timeout=5)
            command = r.recognize_google(audio)

            output_box.insert(tk.END,"You: "+command+"\n")

            return command.lower()

        except:
            return ""

# ---------------- SYSTEM STATUS ----------------
def update_system():

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent

    try:
        battery = psutil.sensors_battery().percent
    except:
        battery = "N/A"

    cpu_label.config(text=f"CPU: {cpu}%")
    ram_label.config(text=f"RAM: {ram}%")
    battery_label.config(text=f"Battery: {battery}%")

    root.after(2000,update_system)

# ---------------- MEMORY ----------------
def load_memory():

    try:
        with open("memory.json","r") as f:
            return json.load(f)
    except:
        return {}

def save_memory(data):

    with open("memory.json","w") as f:
        json.dump(data,f)

# ---------------- WEATHER ----------------
def get_weather(city):

    api = "YOUR_API_KEY"

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric"

    data = requests.get(url).json()

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    return f"{city} temperature is {temp} degree with {desc}"

# ---------------- COMMAND SYSTEM ----------------
def run_command(cmd):

    memory = load_memory()

    if "open youtube" in cmd:

        speak("Opening youtube")
        webbrowser.open("https://youtube.com")

    elif "open google" in cmd:

        speak("Opening google")
        webbrowser.open("https://google.com")

    elif "open notepad" in cmd:

        os.system("notepad")
        speak("Opening notepad")

    elif "open calculator" in cmd:

        os.system("calc")
        speak("Opening calculator")

    elif "shutdown computer" in cmd:

        speak("Shutting down")
        os.system("shutdown /s /t 1")

    elif "restart computer" in cmd:

        speak("Restarting computer")
        os.system("shutdown /r /t 1")

    elif "take screenshot" in cmd:

        file = f"screenshot_{datetime.datetime.now().strftime('%H%M%S')}.png"
        pyautogui.screenshot(file)

        speak("Screenshot saved")

    elif "time" in cmd:

        time = datetime.datetime.now().strftime("%I:%M %p")
        speak("Current time is "+time)

    elif "date" in cmd:

        date = datetime.datetime.now().strftime("%d %B %Y")
        speak("Today is "+date)

    elif "search" in cmd:

        q = cmd.replace("search","")
        webbrowser.open(f"https://google.com/search?q={q}")

        speak("Searching "+q)

    elif "weather in" in cmd:

        city = cmd.split("weather in")[-1]
        report = get_weather(city)

        speak(report)

    elif "my name is" in cmd:

        name = cmd.replace("my name is","")
        memory["name"] = name
        save_memory(memory)

        speak("Okay I will remember")

    elif "what is my name" in cmd:

        if "name" in memory:
            speak("Your name is "+memory["name"])
        else:
            speak("I don't know your name")

    else:

        speak("Command not recognized")

# ---------------- WAKE WORD ----------------
def wake_word_detect():

    r = sr.Recognizer()

    with sr.Microphone() as source:

        try:
            audio = r.listen(source)
            text = r.recognize_google(audio).lower()

            if "hey bro" in text:

                speak("Yes boss")

                return True

        except:
            pass

    return False

# ---------------- JARVIS LOOP ----------------
def jarvis_loop():

    speak("Jarvis online")

    while True:

        wake = wake_word_detect()

        if wake:

            cmd = listen()

            if "stop jarvis" in cmd:

                speak("Shutting down")
                break

            run_command(cmd)

# ---------------- START ----------------
def start_jarvis():

    t = Thread(target=jarvis_loop)
    t.start()

# ---------------- HOLOGRAM CORE ----------------
angle = 0

def animate():

    global angle

    canvas.delete("core")

    x = 450
    y = 300
    r = 120

    for i in range(8):

        a = angle + i*45

        x1 = x + r * math.cos(math.radians(a))
        y1 = y + r * math.sin(math.radians(a))

        canvas.create_line(x,y,x1,y1,fill="cyan",width=2,tags="core")

    canvas.create_oval(x-60,y-60,x+60,y+60,outline="cyan",width=3,tags="core")

    angle += 5

    root.after(50,animate)

# ---------------- START BUTTON ----------------
start_button = tk.Button(root,text="Start Jarvis",font=("Arial",16),command=start_jarvis)
start_button.pack(pady=10)

# ---------------- START SYSTEM ----------------
animate()
update_system()

root.mainloop()