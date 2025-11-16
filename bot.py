import telebot
import time
import threading
from Rtoken import realtoken
from parser import get_COM_news,get_OFF_news, get_ALL_news

token = (realtoken)
bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! Выбери какие именно новости ты хочешь пропарсить!\nНовости от комьюнити(/comnews)\nОффицальные новости(/offnews)\nВсе новости(/news)")
@bot.message_handler(commands=["comnews"])# Функция для парсинга статьей комьюнити
def Comnews(message):
    all_COM_news = get_COM_news()
    for comnews in all_COM_news:
        bot.send_message(
            message.chat.id, 
            f"Заголовок: {comnews['title']}\nСсылка: {comnews['link']}"
        )

@bot.message_handler(commands=["offnews"])# Функция для парсинга оффициальных статьей
def Offnews(message):
    all_OFF_news = get_OFF_news()
    for offnews in all_OFF_news:
        bot.send_message(
            message.chat.id,
            f"Заголовок: {offnews['title']}\nСсылка: {offnews['link']}"
    )

@bot.message_handler(commands=["news"])# Функция для парсинга всей статьей в целом
def Allnews(message):
    all_ALL_news = get_ALL_news()
    for allnews in all_ALL_news:
        bot.send_message(
            message.chat.id,
            f"Заголовок: {allnews['title']}\nСсылка: {allnews['link']}")


bot.polling()

