import asyncio

from null import Null

from settings import bot
from telegram_bot.controls.adm_text_editor import adm_text_editor
from telegram_bot.profile_fitst_meet import profile_fitst_meet
from telegram_bot.controls.user_text_editor import user_text_editor
from telegram_bot.controls.create_menus import create_menus

mode_adm = False
create_menus.create_markup(0)

# Commands
@bot.message_handler(commands=['start'])
def start(message):
    if(True): # проверка существует есть ли такой пользователей в бд
        bot.register_next_step_handler(message, profile_fitst_meet.get_name_prof)
        bot.send_message(message.chat.id,
                         text="Привет, я смотрю вы здесь в первый раз, давай те заполним вашу анкету"
                              "\n Введите как мне вас называть".format(
                             message.from_user))
    else:
        bot.send_message(message.chat.id,
                         text="Привет, {0.first_name}, рад тебя видеть".format(
                             message.from_user), reply_markup=create_menus.markup_start_menu)


@bot.message_handler(commands=['adm'])
def adm(message):
    mode_adm = True
    bot.send_message(message.chat.id,
                     text="Теперь вы адиминстратор".format(
                         message.from_user), reply_markup=create_menus.markup_adm_menu)


# Text
@bot.message_handler(content_types=['text'])
def text(message):
    if(mode_adm):
        asyncio.run(adm_text_editor.editor(message))
    else:
        asyncio.run(user_text_editor.user_editor(message))


bot.polling()