# chatbot
from datetime import datetime
import webbrowser
import requests

# Corpus
greet_messages = ["hi", "hello", "hey", "hi there", "hey there"]
date_msgs = ["what's the date","date","tell me date","today's date"]
time_msgs = ["what's the time","time","tell me time","current time"]

def get_weather(city):
    WEATHER_API_KEY="0cd7b92016b8d8d8b69583cc15612985"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    #print(data)

    if data["cod"] != 200:
        return "Sorry, I couldn't find that location."

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]

    return f"\nWeather in {city}:\nTemperature: {temp}°C\nCondition: {desc}\nHumidity: {humidity}%\n"

def get_latest_news():
    NEWS_API_KEY = "8fed92d6de2447caba785aef3e9f2dcd"

    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    data = requests.get(url).json()
    #print(data)
    if data["status"] != "ok":
        return "Error fetching news."

    articles = data["articles"][:5]
    reply = "Top 5 Latest News:\n"
    for i, a in enumerate(articles, 1):
        reply += f"\n{i}. {a['title']} ({a['source']['name']})"

    return reply

def get_location():
    response = requests.get("http://ip-api.com/json/")
    data = response.json()
    #print(data);
    city = data.get("city", "Unknown location")
    country = data.get("country", "Unknown country")
    return country,city

#news url="https://newsapi.org/v2/everything?q=tesla&from=2026-01-01&sortBy=publishedAt&apiKey=8fed92d6de2447caba785aef3e9f2dcd"

chat = True

while chat:
    msg = input("Enter your message: ").lower()

    if msg in greet_messages:
        print("Hello, how are you ?\n")

    elif msg in date_msgs:
        print(datetime.now().date())

    elif msg in time_msgs:
        current_time = datetime.now().time()
        print(current_time.strftime("%I:%M:%S"))

    elif "open" in msg:
        site = msg.split("open ")[-1]
        url = f"https://www.{site}.com"
        webbrowser.open(url)
        print(f"Opening {site}...\n")

    elif "location" in msg:
        country, city = get_location()
        print(f"Your location is {city}, {country}\n")

    elif "weather" in msg:
        c,cty=get_location()
        print(get_weather(cty))

    elif "news" in msg:
        print(get_latest_news())
        print()

    elif "bye" in msg:
        print("Bye !!")
        chat = False

    else:
        print("I can't understand\n")