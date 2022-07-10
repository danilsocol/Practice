import asyncio

from database_methods import database_methods
from settings import bot
from telegram_bot.controls.collect_inf import collect_inf
from telegram_bot.controls.create_menus import create_menus
from telegram_bot.controls.view_fav import view_fav
from telegram_bot.controls.view_his import view_his
from telegram_bot.search_inf import search_inf


class user_text_editor:

    start_collect_inf = False

    async def user_editor(message):
        if (message.text == "Меню"):
            bot.send_message(message.chat.id, text="Вы в меню!)",reply_markup= create_menus.markup_main_menu)

        elif (message.text == "Личный кабинет"):
            prof = database_methods.get_user_data(message.chat.id)
            bot.send_message(message.chat.id, text=f"Ваш личный кабинет\n"
                                                   f"Ваш id: {message.chat.id}\n"
                                                   f"Ваш город: {prof[1]}\n"
                                                   f"У вас {prof[4]} койнов", reply_markup=create_menus.markup_menu_back)

        elif (message.text == "Назад" ):
            bot.send_message(message.chat.id,
                             text="Вы вернулись".format(
                                 message.from_user), reply_markup=create_menus.markup_start_menu)

        elif(message.text == "Просмотреть объявления"):

            bot.send_message(message.chat.id,
                             text="Стоимость данной операции 50 койнов"
                                  "\nХотите продолжить".format(
                                 message.from_user),reply_markup=create_menus.markup_menu_yes_no)
            bot.register_next_step_handler(message, user_text_editor.question_start_viewing)

        elif (message.text == "Избранное"):
            view_fav.start_view(message)

        elif (message.text == "История"):
            view_his.start_view(message)



        else:
            bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")

    def question_start_viewing(message):
        asyncio.run(user_text_editor.question_start_viewing_as(message))

    async def question_start_viewing_as(message):
        if(message.text == "Да"):
            collect_inf.user_dict[message.chat.id] = search_inf
            user_text_editor.start_collect_inf = True
            database_methods.change_coins(message.chat.id)
            bot.send_message(message.chat.id,
                             text="Вы будете искать в своём городе или нет?".format(
                                 message.from_user), reply_markup=create_menus.markup_menu_yes_no)
            bot.register_next_step_handler(message, collect_inf.question_search_your_city)

        elif(message.text == "Нет"):
            bot.send_message(message.chat.id,
                             text="Вы венулись в меню".format(
                                 message.from_user),reply_markup=create_menus.markup_main_menu)
        else:
            bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")