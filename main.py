import pyttsx3
import os
import requests
import smtplib
import json
import wikipedia
import datetime
import webbrowser
import speech_recognition as sr

SECRETS = json.load(open("./SECRETS.json"))
Google_pass = SECRETS['google']['password']
Google_email = SECRETS['google']['email']
news_api_key = SECRETS["newsapi"]
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("I am Jarvis Sir. Please tell me how may I help you")   


def fetchNews():
    url = 'http://newsapi.org/v2/top-headlines?apiKey={}'.format(news_api_key)
    news = requests.get(url).text
    c = 0 
    news_dict = json.loads(news)
    arts = news_dict['articles']
    number  = news_dict['totalResults']
    speak("Lets begin with the first news")
    for article in arts:
        c = c + 1
        print(article['title'])
        speak(article['title'])
        print(article['description'])
        speak(article['description'])
        print(article['url'])
        print()
        speak("Refer the following link for more")
        if c == number-1:
            speak("That's it for today")
        else:
            speak("Moving on to the next news please Listen Carefully")

    speak("Thanks for listening...")

def speak(msg):
    engine = pyttsx3.init()
    engine.say(msg)
    engine.runAndWait()


def sendEmail(reciever, message):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()   
    s.login(Google_email, Google_pass) 
    s.sendmail(Google_email, reciever, message)
    s.quit() 


##########################################################


def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        audio = r.listen(source)
        print("Listening.....")

    try:
        print(r.recognize_google(audio))
        return r.recognize_google(audio)

    except:
        print("Could not understand what you told")
        return "Could not understand what you told"


##########################################################


def searchWiki(query):
    result = wikipedia.summary(query, sentences=5)
    print(result)
    return result

if __name__ == "__main__":

    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = searchWiki(query)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")   


        elif 'play music' in query:
            os.startfile("/usr/bin/spotify")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            os.system("code")

        elif 'email' in query:
            try:
                speak("To whom ?")
                to = input()   
                speak("What should I say?")
                content = input()
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Email was not able to be sent") 
        
        elif "news" in query:
            fetchNews()
	        

