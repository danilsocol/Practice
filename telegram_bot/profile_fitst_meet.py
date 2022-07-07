import asyncio
import profile
from settings import bot
from telegram_bot.controls.create_menus import create_menus
from database_methods import database_methods


class profile_fitst_meet:
    profile_dict = dict()

    def get_name_prof(message):
        profile_fitst_meet.profile_dict[message.chat.id] = profile
        try:
            asyncio.run(profile_fitst_meet.get_name_prof_as(message))
        except:
            bot.send_message(message.chat.id,
                             text="Не верно введены данные, пожалуста повторите попытку".format(
                                 message.from_user))
            bot.register_next_step_handler(message, profile_fitst_meet.get_name_prof)

    async def get_name_prof_as(message):
        text = message.text.split()

        profile_fitst_meet.profile_dict[message.chat.id].name = text[0]
        profile_fitst_meet.profile_dict[message.chat.id].surname = text[1]

        bot.register_next_step_handler(message, profile_fitst_meet.get_city_prof)
        bot.send_message(message.chat.id,
                         text="Введите город в котором вы проживаете".format(
                             message.from_user))

    def get_city_prof(message):
        try:
            asyncio.run(profile_fitst_meet.get_city_prof_as(message))
        except:
            bot.send_message(message.chat.id,
                             text="Не верно введены данные, пожалуста повторите попытку".format(
                                 message.from_user))
            bot.register_next_step_handler(message, profile_fitst_meet.get_city_prof)



    async def get_city_prof_as(message):
        profile_fitst_meet.profile_dict[message.chat.id].user_city = message.text
        database_methods.create_user(message.chat.id,
                   profile_fitst_meet.profile_dict[message.chat.id].user_city)
        database_methods.add_coins(message.chat.id,100)
        bot.send_message(message.chat.id,
                         text="Спасибо, для того что бы вы смогли попробовать наш продукт мы зачислили вам 100 койнов, приятного пользования".format(
                             message.from_user),reply_markup=create_menus.markup_start_menu) # надо внести в бд

