import asyncio

import settings
from settings import bot
from telegram_bot.controls import graph_text_editor
from telegram_bot.controls.create_menus import create_menus


class adm_text_editor:
    adm_dict = dict()

    async def editor_menu_adm(message):
        if (message.text == "Перейти в режим пользователя"):
            settings.mode_adm = False
            bot.send_message(message.chat.id,
                             text="Вы вернулись".format(
                                 message.from_user), reply_markup=create_menus.markup_start_menu)

        elif( message.text == "Просмотреть кол-во активности пользователей"):
            adm_text_editor.adm_dict[message.chat.id] = "act"
            adm_text_editor.select_interval(message)

        elif (message.text == "Просмотреть кол-во запросов"):
            adm_text_editor.adm_dict[message.chat.id] = "req"
            adm_text_editor.select_interval(message)

        elif (message.text == "Просмотреть кол-во новых пользователей"):
            adm_text_editor.adm_dict[message.chat.id] = "rook"
            adm_text_editor.select_interval(message)

        elif(message.text == "Добавить пользователю койны"):
            bot.send_message(message.chat.id, text="Введите id пользователя и кол-во койнов (например: id 486468 coins 1000)")
            bot.register_next_step_handler(message, adm_text_editor.set_user_and_coins)

        else:
            bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")


    def select_interval(message):
        bot.register_next_step_handler(message, adm_text_editor.editor_interval)

        bot.send_message(message.chat.id,
                         text="Выберете промежуток времени".format(
                             message.from_user), reply_markup=create_menus.markup_menu_interval_selection)

    def set_user_and_coins(message):
        id_user_and_coins = message.text.split()
        #Todo отправить койны и id

    def editor_interval(message):
        asyncio.run(adm_text_editor.editor_interval_as)


    # def editor_interval_as(message):
    #     if (adm_text_editor.adm_dictp[message.chat.id] == "act"):
    #         if(message.text == "Неделя"):
    #             graph_text_editor.grp(7,,)
    #         elif(message.text == "Месяц"):
    #             graph_text_editor.grp(30,,)
    #         elif(message.text == "Год"):
    #             graph_text_editor.grp(12,,)
    #
    #     elif( adm_text_editor.adm_dictp[message.chat.id] == "req"):
    #         if (message.text == "Неделя"):
    #             graph_text_editor.grp(7,,)
    #         elif (message.text == "Месяц"):
    #             graph_text_editor.grp(30,,)
    #         elif (message.text == "Год"):
    #             graph_text_editor.grp(12,,)
    #
    #     elif (adm_text_editor.adm_dictp[message.chat.id] == "rook"):
    #         if (message.text == "Неделя"):
    #             graph_text_editor.grp(7,,)
    #         elif (message.text == "Месяц"):
    #             graph_text_editor.grp(30,,)
    #         elif (message.text == "Год"):
    #             graph_text_editor.grp(12,,)
    #
    #     else:
    #         bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")