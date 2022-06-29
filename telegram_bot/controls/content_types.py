from create_menus import *
from main import bot


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


