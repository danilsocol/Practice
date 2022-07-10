from telebot import types

from database_methods import database_methods
from settings import bot
from telegram_bot.controls.create_menus import create_menus


class view_fav:
    list_fav = 0
    count = 0

    @staticmethod
    def start_view(message):
        view_fav.count = 0
        view_fav.list_fav = database_methods.get_fav(message.chat.id)
        view_fav.view(message)

    @staticmethod
    def view(message):
        over_fav = False
        for i in range(view_fav.count,view_fav.count+5):
            if(len(view_fav.list_fav) <= i):
                over_fav = True
                break
            markup = types.InlineKeyboardMarkup()
            btn_del_favourit = types.InlineKeyboardButton(text="Удалить из избрангого", callback_data=f"del {view_fav.list_fav[i][2][-10::]}")
            btn_view_graph = types.InlineKeyboardButton(text="Посмотреть изменение цены", callback_data=f"graph {view_fav.list_fav[i][2][-10::]}")
            markup.add(btn_del_favourit,btn_view_graph)
            bot.send_message(message.chat.id,
                         text=f"{view_fav.list_fav[i][2]}".format(
                             message.from_user), reply_markup=markup)

        if (over_fav):
            bot.send_message(message.chat.id,
                             text="Объявления закончились\nВы вернулись в меню".format(
                                 message.from_user), reply_markup=create_menus.markup_main_menu)
        else:
            view_fav.count += 5
            bot.register_next_step_handler(message, view_fav.editor)
            bot.send_message(message.chat.id,
                             text="Вы хотите ещё?".format(
                                 message.from_user), reply_markup=create_menus.markup_menu_yes_no)



    def editor(message):
        if(message.text == "Да"):
            #TODO койны гони
            view_fav.view(message)

        elif(message.text == "Нет"):
            bot.send_message(message.chat.id,
                             text="Вы вернулись в меню".format(
                                 message.from_user), reply_markup=create_menus.markup_main_menu)

        else:
            bot.register_next_step_handler(message, view_fav.editor)
            bot.send_message(message.chat.id,
                             text="Я вас не понял".format(
                                 message.from_user), reply_markup=create_menus.markup_menu_yes_no)
