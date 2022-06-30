import telebot
import asyncio
import settings
from telebot import types
from telegram_bot.controls.content_types import content_types
from telegram_bot.controls.create_menus import create_start_menu, create_adm_menu

bot = telebot.TeleBot(settings.API_KEY)


#Commands
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    asyncio.run(create_start_menu(markup,message.chat.id))
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я BuyVideoCardsBot".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(commands=['adm'])
def adm(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    asyncio.run(create_adm_menu(markup,message.chat.id))
    bot.send_message(message.chat.id,
                     text="Теперь вы адиминстратор".format(
                         message.from_user), reply_markup=markup)


#Text
@bot.message_handler(content_types=['text'])
def text(message):
    asyncio.run(content_types.func(message,bot))


bot.polling()