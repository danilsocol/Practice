import asyncio

from settings import bot
from telegram_bot.controls.content_types import content_types
from telegram_bot.controls.create_menus import create_menus



create_menus.create_markup(0)

# Commands
@bot.message_handler(commands=['start'])
def start(message):
   # content_types.start_collect_inf = False
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я BuyVideoCardsBot".format(
                         message.from_user), reply_markup=create_menus.markup_start_menu)


@bot.message_handler(commands=['adm'])
def adm(message):
   # content_types.start_collect_inf = False
    bot.send_message(message.chat.id,
                     text="Теперь вы адиминстратор".format(
                         message.from_user), reply_markup=create_menus.markup_adm_menu)


# Text
@bot.message_handler(content_types=['text'])
def text(message):
   # if (content_types.start_collect_inf == False):
        asyncio.run(content_types.func(message))
    # else:
    #     #bot.register_next_step_handler(message, get_city)
    #     collect_inf.collecting_inf(message, bot)


bot.polling()