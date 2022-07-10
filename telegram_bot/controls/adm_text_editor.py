import asyncio
import datetime
import os
import time
from dateutil.relativedelta import relativedelta
import settings
from database_methods import database_methods
from settings import bot
from telegram_bot.controls.create_menus import create_menus
from telegram_bot.controls.graph_creater import graph_creater


class adm_text_editor:
    adm_dict = dict()


    def editor_menu_adm(message):
        if (message.text == "Перейти в режим пользователя"):
            settings.mode_adm[message.chat.id] = False
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
            bot.send_message(message.chat.id, text="Введите id пользователя и кол-во койнов (например: id 486468 coins 1000)" ,
            reply_markup=create_menus.markup_menu_back)
            bot.register_next_step_handler(message, adm_text_editor.set_user_and_coins)

        elif (message.text == "Обновить избранное"):
            bot.send_message(message.chat.id, text="Началось обновление избранного, дождитесь сообщение об окончании")
            database_methods.update_all_favorite_prices()
            bot.send_message(message.chat.id, text="Обновление закончилось")

        else:
            if(message.text == "/start"):
                settings.mode_adm[message.chat.id] = False
                bot.send_message(message.chat.id,
                                 text="Вы в меню".format(
                                     message.from_user), reply_markup=create_menus.markup_main_menu)
            else:
                bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")


    def select_interval(message):
        bot.register_next_step_handler(message, adm_text_editor.editor_interval)
        bot.send_message(message.chat.id,
                         text="Выберете промежуток времени".format(
                             message.from_user), reply_markup=create_menus.markup_menu_interval_selection)

    def set_user_and_coins(message):
        if(message.text != "Назад"):
            id_user_and_coins = message.text.split()
            database_methods.change_coins(id_user_and_coins[0],id_user_and_coins[1])
            bot.send_message(message.chat.id,
                             text=f"Койны были добавлены".format(
                                 message.from_user), reply_markup=create_menus.markup_adm_menu)


    def editor_interval(message):
        asyncio.run(adm_text_editor.editor_interval_as(message))


    async def editor_interval_as(message):
        if (adm_text_editor.adm_dict[message.chat.id] == "act"):
            if (message.text == "Неделя"):
                act = database_methods.get_active_users(datetime.date.today() - datetime.timedelta(days=6),
                                                        datetime.date.today())
                bot.send_message(message.chat.id,
                                 text=f"В выбронный промежуток времени активано {act} пользователей".format(
                                     message.from_user), reply_markup=create_menus.markup_adm_menu)


            elif (message.text == "Месяц"):
                act = database_methods.get_active_users(datetime.date.today() - datetime.timedelta(days=29),
                                                        datetime.date.today())
                bot.send_message(message.chat.id,
                                 text=f"В выбронный промежуток времени активано {act} пользователей".format(
                                     message.from_user), reply_markup=create_menus.markup_adm_menu)

            elif (message.text == "Год"):
                act = database_methods.get_active_users(datetime.date.today() - datetime.timedelta(days=364),
                                                        datetime.date.today())
                bot.send_message(message.chat.id,
                                 text=f"В выбронный промежуток времени активано {act} пользователей".format(
                                     message.from_user), reply_markup=create_menus.markup_adm_menu)

        elif( adm_text_editor.adm_dict[message.chat.id] == "req"):
            if (message.text == "Неделя"):
                req = database_methods.get_requests_count(datetime.date.today() - datetime.timedelta(days=6),
                                                        datetime.date.today())
                bot.send_message(message.chat.id,
                                 text=f"В выбронный промежуток времени было {req} запросов".format(
                                     message.from_user), reply_markup=create_menus.markup_adm_menu)


            elif (message.text == "Месяц"):
                req = database_methods.get_requests_count(datetime.date.today() - datetime.timedelta(days=29),
                                                        datetime.date.today())
                bot.send_message(message.chat.id,
                                 text=f"В выбронный промежуток времени было {req} запросов".format(
                                     message.from_user), reply_markup=create_menus.markup_adm_menu)

            elif (message.text == "Год"):
                req = database_methods.get_requests_count(datetime.date.today() - datetime.timedelta(days=364),
                                                        datetime.date.today())
                bot.send_message(message.chat.id,
                                 text=f"В выбронный промежуток времени было {req} запросов".format(
                                     message.from_user), reply_markup=create_menus.markup_adm_menu)

        elif (adm_text_editor.adm_dict[message.chat.id] == "rook"):
            if (message.text == "Неделя"):
                rook = database_methods.get_list_rookie(datetime.date.today() - datetime.timedelta(days=6),datetime.date.today())
                graph_creater.graph_creat(7, graph_creater.pull_day(7,rook), graph_creater.week_day(),message.chat.id)
                img = open(f"graph{message.chat.id}.png",'rb')
                bot.send_photo(message.chat.id, photo=img)
                img.close()
                os.remove(f"D:/Project/Practic/graph{message.chat.id}.png")
                bot.send_message(message.chat.id,
                                 text="Что то ещё?".format(
                                     message.from_user), reply_markup=create_menus.markup_adm_menu)

            elif (message.text == "Месяц"):
                rook = database_methods.get_list_rookie(datetime.date.today() - datetime.timedelta(days=29), datetime.date.today())
                graph_creater.graph_creat(30,graph_creater.pull_day(30,rook), graph_creater.month(),message.chat.id)
                img = open(f"graph{message.chat.id}.png",'rb')
                bot.send_photo(message.chat.id, photo=img)
                img.close()
                os.remove(f"D:/Project/Practic/graph{message.chat.id}.png")
                bot.send_message(message.chat.id,
                                 text="Что то ещё?".format(
                                     message.from_user), reply_markup=create_menus.markup_adm_menu)

            elif (message.text == "Год"):
                rook = database_methods.get_list_rookie_months(datetime.date.today() - relativedelta(months = 11),11)
                graph_creater.graph_creat(12,graph_creater.pull_month(12,rook), graph_creater.year(),message.chat.id)
                img = open(f"graph{message.chat.id}.png",'rb')
                bot.send_photo(message.chat.id, photo=img)
                img.close()
                os.remove(f"D:/Project/Practic/graph{message.chat.id}.png")
                bot.send_message(message.chat.id,
                                 text="Что то ещё?".format(
                                     message.from_user), reply_markup=create_menus.markup_adm_menu)

        else:
            bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")


