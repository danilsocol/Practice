import asyncio
import threading
import time
from multiprocessing.pool import ThreadPool
from threading import Thread

from telebot import types

from database_methods import database_methods
from settings import bot
from telegram_bot.controls.create_menus import create_menus


class output_ad:
    count = {}
    ad_youla = {}
    ad_avito = {}
    ad_bd = {}

    q = []
    ad = {}
    #get_ads_from_db
    @staticmethod
    def down_ad(message, ad):
        output_ad.ad[message.chat.id] = ad
        bot.register_next_step_handler(message, output_ad.buff)


    def buff(message):
        bot.send_message(message.chat.id,
                         text=f"Вы в очереди".format(
                             message.from_user))
        output_ad.bd_or_parse(message)

    @staticmethod
    def bd_or_parse(message):
        if(message.text == "База данных"):
            output_ad.down_ad_bd(message, output_ad.ad[message.chat.id])
        elif(message.text == "Сайт"):
            output_ad.down_ad_pars(message, output_ad.ad[message.chat.id])
        else:
            bot.register_next_step_handler(message, output_ad.bd_or_parse)
            bot.send_message(message.chat.id,
                             text="Я вас не понял".format(
                                 message.from_user), reply_markup=create_menus.markup_menu_parse_or_bd)

    @staticmethod
    def down_ad_bd(message, ad):
        output_ad.count[message.chat.id] = 0

        output_ad.ad_bd[message.chat.id] = database_methods.get_ads_from_db(message.chat.id,  ad.sphere,ad.city, ad.range[0], ad.range[1])
        output_ad.output_bd(message)

    @staticmethod
    def down_ad_pars(message, ad):
        output_ad.come_queue(message)
        output_ad.count[message.chat.id] = 0

        th_youla = ThreadPool(processes=1)
        th_avito = ThreadPool(processes=1)
        th1 = th_youla.apply_async(database_methods.get_youla_ads,(message.chat.id, ad.city, ad.sphere, ["Открываю браузер","Ищу объявления по запросу","Собираю объявления"] ,ad.range[0], ad.range[1]))
        th2 = th_avito.apply_async(database_methods.get_avito_ads,(message.chat.id, ad.city, ad.sphere, ad.range[0], ad.range[1]))
        output_ad.ad_youla[message.chat.id] = th1.get()
        output_ad.ad_avito[message.chat.id] = th2.get()
        output_ad.output_parse(message)

    @staticmethod
    def come_queue(message):


        output_ad.q.append(message.chat.id)
        if (threading.active_count() > 8 and output_ad.q[0] != message.chat.id):
            for i in range(0,len(output_ad.q)):
                if(output_ad.q[i] == message.chat.id):
                    bot.send_message(message.chat.id,
                                     text=f"Вы {i} в очереди".format(
                                         message.from_user))
            time.sleep(10)
        output_ad.q.pop()
        bot.send_message(message.chat.id,
                         text=f"Вас пропустили".format(
                             message.from_user))

    def output_bd(message):
        over_ad = True
        for i in range(output_ad.count[message.chat.id], output_ad.count[message.chat.id] + 5):
            if (len(output_ad.ad_bd[message.chat.id]) <= i):
                over_ad = False
                break
            markup = types.InlineKeyboardMarkup()
            btn_add_favourit = types.InlineKeyboardButton(text="Добавить в избранное",
                                                          callback_data=f"add {output_ad.ad_bd[message.chat.id][i][2][-10::]}")
            markup.add(btn_add_favourit)
            bot.send_message(message.chat.id,
                             text=f"Название: {output_ad.ad_bd[message.chat.id][i][3]}\n"
                                  f"Цена: {output_ad.ad_bd[message.chat.id][i][4]}\n"
                                  f"Ссылка: {output_ad.ad_bd[message.chat.id][i][2]}".format(
                                 message.from_user), reply_markup=markup)

        if (not over_ad):
            # if (not over_ad[0]):
            bot.send_message(message.chat.id,
                             text="Объявления закончились\nВы вернулись в меню".format(
                                 message.from_user), reply_markup=create_menus.markup_main_menu)

        else:
            output_ad.count += 5
            bot.register_next_step_handler(message, output_ad.editor_bd)
            bot.send_message(message.chat.id,
                             text="Вы хотите ещё?".format(
                                 message.from_user), reply_markup=create_menus.markup_menu_yes_no)

    def output_parse(message):
        over_ad = [True, True]
        #over_ad = [True]
        for i in range(output_ad.count[message.chat.id],output_ad.count[message.chat.id]+5):
            if(len(output_ad.ad_youla[message.chat.id]) <= i):
                over_ad[0] = False
                break
            markup = types.InlineKeyboardMarkup()
            btn_add_favourit = types.InlineKeyboardButton(text="Добавить в избранное", callback_data=f"add {output_ad.ad_youla[message.chat.id][i]['url'][-10::]}")
            markup.add(btn_add_favourit)
            bot.send_message(message.chat.id,
                         text=f"Название: {output_ad.ad_youla[message.chat.id][i]['title']}\n"
                              f"Цена: {output_ad.ad_youla[message.chat.id][i]['price']}\n"
                              f"Ссылка: {output_ad.ad_youla[message.chat.id][i]['url']}".format(
                             message.from_user), reply_markup=markup)

        for i in range(output_ad.count[message.chat.id],output_ad.count[message.chat.id]+5):
            if (len(output_ad.ad_avito[message.chat.id]) <= i):
                over_ad[1] = False
                break
            markup = types.InlineKeyboardMarkup()
            btn_add_favourit = types.InlineKeyboardButton(text="Добавить в избранное",
                                                          callback_data=f"add {output_ad.ad_avito[message.chat.id][i]['url'][-10::]}")
            markup.add(btn_add_favourit)
            bot.send_message(message.chat.id,
                         text=f"Название: {output_ad.ad_avito[message.chat.id][i]['title']}\n"
                              f"Цена: {output_ad.ad_avito[message.chat.id][i]['price']}\n"
                              f"Ссылка: {output_ad.ad_avito[message.chat.id][i]['url']}".format(
                             message.from_user), reply_markup=markup)

        if(not over_ad[0] and not over_ad[1]):
        #if (not over_ad[0]):
            bot.send_message(message.chat.id,
                             text="Объявления закончились\nВы вернулись в меню".format(
                                 message.from_user), reply_markup=create_menus.markup_main_menu)

        else:
            output_ad.count[message.chat.id] += 5
            bot.register_next_step_handler(message, output_ad.editor_parse)
            bot.send_message(message.chat.id,
                             text="Вы хотите ещё?".format(
                                 message.from_user), reply_markup=create_menus.markup_menu_yes_no)



    def editor_parse(message):
        if(message.text == "Да"):
            output_ad.output_parse(message)

        elif(message.text == "Нет"):
            bot.send_message(message.chat.id,
                             text="Вы вернулись в меню".format(
                                 message.from_user), reply_markup=create_menus.markup_main_menu)

        else:
            bot.register_next_step_handler(message, output_ad.editor_parse)
            bot.send_message(message.chat.id,
                             text="Я вас не понял".format(
                                 message.from_user), reply_markup=create_menus.markup_menu_yes_no)


    def editor_bd(message):
        if(message.text == "Да"):
            output_ad.output_bd(message)

        elif(message.text == "Нет"):
            bot.send_message(message.chat.id,
                             text="Вы вернулись в меню".format(
                                 message.from_user), reply_markup=create_menus.markup_main_menu)

        else:
            if(message.text == "/start"):
                bot.send_message(message.chat.id,
                                 text="Вы в меню".format(
                                     message.from_user), reply_markup=create_menus.markup_main_menu)
            else:
                bot.register_next_step_handler(message, output_ad.editor_bd)
                bot.send_message(message.chat.id,
                                 text="Я вас не понял".format(
                                     message.from_user), reply_markup=create_menus.markup_menu_yes_no)