from settings import bot
from telegram_bot.controls.collect_inf import collect_inf
from telegram_bot.controls.create_menus import create_menus
from telegram_bot.search_inf import search_inf


class user_text_editor:

    start_collect_inf = False

    async def user_editor(message):
        if (message.text == "Меню"):
            bot.send_message(message.chat.id, text="Вы в меню!)",reply_markup= create_menus.markup_main_menu)

        elif (message.text == "Личный кабинет"): # принять фигню и вывести
            bot.send_message(message.chat.id, text=f"Ваш личный кабинет\n"
                                                   "Имя и Фамилия: {}\n"
                                                   "Ваш город: {}\n"
                                                   "У вас {} койнов", reply_markup=create_menus.markup_menu_back)

        elif (message.text == "Назад" ):
            bot.send_message(message.chat.id,
                             text="Вы вернулись".format(
                                 message.from_user), reply_markup=create_menus.markup_start_menu)

        elif(message.text == "Просмотреть объявления"):
            user_text_editor.start_collect_inf = True
            bot.send_message(message.chat.id,
                             text="Введите название города".format(
                                 message.from_user),reply_markup=create_menus.markup_menu_collect_inf)
            #content_types.start_collect_inf = True
            collect_inf.user_dict[message.chat.id] = search_inf
            bot.register_next_step_handler(message, collect_inf.get_city)

        else:
            bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")


