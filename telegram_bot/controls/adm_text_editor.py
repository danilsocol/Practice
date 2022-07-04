import asyncio

from settings import bot
from telegram_bot.controls.create_menus import create_menus


class adm_text_editor:
    adm_dict = dict()

    async def editor_menu_adm(message):
        if (message.text == "Режим посетителя"):
            bot.send_message(message.chat.id,
                             text="Вы вернулись".format(
                                 message.from_user), reply_markup=create_menus.markup_start_menu)

        elif( message.text == "Активность"):
            adm_text_editor.adm_dict[message.chat.id] = "act"
            adm_text_editor.select_interval(message)

        elif (message.text == "Кол-во запросов"):
            adm_text_editor.adm_dict[message.chat.id] = "req"
            adm_text_editor.select_interval(message)

        elif (message.text == "Кол-во новых пользователей"):
            adm_text_editor.adm_dict[message.chat.id] = "rook"
            adm_text_editor.select_interval(message)

        else:
            bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")


    def select_interval(message):
        bot.register_next_step_handler(message, adm_text_editor.editor_interval)

        bot.send_message(message.chat.id,
                         text="Выберете промежуток времени".format(
                             message.from_user), reply_markup=create_menus.markup_menu_interval_selection)

    def editor_interval(message):
        asyncio.run(adm_text_editor.editor_interval_as)


    def editor_interval_as(message):
        if (adm_text_editor.adm_dictp[message.chat.id] == "act"):
            if(message.text == "Неделя"):
                pass
            elif(message.text == "Месяц"):
                pass
            elif(message.text == "Год"):
                pass

        elif( adm_text_editor.adm_dictp[message.chat.id] == "req"):
            if (message.text == "Неделя"):
                pass
            elif (message.text == "Месяц"):
                pass
            elif (message.text == "Год"):
                pass

        elif (adm_text_editor.adm_dictp[message.chat.id] == "rook"):
            if (message.text == "Неделя"):
                pass
            elif (message.text == "Месяц"):
                pass
            elif (message.text == "Год"):
                pass

        else:
            bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")