import telebot
from telebot import types


bot = telebot.TeleBot('5510546300:AAGhyj2jzJ8saz5LW7FoDUQ1OuYYYPFoKGQ')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    createStartMenu(markup,message.chat.id)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я BuyVideoCardsBot".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(commands=['adm'])
def adm(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    createAdmMenu(markup,message.chat.id)
    bot.send_message(message.chat.id,
                     text="Теперь вы адиминстратор".format(
                         message.from_user), reply_markup=markup)


def createAdmMenu(markup,chat_id):
    btnActivity = types.KeyboardButton("Активность")
    btnNumberOfRequests = types.KeyboardButton("Кол-во запросов")
    btnNumberOfNewUsers = types.KeyboardButton("Кол-во новых пользователей")
    btnNumberOfAds = types.KeyboardButton("Кол-во объявлений")
    btnNormalMode = types.KeyboardButton("Режим посетителя")
    markup.add(btnActivity, btnNumberOfRequests, btnNumberOfNewUsers, btnNumberOfAds, btnNormalMode)


def createStartMenu(markup,chat_id):
    btn1 = types.KeyboardButton("Меню")
    btn2 = types.KeyboardButton("Техподдержка")
    markup.add(btn1, btn2)


def createMenu(markup,chat_id):
    btnBack = types.KeyboardButton("Назад")
    btnFavourites = types.KeyboardButton("Избранное")
    btnViewAds = types.KeyboardButton("Просмотреть объявления")
    btnSearchHistory = types.KeyboardButton("История")
    btnNotifications = types.KeyboardButton("Уведомления")
    markup.add(btnViewAds, btnFavourites, btnNotifications ,btnSearchHistory, btnBack)


@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "Меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        createMenu(markup,message.chat.id)
        bot.send_message(message.chat.id, text="Вы в меню!)",reply_markup=markup)

    elif (message.text == "Техподдержка"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Связаться с администратором")
        back = types.KeyboardButton("Назад")
        markup.add(btn1, back)
        bot.send_message(message.chat.id, text="Что вас интересует", reply_markup=markup)

    elif (message.text == "Назад" or message.text == "Режим посетителя" ):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        createStartMenu(markup,message.chat.id)
        bot.send_message(message.chat.id,
                         text="Вы вернулись".format(
                             message.from_user), reply_markup=markup)

    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")


bot.polling()