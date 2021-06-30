import telebot
from dotenv import load_dotenv
from pathlib import Path
import os
import yfinance as yf
import requests
 
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("API_KEY")
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['weather'])
def send_weather(message):
    if len(message.text.split()) < 2:
        return bot.reply_to(message, "Please input a city.")
    weather_address = f"https://api.openweathermap.org/data/2.5/weather?q={message.text.split()[1]}&appid=0c42f7f6b53b244c78a418f4f181282a&units=metric"
    json_data = requests.get(weather_address).json()
    formatted_data = f"""Description: {json_data['weather'][0]['description']}
Temperature: {round(json_data['main']['temp'])}℃
Feels like: {round(json_data['main']['feels_like'])}℃
Humidity: {json_data['main']['humidity']}%"""
    bot.send_message(message.chat.id, formatted_data)

@bot.message_handler(commands=['btcprice'])
def send_cprice(message):
    if len(message.text.split()) < 2:
        return bot.reply_to(message, "Please input a currency to display in!")
    crypto_address = f"https://api.coindesk.com/v1/bpi/currentprice/{message.text.split()[1].upper()}.json"
    jsondata = requests.get(crypto_address).json()
    reply = f"""Bitcoin Price
{jsondata['bpi'][f"{message.text.split()[1].upper()}"]['description']}
Price: ${round(float(jsondata['bpi'][f"{message.text.split()[1].upper()}"]['rate'].replace(',', '')), 2)}
Updated: {jsondata['time']['updated']}"""
    bot.send_message(message.chat.id, reply)
bot.polling()