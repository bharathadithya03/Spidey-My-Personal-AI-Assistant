import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import os
import sys
import webbrowser

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice

def talk(text):
    print("Spidey:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        try:
            audio = r.listen(source, timeout=5)
            command = r.recognize_google(audio).lower()
            print("Heard:", command)
            return command
        except sr.UnknownValueError:
            talk("Couldn't hear you. Please type your command.")
            return input("Type here: ").lower()
        except sr.WaitTimeoutError:
            talk("Mic was silent. Please type your command.")
            return input("Type here: ").lower()
        except Exception:
            talk("Mic or internet issue. Please type your command.")
            return input("Type here: ").lower()

def handle_command(command):
    command = command.lower()

    if "play" in command and "song" in command:
        song = command.replace("play", "").replace("song", "").strip()
        if song:
            talk(f"Playing {song} on YouTube.")
            pywhatkit.playonyt(song)
        else:
            talk("What song should I play?")

    elif "what's the time now" in command or "current time" in command:
        now = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"Current time is {now}.")

    elif "what's today's date" in command or "current date" in command:
        today = datetime.datetime.now().strftime('%A, %d %B %Y')
        talk(f"Today is {today}.")

    elif "tell me a joke" in command or "joke" in command:
        talk(pyjokes.get_joke())

    elif "tell me about bharath adithya" in command or "tell me about bharat" in command:
        talk("My boss who built me. He is a B.Tech final year student at Ideal Institute of Technology, Kakinada, specializing in Computer Science with Artificial Intelligence and Machine Learning.")

    elif any(keyword in command for keyword in ["search about","who is ","what is", "how", "define"]):
        topic = command
        for prefix in ["search about", "what is", "how", "define", "who is "]:
            topic = topic.replace(prefix, "")
        topic = topic.strip()
        if topic:
            try:
                summary = wikipedia.summary(topic, sentences=2)
                talk(summary)
            except:
                talk("Sorry Boss, I couldn't find that on Wikipedia.")
        else:
            talk("What should I search about?")

    elif "open" in command:
        site = command.replace("open", "").strip().lower().replace(" ", "")
        if site == "youtube":
            url = "https://www.youtube.com"
        elif site == "github":
            url = "https://www.github.com"
        elif site == "linkedin":
            url = "https://www.linkedin.com"
        elif site == "whatsappweb":
            url = "https://web.whatsapp.com"
        else:
            if "." not in site:
                site += ".com"
            url = f"https://www.{site}"
        talk(f"Opening {site}")
        webbrowser.open(url)

    elif command in ["exit", "stop", "terminate", "bye"]:
        talk("Spidey signing off, see you Boss.")
        sys.exit()

    else:
        talk("Sorry Boss, I didn't understand that. Try asking me to open a website or tell you something.")

def spidey_loop():
    talk("Hey Boss, I’m Spidey – your AI Assistant is ready.")

    while True:
        command = listen()
        if command:
            handle_command(command)

            # Ask whether to continue or exit
            talk("Do you want me to listen again or exit?")
            response = listen()
            if any(x in response for x in ["exit", "stop", "terminate", "bye", "no"]):
                talk("Spidey signing off, see you Boss.")
                break
            elif any(x in response for x in ["yes", "again", "listen", "continue"]):
                continue
            else:
                talk("I'll assume you want me to continue.")
        else:
            talk("Didn't catch anything. Try again.")

# Start the Assistant
if __name__ == "__main__":
    spidey_loop()
