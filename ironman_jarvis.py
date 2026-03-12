import tkinter as tk
from threading import Thread
import speech_recognition as sr
import pyttsx3
import ollama
import psutil
import webbrowser
import json
import requests

# -------- GUI ROOT --------
root = tk.Tk()
root.title("Jarvis AI")
root.geometry("700x600")
root.configure(bg="black")

# -------- VOICE ENGINE --------
engine = pyttsx3.init('sapi5')
engine.setProperty("rate",170)

# -------- SYSTEM STATUS --------
def update_system():

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent

    try:
        battery = psutil.sensors_battery().percent
    except:
        battery = "N/A"

    cpu_label.config(text=f"CPU Usage: {cpu}%")
    ram_label.config(text=f"RAM Usage: {ram}%")
    battery_label.config(text=f"Battery: {battery}")

    root.after(2000, update_system)

# -------- SPEAK --------
def speak(text):

    output_box.insert(tk.END, "Jarvis: " + text + "\n")
    output_box.see(tk.END)

    engine.say(text)
    engine.runAndWait()

# -------- LISTEN --------
def listen():

    r = sr.Recognizer()

    with sr.Microphone() as source:

        status_label.config(text="🎤 Listening...")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)

        output_box.insert(tk.END, "You: " + command + "\n")

        return command.lower()

    except:

        return ""

# -------- WAKE WORD --------
def wake_word_detect():

    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Waiting for wake word...")
        audio = r.listen(source)

    try:

        text = r.recognize_google(audio).lower()

        if "hey bro" in text:

            speak("Yes boss how can I help")
            return True

    except:

        return False

# -------- AI --------
def ask_ai(question):

    response = ollama.chat(
        model='llama3',
        messages=[{"role":"user","content":question}]
    )

    return response['message']['content']

# -------- MEMORY --------
def load_memory():

    try:
        with open("memory.json","r") as f:
            return json.load(f)
    except:
        return {}

def save_memory(data):

    with open("memory.json","w") as f:
        json.dump(data,f)

# -------- WEATHER --------
def get_weather(city):

    api_key = "YOUR_API_KEY"

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    data = requests.get(url).json()

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    return f"The temperature in {city} is {temp} degree celsius with {desc}"

# -------- COMMAND --------
def run_command(cmd):

    memory = load_memory()

    if "my name is" in cmd:

        name = cmd.replace("my name is","").strip()

        memory["name"] = name

        save_memory(memory)

        speak("Okay I will remember that")

    elif "what is my name" in cmd:

        if "name" in memory:

            speak("Your name is " + memory["name"])

        else:

            speak("I don't know your name yet")

    elif "open youtube" in cmd:

        speak("Opening youtube")

        webbrowser.open("https://youtube.com")

    elif "open google" in cmd:

        speak("Opening google")

        webbrowser.open("https://google.com")

    elif "weather in" in cmd:

        city = cmd.split("weather in")[-1].strip()

        report = get_weather(city)

        speak(report)

    else:

        answer = ask_ai(cmd)

        speak(answer[:200])
    

# -------- MAIN LOOP --------
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

# -------- START BUTTON --------
def start_jarvis():

    t = Thread(target=jarvis_loop)

    t.start()

# -------- GUI --------
title = tk.Label(
    root,
    text="IRON MAN JARVIS",
    font=("Arial",28),
    fg="cyan",
    bg="black"
)
title.pack(pady=10)

status_label = tk.Label(
    root,
    text="System Ready",
    font=("Arial",14),
    fg="white",
    bg="black"
)
status_label.pack()

output_box = tk.Text(
    root,
    height=20,
    width=80,
    bg="black",
    fg="cyan",
    insertbackground="white"
)
output_box.pack(pady=20)

cpu_label = tk.Label(root,text="CPU:0%",fg="lime",bg="black")
cpu_label.pack()

ram_label = tk.Label(root,text="RAM:0%",fg="lime",bg="black")
ram_label.pack()

battery_label = tk.Label(root,text="Battery:0%",fg="lime",bg="black")
battery_label.pack()

start_button = tk.Button(
    root,
    text="Start Jarvis",
    font=("Arial",14),
    command=start_jarvis
)
start_button.pack(pady=20)

update_system()

root.mainloop()