import asyncio
import datetime
import settings
from database_methods import database_methods
from settings import bot
from telegram_bot.controls import graph_creater
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
        database_methods.change_coins(id_user_and_coins[0],id_user_and_coins[1])


    def editor_interval(message):
        asyncio.run(adm_text_editor.editor_interval_as(message))


    async def editor_interval_as(message):
        # if (adm_text_editor.adm_dict[message.chat.id] == "act"):
        #     if(message.text == "Неделя"):
        #         graph_creater.graph_creat(7,,graph_creater.week_day())
        #     elif(message.text == "Месяц"):
        #         graph_creater.graph_creat(30,,graph_creater.month())
        #     elif(message.text == "Год"):
        #         graph_creater.graph_creat(12,,graph_creater.year())
        #
        # elif( adm_text_editor.adm_dict[message.chat.id] == "req"):
        #     if (message.text == "Неделя"):
        #         graph_creater.graph_creat(7, , graph_creater.week_day())
        #     elif (message.text == "Месяц"):
        #         graph_creater.graph_creat(30,, graph_creater.month())
        #     elif (message.text == "Год"):
        #         graph_creater.graph_creat(12,, graph_creater.year())

        # elif (adm_text_editor.adm_dictp[message.chat.id] == "rook"):
        if (adm_text_editor.adm_dict[message.chat.id] == "rook"): #TODO проверить с тестовыми данными
            if (message.text == "Неделя"):
                rook = database_methods.get_list_rookie(datetime.date.today(),
                                                 datetime.date.today() - datetime.timedelta(days=7))
                graph_creater.graph_creat(7, rook, graph_creater.week_day())
            elif (message.text == "Месяц"):
                rook = database_methods.get_list_rookie(datetime.date.today(),
                                                        datetime.date.today() - datetime.timedelta(days=30))
                graph_creater.graph_creat(30,rook, graph_creater.month())
            elif (message.text == "Год"):
                rook = database_methods.get_list_rookie(datetime.date.today(),
                                                        datetime.date.today() - datetime.timedelta(days=365))
                graph_creater.graph_creat(12,rook, graph_creater.year())

        else:
            bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")