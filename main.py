import asyncio

import settings
from settings import bot
from telegram_bot.controls.adm_text_editor import adm_text_editor
from telegram_bot.profile_fitst_meet import profile_fitst_meet
from telegram_bot.controls.user_text_editor import user_text_editor
from telegram_bot.controls.create_menus import create_menus
from database_methods import database_methods

class main:


    create_menus.create_markup(0)

    # Commands



    @bot.message_handler(commands=['start'])
    def start(message):
        if(False): # database_methods.outer_user_id(message.chat.id)
            bot.register_next_step_handler(message, profile_fitst_meet.get_name_prof)
            bot.send_message(message.chat.id,
                             text="Привет, я смотрю вы здесь в первый раз, давай те заполним вашу анкету"
                                  "\nВведите свое Имя и фамилию через пробел".format(
                                 message.from_user))
        else:
            bot.send_message(message.chat.id,
                             text="Привет, {0.first_name}, рад тебя видеть".format(
                                 message.from_user), reply_markup=create_menus.markup_start_menu)


    @bot.message_handler(commands=['adm'])
    def adm(message):
        settings.mode_adm = True
        bot.send_message(message.chat.id,
                         text="Теперь вы адиминстратор".format(
                             message.from_user), reply_markup=create_menus.markup_adm_menu)


    # Text
    @bot.message_handler(content_types=['text'])
    def text(message):
        if(settings.mode_adm):
            asyncio.run(adm_text_editor.editor_menu_adm(message))
        else:
            asyncio.run(user_text_editor.user_editor(message))


    bot.polling()