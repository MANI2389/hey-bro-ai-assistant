import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import ollama
import json
import speedtest


engine = pyttsx3.init()
engine.setProperty("rate",170)

def ask_ai(question):

    response = ollama.chat(
        model='llama3',
        messages=[
            {"role": "user", "content": question}
        ]
    )

    return response['message']['content']
import json

def load_memory():
    try:
        with open("memory.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_memory(memory):
    with open("memory.json", "w") as f:
        json.dump(memory, f)    

def speak(text):
    print("thambi:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        print("You:", command)
        return command.lower()
    except:
        return ""

speak("thambi started. Say Hey bro to activate.")
memory = load_memory()
def check_internet_speed():
    try:
        import speedtest
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download()/1_000_000
        upload = st.upload()/1_000_000
        return f"Download {download:.2f} Mbps Upload {upload:.2f} Mbps"
    except:
        return "Unable to check internet speed"

while True:

    wake = listen()

    if wake == "none":
        continue

    if "hey bro" in wake:
        speak("Yes bro, how can I help you")

        cmd = listen()
        print(cmd)

        if "open youtube" in cmd:
            webbrowser.open("https://youtube.com")
            speak("Opening YouTube")

        elif "open google" in cmd:
            webbrowser.open("https://google.com")
            speak("Opening Google")
        elif "clode google" in cmd:
            webbrowser.close("https://google.com")
            speak("clode Google")    

        elif "stop" in cmd:
            speak("Goodbye bro")
            break
        import webbrowser
        import pywhatkit
        import pyautogui
        import pyjokes
        import psutil
        import ctypes
        import speedtest
        import time
        
        

        if "search" in cmd:
            topic = cmd.replace("search", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={topic}")
            speak(f"Searching {topic}")

        elif "play" in cmd:
            song = cmd.replace("play", "").strip()
            speak(f"Playing {song}")
            pywhatkit.playonyt(song)
        elif "off" in cmd:
            speak("Stopping the video")
            pyautogui.hotkey('ctrl', 'w')             
        
        import os
        if "open chrome" in cmd:
            os.system("start chrome")
            speak("Opening Chrome")

        elif "open vs code" in cmd:
            os.system("code")
            speak("Opening Visual Studio Code")

        elif "open notepad" in cmd:
            os.system("notepad")
            speak("Opening Notepad")
        elif "open calculator" in cmd:
            os.system("calc")
            speak("Opening calculator")

        elif "open file explorer" in cmd:
            os.system("explorer")
            speak("Opening file explorer")    

        elif "time" in cmd:
            from datetime import datetime
            time = datetime.now().strftime("%H:%M")
            speak("Current time is " + time)
        elif "shutdown" in cmd:
            speak("Shutting down the system")
            os.system("shutdown /s /t 1")

        elif "restart" in cmd:
            speak("Restarting the system")
            os.system("shutdown /r /t 1") 

        elif "screenshot" in cmd:
            img = pyautogui.screenshot()
            img.save("screenshot.png")
            speak("Screenshot taken")
        elif "volume up" in cmd:
            pyautogui.press("volumeup")
            speak("Volume increased")

        elif "volume down" in cmd:
            pyautogui.press("volumedown")
            speak("Volume decreased")

        elif "mute" in cmd:
            pyautogui.press("volumemute")
            speak("Muted")  
        
        elif "joke" in cmd:
            joke = pyjokes.get_joke()
            speak(joke) 
        elif "weather" in cmd:
            webbrowser.open("https://www.google.com/search?q=weather")
            speak("Showing weather")  
        
        elif "battery" in cmd:
            battery = psutil.sensors_battery()
            percent = battery.percent
            speak(f"Battery is {percent} percent") 
        elif "lock computer" in cmd:
            speak("Locking your computer")
            ctypes.windll.user32.LockWorkStation()
        elif "internet speed" in cmd:
            speak("Checking internet speed")
            st = speedtest.Speedtest()

            download = st.download() / 1_000_000
            upload = st.upload() / 1_000_000

            speak(f"Download speed is {download:.2f} mbps")
            speak(f"Upload speed is {upload:.2f} mbps") 
        elif "open website" in cmd:
            site = cmd.replace("open website", "").strip()
            webbrowser.open(f"https://{site}.com")
            speak(f"Opening {site}")  
        elif "where is" in cmd:
            location = cmd.replace("where is", "").strip()
            webbrowser.open(f"https://www.google.com/maps/place/{location}")
            speak(f"Showing location of {location}")   
        elif "news" in cmd:
            webbrowser.open("https://news.google.com")
            speak("Here are the latest news")
        elif "send whatsapp message" in cmd:
            speak("Tell the phone number with country code")
            number = input("Enter number: ")

            speak("What message should I send")
            message = listen()
 
            pywhatkit.sendwhatmsg_instantly(number, message)

            speak("Message sent successfully")   
        elif "set reminder" in cmd:
            speak("What should I remind you")
            reminder = listen()

            speak("After how many seconds")
            seconds = int(input("Seconds: "))

            speak("Reminder set")
            time.sleep(seconds)

            speak(f"Reminder: {reminder}")  
        elif "start typing" in cmd:
            speak("Start speaking")

            while True:
                text = listen()

                if "stop typing" in text:
                    speak("Typing stopped")
                    break

                pyautogui.write(text + " ") 
        elif "sleep" in cmd:
           speak("Going to sleep. Say hey bro to wake me.")
           continue 
        elif "wake screen" in cmd:
           speak("Waking the screen")
           pyautogui.press("shift")

        elif "god" in cmd:

           speak("Ask me anything")

           question = listen()

           if question == "none":
              speak("I did not hear your question")
           else:
              answer = ask_ai(question)
              speak(answer)                                         
        elif "start ai mode" in cmd:

              speak("AI mode started. Ask me anything")

              while True:

                  question = listen()
                  if not question or question == "none":
                     continue
                  

                  if "stop ai" in question:
                      speak("Exiting AI mode")
                      break
                  answer = ask_ai(question)

                  print("AI:", answer)

                  speak(answer[:300])  # speak only first part

        elif "my name is" in cmd:

            name = cmd.replace("my name is", "").strip()

            memory["name"] = name

            save_memory(memory)

            speak(f"Nice to meet you {name}") 
        elif "what is my name" in cmd:

            name = memory.get("name")

            if name:
               speak(f"Your name is {name}")
            else:
               speak("I don't know your name yet") 
        

        elif "stop" in cmd:
             speak("Goodbye bro")
             break

        elif "who is" in cmd or "what is" in cmd:
            try:
               info = wikipedia.summary(cmd, 2)
               speak(info)
            except:
               speak("Sorry bro I could not find information")

        

             

