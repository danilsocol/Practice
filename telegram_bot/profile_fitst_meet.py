import asyncio
import datetime
import profile
from settings import bot
from telegram_bot.controls.create_menus import create_menus


class profile_fitst_meet:
    profile_dict = dict()

    def get_name_prof(message):
        profile_fitst_meet.profile_dict[message.chat.id] = profile
        asyncio.run(profile_fitst_meet.get_name_prof_as(message))

    async def get_name_prof_as(message):
        profile_fitst_meet.profile_dict[message.chat.id].name = message.text
        bot.register_next_step_handler(message, profile_fitst_meet.get_city_prof)
        bot.send_message(message.chat.id,
                         text="Введите город в котором вы проживаете".format(
                             message.from_user))

    def get_city_prof(message):
        asyncio.run(profile_fitst_meet.get_city_prof_as(message))

    async def get_city_prof_as(message):
        profile_fitst_meet.profile_dict[message.chat.id].city = message.text
        profile_fitst_meet.profile_dict[message.chat.id].reg_date = datetime.date.today()
        profile_fitst_meet.profile_dict[message.chat.id].date_last_request = datetime.date.today()
        bot.send_message(message.chat.id,
                         text="Спасибо, теперь вы можете продолжить)".format(
                             message.from_user),reply_markup=create_menus.markup_start_menu) # надо внести в бд

