from telebot import types

from database_methods import database_methods
from settings import bot
from telegram_bot.controls.create_menus import create_menus


class view_his:
    list_fav = 0
    count = 0

    @staticmethod
    def start_view(message):
        view_his.count = 0
        view_his.list_fav = database_methods.get_user_requests(message.chat.id)
        view_his.view(message)

    @staticmethod
    def view(message):
        over_fav = False
        for i in range(view_his.count, view_his.count + 5):
            if(len(view_his.list_fav) <= i):
                over_fav = True
                break
            bot.send_message(message.chat.id,
                         text=f"id пользователя: {view_his.list_fav[i][1]}\n"
                                f"Город: {view_his.list_fav[i][4]}\n"
                              f"Запрос: {view_his.list_fav[i][2]}\n"
                              f"Время: {view_his.list_fav[i][3]}".format(
                             message.from_user))

        if (over_fav):
            bot.send_message(message.chat.id,
                             text="Запросы закончились\nВы вернулись в меню".format(
                                 message.from_user), reply_markup=create_menus.markup_main_menu)
        else:
            view_his.count += 5
            bot.register_next_step_handler(message, view_his.editor)
            bot.send_message(message.chat.id,
                             text="Вы хотите ещё?".format(
                                 message.from_user), reply_markup=create_menus.markup_menu_yes_no)



    def editor(message):
        if(message.text == "Да"):
            view_his.view(message)

        elif(message.text == "Нет"):
            bot.send_message(message.chat.id,
                             text="Вы вернулись в меню".format(
                                 message.from_user), reply_markup=create_menus.markup_main_menu)

        else:
            bot.register_next_step_handler(message, view_his.editor)
            bot.send_message(message.chat.id,
                             text="Я вас не понял".format(
                                 message.from_user), reply_markup=create_menus.markup_menu_yes_no)
