import telebot
from telebot import types


bot = telebot.TeleBot('5510546300:AAGhyj2jzJ8saz5LW7FoDUQ1OuYYYPFoKGQ')


@bot.message_handler(commands=['start'])
async def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await create_start_menu(markup,message.chat.id)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я BuyVideoCardsBot".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(commands=['adm'])
async def adm(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await create_adm_menu(markup,message.chat.id)
    bot.send_message(message.chat.id,
                     text="Теперь вы адиминстратор".format(
                         message.from_user), reply_markup=markup)


async def create_adm_menu(markup,chat_id):
    btn_activity = types.KeyboardButton("Активность")
    btn_number_of_requests = types.KeyboardButton("Кол-во запросов")
    btn_number_of_new_users = types.KeyboardButton("Кол-во новых пользователей")
    btn_number_of_ads = types.KeyboardButton("Кол-во объявлений")
    btn_normal_mode = types.KeyboardButton("Режим посетителя")
    markup.add(btn_activity, btn_number_of_requests, btn_number_of_new_users, btn_number_of_ads, btn_normal_mode)


async def create_start_menu(markup,chat_id):
    btn_menu = types.KeyboardButton("Меню")
    btn_technical_support = types.KeyboardButton("Техподдержка")
    markup.add(btn_menu, btn_technical_support)


async def create_main_menu(markup, chat_id):
    btn_back = types.KeyboardButton("Назад")
    btn_favourites = types.KeyboardButton("Избранное")
    btn_view_ads = types.KeyboardButton("Просмотреть объявления")
    btn_search_history = types.KeyboardButton("История")
    btn_notifications = types.KeyboardButton("Уведомления")
    markup.add(btn_view_ads, btn_favourites, btn_notifications, btn_search_history, btn_back)


@bot.message_handler(content_types=['text'])
async def func(message):
    if (message.text == "Меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        await create_main_menu(markup, message.chat.id)
        bot.send_message(message.chat.id, text="Вы в меню!)",reply_markup=markup)

    elif (message.text == "Техподдержка"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_contact_administrator = types.KeyboardButton("Связаться с администратором")
        back = types.KeyboardButton("Назад")
        markup.add(btn_contact_administrator, back)
        bot.send_message(message.chat.id, text="Что вас интересует", reply_markup=markup)

    elif (message.text == "Назад" or message.text == "Режим посетителя" ):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        await create_start_menu(markup,message.chat.id)
        bot.send_message(message.chat.id,
                         text="Вы вернулись".format(
                             message.from_user), reply_markup=markup)

    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")


bot.polling()