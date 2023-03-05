import telebot
from telebot import types
from bs4 import BeautifulSoup
import requests
import random

def parse():

    url = 'https://statusas.ru/citaty-i-aforizmy/citaty-pro-zhivotnyx-i-zverej/citaty-i-memy-volka-auf.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    items = soup.findAll('img', class_="lazy")
    workers = []
    for data in items:
        if 'volk' in data['data-src']:
            workers.append(data["data-src"])

    return workers
wolf_images = parse()

def choose_img():
    index = random.randrange(len(wolf_images))
    return wolf_images[index]

token_file = open('config.token', 'r')
token = token_file.read()
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🐺 Замотивироваться 🐺")
    btn2 = types.KeyboardButton("🐺 Тоже замотивироваться 🐺")
    markup.add(btn1, btn2)
    bot.send_sticker(message.chat.id, sticker="CAACAgIAAxkBAAIlpGQEL0duQmOBBWOlfSGQZF4Jbd5HAAIzAQAC9wLIDzvK4ZTu2U7NLgQ")
    bot.send_message(message.chat.id, "Важно не то, кто первый, а то, кто первый!".format(message.from_user), reply_markup=markup)
@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text=="🐺 Замотивироваться 🐺" or message.text=="🐺 Тоже замотивироваться 🐺":
        img = choose_img()
        bot.send_photo(message.chat.id,img)
bot.polling(non_stop=True)
