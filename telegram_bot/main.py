import telebot
import asyncio
from telebot import types
from telegram_bot.controls.create_menus import *

bot = telebot.TeleBot('5510546300:AAGhyj2jzJ8saz5LW7FoDUQ1OuYYYPFoKGQ')

#Text
@bot.message_handler(content_types=['text'])
def text(message):
    asyncio.run(message.func(message))

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

bot.polling()