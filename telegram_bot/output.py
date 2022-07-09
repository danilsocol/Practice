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
    count = 0
    ad_youla = 0
    ad_avito = 0
    q = []

    @staticmethod
    def down_ad(message, ad):
        output_ad.come_queue(message)
        count = 0

        th_youla = ThreadPool(processes=1)
        th_avito = ThreadPool(processes=1)
        th1 = th_youla.apply_async(database_methods.get_youla_ads,(message.chat.id, ad.city, ad.sphere, ["Открываю браузер","Ищу объявления по запросу","Собираю объявления"] ,ad.range[0], ad.range[1]))
        th2 = th_avito.apply_async(database_methods.get_avito_ads,(message.chat.id, ad.city, ad.sphere, ad.range[0], ad.range[1]))
        output_ad.ad_youla = th1.get()
        output_ad.ad_avito = th2.get()
        output_ad.output(message)

    @staticmethod
    def come_queue(message):
        bot.send_message(message.chat.id,
                         text=f"Вы {len(output_ad.q)} в очереди".format(
                             message.from_user))

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

    def output(message):
        over_ad = [True, True]
        #over_ad = [True]
        for i in range(output_ad.count,output_ad.count+5):
            if(len(output_ad.ad_youla) <= i):
                over_ad[0] = False
                break
            markup = types.InlineKeyboardMarkup()
            btn_add_favourit = types.InlineKeyboardButton(text="Добавить в избранное", callback_data=f"add {output_ad.ad_youla[i]['url'][-10::]}")
            markup.add(btn_add_favourit)
            bot.send_message(message.chat.id,
                         text=f"Название: {output_ad.ad_youla[i]['title']}\n"
                              f"Цена: {output_ad.ad_youla[i]['price']}\n"
                              f"Ссылка: {output_ad.ad_youla[i]['url']}".format(
                             message.from_user), reply_markup=markup)

        for i in range(output_ad.count,output_ad.count+5):
            if (len(output_ad.ad_avito) <= i):
                over_ad[1] = False
                break
            markup = types.InlineKeyboardMarkup()
            btn_add_favourit = types.InlineKeyboardButton(text="Добавить в избранное",
                                                          callback_data=f"add {output_ad.ad_avito[i]['url'][-10::]}")
            markup.add(btn_add_favourit)
            bot.send_message(message.chat.id,
                         text=f"Название: {output_ad.ad_avito[i]['title']}\n"
                              f"Цена: {output_ad.ad_avito[i]['price']}\n"
                              f"Ссылка: {output_ad.ad_avito[i]['url']}".format(
                             message.from_user), reply_markup=markup)

        if(not over_ad[0] and not over_ad[1]):
        #if (not over_ad[0]):
            bot.send_message(message.chat.id,
                             text="Объявления закончились\nВы вернулись в меню".format(
                                 message.from_user), reply_markup=create_menus.markup_main_menu)

        else:
            output_ad.count += 5
            bot.register_next_step_handler(message, output_ad.editor)
            bot.send_message(message.chat.id,
                             text="Вы хотите ещё?".format(
                                 message.from_user), reply_markup=create_menus.markup_menu_yes_no)



    def editor(message):
        if(message.text == "Да"):
            #TODO койны гони
            output_ad.output(message)

        elif(message.text == "Нет"):
            bot.send_message(message.chat.id,
                             text="Вы вернулись в меню".format(
                                 message.from_user), reply_markup=create_menus.markup_main_menu)

        else:
            bot.register_next_step_handler(message, output_ad.editor)
            bot.send_message(message.chat.id,
                             text="Я вас не понял".format(
                                 message.from_user), reply_markup=create_menus.markup_menu_yes_no)