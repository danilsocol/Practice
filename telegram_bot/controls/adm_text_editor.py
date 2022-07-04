from settings import bot
from telegram_bot.controls.create_menus import create_menus


class adm_text_editor:


    async def editor(message):
        if (message.text == "Режим посетителя"):
            bot.send_message(message.chat.id,
                             text="Вы вернулись".format(
                                 message.from_user), reply_markup=create_menus.markup_start_menu)

        elif( message.text == "Активность"):
            adm_text_editor.select_interval(message)

        elif (message.text == "Кол-во запросов"):
            adm_text_editor.select_interval(message)

        elif (message.text == "Кол-во новых пользователей"):
            adm_text_editor.select_interval(message)


        else:
            bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")


    def select_interval(message):
        bot.send_message(message.chat.id,
                         text="Выберете промежуток времени".format(
                             message.from_user), reply_markup=create_menus.markup_menu_interval_selection)
