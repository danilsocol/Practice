from settings import bot
from telegram_bot.controls.collect_inf import collect_inf
from telegram_bot.controls.create_menus import create_menus
from telegram_bot.user_inf import user_inf


class content_types:

    start_collect_inf = False

    async def func(message):
        if (message.text == "Меню"):
            # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            # await create_main_menu(markup)
            bot.send_message(message.chat.id, text="Вы в меню!)",reply_markup= create_menus.markup_main_menu)

        elif (message.text == "Техподдержка"):
            # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            # await create_menu_technical_support(markup)
            bot.send_message(message.chat.id, text="Что вас интересует", reply_markup=create_menus.markup_menu_technical_support)

        elif (message.text == "Назад" or message.text == "Режим посетителя" ):
            # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            # await create_start_menu(markup)
            bot.send_message(message.chat.id,
                             text="Вы вернулись".format(
                                 message.from_user), reply_markup=create_menus.markup_start_menu)

        elif(message.text == "Просмотреть объявления"):
            content_types.start_collect_inf = True
            # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            # await create_menu_collect_inf(markup)
            bot.send_message(message.chat.id,
                             text="Введите название города".format(
                                 message.from_user),reply_markup=create_menus.markup_menu_collect_inf)
            #content_types.start_collect_inf = True
            collect_inf.user_dict[message.chat.id] = user_inf
            bot.register_next_step_handler(message, collect_inf.get_city)


        else:
            bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")


