from flask import Flask, render_template, request, jsonify
import threading
import datetime
import os
import webbrowser
import wikipedia
import speech_recognition as sr
import pyttsx3
from MARK1 import *
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('web.html')

@app.route('/assistant', methods=['POST'])
def assistant():
    user_input = request.json.get("message")
    if user_input:
        response = handle_user_input(user_input)
        return jsonify({"response": response})
    return jsonify({"response": "Sorry, I didn't understand that."})

def handle_user_input(query):
    query = query.lower()
    if query == "cut":
        return "Exiting..."

    if "movie" in query or "tv show" in query:
        title_query = query.replace("movie", "").replace("tv show", "").strip()
        movie_info = get_movie_info(title_query)
        return movie_info

    elif "ask me a trivia question" in query or "ask me a question" in query:
        question, correct_answer, all_answers = get_trivia_question()
        if question:
            options = '\n'.join([f"Option {i + 1}: {answer}" for i, answer in enumerate(all_answers)])
            return f"Here's a trivia question for you:\n{question}\n{options}"
        else:
            return "Sorry, I couldn't fetch a trivia question at the moment."

    elif "how are you" in query:
        return "I'm fine sir, how can I help you?"
    elif "thank you" in query:
        return "You're welcome! If you have any more questions or need further assistance, feel free to ask. I'm here to help!"
    elif "hello" in query or "hi" in query:
        return "Hello! How can I assist you today?"
    elif "open amazon" in query:
        webbrowser.open("https://www.amazon.com")
        return "Opening Amazon..."
    elif "open flipkart" in query:
        webbrowser.open("https://www.flipkart.com/")
        return "Opening Flipkart..."
    elif "python" in query:
        webbrowser.open("https://www.codewithharry.com/tutorial/python/")
        webbrowser.open("https://www.youtube.com/results?search_query=python+playlist")
        return "Opening python related notes and videos..."
    elif "html" in query:
        webbrowser.open("https://www.codewithharry.com/tutorial/html-home/")
        webbrowser.open("https://www.youtube.com/results?search_query=html+playlist")
        return "Opening html related notes and videos.."
    elif "css" in query:
        webbrowser.open("https://www.codewithharry.com/tutorial/css-home/")
        webbrowser.open("https://www.youtube.com/results?search_query=css+playlist")
        return "Opening css related notes and videos..."
    elif "javascript" in query or "js" in query:
        webbrowser.open("https://www.codewithharry.com/tutorial/js/")
        webbrowser.open("https://www.youtube.com/results?search_query=javascript+playlist")
        return "Opening Javascript related notes and videos..."
    elif "c programming" in query:
        webbrowser.open("https://www.codewithharry.com/tutorial/c/")
        webbrowser.open("https://www.youtube.com/results?search_query=c+playlist")
        return "Opening C related notes and videos..."
    elif "java" in query:
        webbrowser.open("https://www.codewithharry.com/tutorial/java/")
        webbrowser.open("https://www.youtube.com/results?search_query=java+playlist")
        return "Opening java related notes and videos..."
    elif "web development" in query or "web developer" in query or "web programming" in query:
        webbrowser.open("https://www.youtube.com/results?search_query=web+development+playlist")
        return "Opening web development related videos..."
    elif "front end" in query:
        webbrowser.open("https://www.codewithharry.com/tutorial/html-home/")
        webbrowser.open("https://www.codewithharry.com/tutorial/css-home/")
        webbrowser.open("https://www.codewithharry.com/tutorial/js/")
        webbrowser.open("https://www.codewithharry.com/tutorial/react-home/")
        webbrowser.open("https://www.geeksforgeeks.org/bootstrap/")
        webbrowser.open("https://www.youtube.com/results?search_query=front+end+web+development+full+course+playlist")
        return "Opening front end related notes and videos.."
    elif "back end" in query:
        webbrowser.open("https://www.codewithharry.com/tutorial/php/")
        webbrowser.open("https://www.codewithharry.com/blogpost/mysql-cheatsheet/")
        webbrowser.open("https://www.codewithharry.com/blogpost/django-cheatsheet/")
        webbrowser.open("https://www.codewithharry.com/blogpost/flask-cheatsheet/")
        return "Opening back end end related notes..."
    
    elif "cricket score" in query:
        webbrowser.open("https://www.espncricinfo.com")
        return "Opening espn for cricket score...."
    elif "anime" in query:
        webbrowser.open("https://hianime.to/home")
        return "Opening anime boss, enjoy watching it..."
    elif "sports" in query:
        webbrowser.open("https://www.espn.com")
        return "Opening espn..."
    elif "health" in query:
        webbrowser.open("https://www.webmd.com")
        return "Opening health related website"

    elif "tell me a fact" in query or "interesting fact" in query:
        fact = get_random_fact()
        if fact:
            return f"Here's an interesting fact for you: {fact}"
        else:
            return "Sorry, I couldn't fetch a random fact at the moment."

    elif "who are you" in query:
        return "Sir I am Jarvis personal assistant"

    elif "open youtube" in query:
        webbrowser.open("https://www.youtube.com/")
        return "Opening YouTube..."

    elif "learning mode" in query:
        information = learning_mode()
        return f"Entered learning mode. {information}"

    elif "open video" in query:
        webbrowser.open("https://www.youtube.com/results?search_query=" + query.replace("open video", "").strip())
        return "Searching for the video on YouTube..."

    elif 'news' in query:
        category = 'general'
        country = 'us'
        news = get_news(category='general',country='in')
        return news if news else "Unable to fetch news at the moment."

    elif "motivate me" in query:
        quote = get_motivational_quote()
        return quote

    elif "tell me a joke" in query:
        joke = get_joke()
        return joke

    elif "set alarm" in query:
        time = query.replace("set alarm", "").strip()
        threading.Thread(target=set_alarm, args=(time,)).start()
        return f"Alarm set for {time}."

    elif "open spotify" in query:
        webbrowser.open("https://open.spotify.com/")
        return "Opening Spotify..."

    elif "wikipedia" in query or "information about" in query or "details about" in query:
        results = wikipedia.summary(query.replace("wikipedia", ""), sentences=3)
        return f"According to Wikipedia: {results}"

    elif "exchange rate" in query:
        rates = get_exchange_rate()
        return rates if rates else "Unable to fetch exchange rates at the moment."

    elif 'reminder' in query:
        reminder = query.replace("reminder", "").strip()
        threading.Thread(target=set_reminder, args=(reminder,)).start()
        return f"Reminder set for: {reminder}"

    elif "open chat gpt" in query:
        webbrowser.open("https://chat.openai.com/")
        return "Opening Chat GPT..."

    elif "open google" in query:
        webbrowser.open('https://www.google.co.in/')
        return "Opening Google..."

    elif ("weather" in query) or ("temperature" in query):
        city_name = query.replace("weather", "").replace("temperature", "").strip()
        weather_info = get_weather(city_name)
        return weather_info if weather_info else "Unable to fetch weather information at the moment."

    elif "coding videos" in query:
        coding_channels = [
            "https://www.youtube.com/@CodeWithHarry",
            "https://www.youtube.com/@ApnaCollegeOfficial",
            "https://www.youtube.com/@edurekaIN",
            "https://www.youtube.com/@JennyslecturesCSIT",
            "https://www.youtube.com/@LukeBarousse"
        ]
        for channel in coding_channels:
            webbrowser.open(channel)
        return "Suggesting coding videos..."

    elif "play music" in query:
        music_file = "C:/Users/Aryan/Music/SawanoHiroyuki_nZk_XAI_-_DARK_ARIA_LV2_(Hydr0.org).mp3"
        os.startfile(music_file)
        return "Playing music..."

    elif "the time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        return f"Sir, the time is {strTime}"

    elif "goodbye" in query or "get lost" in query or "bye" in query or "shut down" in query:
        return "Thanks for using me boss, have a good day"

    return "Sorry, I didn't understand that."

def get_news(category="general", country="in"):
    api_key = "65d616f9aac6470791682b979ff81043"
    url = f"https://newsapi.org/v2/top-headlines?category={category}&country={country}&apiKey={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        news_data = response.json()
        articles = news_data.get('articles', [])
        headlines = [f"{article['title']} - {article['description']}" for article in articles[:5]]
        return "\n".join(headlines)
    else:
        return "Failed to fetch news. Please try again later."


def fetch_topic_information(subject, topic):
    try:
        result = wikipedia.summary(f"{subject} {topic}", sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        return "There are multiple results for your query. Please be more specific."
    except wikipedia.exceptions.PageError:
        return "No results found for your query."

def learning_mode():
    speak("Welcome to learning mode. Please tell me the subject.")
    subject = takeCommand().lower()
    if subject == "none":
        speak("Sorry, I didn't get that. Please try again.")
        return "Sorry, I didn't get that. Please try again."

    speak(f"You chose {subject}. Now, please tell me the topic you want to learn about.")
    topic = takeCommand().lower()
    if topic == "none":
        speak("Sorry, I didn't get that. Please try again.")
        return "Sorry, I didn't get that. Please try again."

    speak(f"Searching for information about {topic} in {subject}.")
    information = fetch_topic_information(subject, topic)
    print(information)
    speak(information)
    return information




def get_exchange_rate():
    api_key = "f4787668fecc7c45daaf5fa8"
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
    response = requests.get(url)
    if response.status_code == 200:
        rate_data = response.json()
        rates = rate_data.get('conversion_rates', {})
        rate_info = [f"1 USD = {rate} {currency}" for currency, rate in rates.items() if currency in ['EUR', 'GBP', 'INR']]
        return "\n".join(rate_info)
    return None

def get_weather(city_name):
    api_key = "deb91b8f90b414c9e81bf84889fbe9f7"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        main = weather_data.get('main', {})
        weather = weather_data.get('weather', [{}])[0]
        temp = main.get('temp', 'N/A')
        desc = weather.get('description', 'N/A')
        return f"The current temperature in {city_name} is {temp}°C with {desc}."
    return None

def set_alarm(time_str):
    alarm_time = datetime.datetime.strptime(time_str, "%H:%M").time()
    while True:
        now = datetime.datetime.now().time()
        if now >= alarm_time:
            print("Alarm ringing!")
            break

def set_reminder(reminder_text):
    # Dummy implementation for reminder
    print(f"Reminder set: {reminder_text}")

if __name__ == "__main__":
    wishMe()
    app.run(debug=True)