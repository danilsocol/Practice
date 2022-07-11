import asyncio
import copy

from null import Null

from database_methods import database_methods
from settings import bot
from telegram_bot.controls.create_menus import create_menus
from telegram_bot.output import output_ad


class collect_inf:
    user_dict = dict()

    async def collecting_inf(message):

        if (message.text == "/start"):
            bot.send_message(message.chat.id,
                             text="Вы в меню".format(
                                 message.from_user), reply_markup=create_menus.markup_main_menu)

        elif (message.text == "Меню"):
            bot.send_message(message.chat.id, text="Вы в меню!)", reply_markup=create_menus.markup_start_menu)

        elif (message.text == "Назад"):
            collect_inf.user_dict[message.chat.id].get_step(-1)
            if(collect_inf.user_dict[message.chat.id].step == 0):
                bot.register_next_step_handler(message, collect_inf.question_search_your_city)
                bot.send_message(message.chat.id, text="Вы будете искать в своём городе или нет?".format(
                                 message.from_user), reply_markup=create_menus.markup_menu_yes_no)

            elif (collect_inf.user_dict[message.chat.id].step == 1):
                bot.register_next_step_handler(message, collect_inf.get_sphere)
                bot.send_message(message.chat.id, text="Что вы собираетесь искать".format(
                                 message.from_user),reply_markup=create_menus.markup_menu_collect_inf)

            elif (collect_inf.user_dict[message.chat.id].step == 2):
                bot.register_next_step_handler(message, collect_inf.get_type_range)
                bot.send_message(message.chat.id,
                                 text="Выберете тип диапазона цены".format(
                                     message.from_user), reply_markup=create_menus.markup_range_type)

            elif(collect_inf.user_dict[message.chat.id].step == -1):
                bot.send_message(message.chat.id, text="Вы в меню!)", reply_markup=create_menus.markup_start_menu)


    async def out_exam(message):
        if (collect_inf.user_dict[message.chat.id].type_range == "1"):
            return "от 1000 до 2000"
        elif (collect_inf.user_dict[message.chat.id].type_range == "2"):
            return "От 5000"
        elif (collect_inf.user_dict[message.chat.id].type_range == "3"):
            return "до 5000"


    async def processing_range_str(text,message):
        collect_inf.user_dict[message.chat.id].get_range([None,None])
        str = text.split(" ")
        arr = [None,None]
        if(collect_inf.user_dict[message.chat.id].type_range == "1"):
            arr[0] = int(str[1])
            arr[1] = int(str[3])
        elif (collect_inf.user_dict[message.chat.id].type_range == "2"):
            arr[0] = int(str[1])
        elif (collect_inf.user_dict[message.chat.id].type_range == "3"):
            arr[1] = int(str[1])

        collect_inf.user_dict[message.chat.id].get_range(arr)


    def get_city(message):
        try:
            asyncio.run(collect_inf.get_city_as(message))
        except:
            bot.register_next_step_handler(message, collect_inf.get_city)
            bot.send_message(message.chat.id,
                             text="Не верно введены данные, пожалуйста  повторите попытку".format(
                                 message.from_user), reply_markup=create_menus.markup_range_type)


    def question_search_your_city(message):
        if (message.text == "Да"):
            bot.register_next_step_handler(message, collect_inf.get_sphere)
            collect_inf.user_dict[message.chat.id].get_step( 1)
            collect_inf.user_dict[message.chat.id].get_user_city(database_methods.get_user_data(message.chat.id)[1])
            bot.send_message(message.chat.id,
                             text="Что вы собираетесь искать?".format(
                                 message.from_user), reply_markup=create_menus.markup_menu_collect_inf)

        elif (message.text == "Нет"):
            bot.send_message(message.chat.id, text="Тогда выберете город".format(
                                 message.from_user),reply_markup=create_menus.markup_menu_collect_inf)
            bot.register_next_step_handler(message, collect_inf.get_city)

        else:
            if (message.text == "/start"):
                bot.send_message(message.chat.id,
                                 text="Вы в меню".format(
                                     message.from_user), reply_markup=create_menus.markup_main_menu)

            else:
                bot.send_message(message.chat.id, text="На такую комманду я не запрограммирован..")
                bot.register_next_step_handler(message, collect_inf.question_search_your_city)


    async def get_city_as(message):#TODO проверить Назад X2
        if(message.text == "Назад" or message.text == "Меню"):
            await collect_inf.collecting_inf(message)
        else:
            collect_inf.user_dict[message.chat.id].get_step( 1)
            collect_inf.user_dict[message.chat.id].get_user_city(message.text)
            bot.register_next_step_handler(message, collect_inf.get_sphere)
            bot.send_message(message.chat.id,
                             text="Что вы собираетесь искать?".format(
                                 message.from_user), reply_markup=create_menus.markup_menu_collect_inf)


    def get_sphere(message):
        try:
            asyncio.run(collect_inf.get_sphere_as(message))
        except:
            bot.register_next_step_handler(message, collect_inf.get_sphere)
            bot.send_message(message.chat.id,
                             text="Не верно введены данные, пожалуйста  повторите попытку".format(
                                 message.from_user), reply_markup=create_menus.markup_range_type)


    async def get_sphere_as(message):
        if (message.text == "Назад" or message.text == "Меню"):
            await collect_inf.collecting_inf(message)
        else:
            collect_inf.user_dict[message.chat.id].get_step( 1)
            collect_inf.user_dict[message.chat.id].get_sphere( message.text)
            bot.register_next_step_handler(message, collect_inf.get_type_range)
            bot.send_message(message.chat.id,
                             text="Выберете тип диапазона цены".format(
                                 message.from_user), reply_markup=create_menus.markup_range_type)


    def get_type_range(message):
        try:
           asyncio.run(collect_inf.get_type_range_as(message))
        except:
            bot.register_next_step_handler(message, collect_inf.get_type_range)
            bot.send_message(message.chat.id,
                             text="Не верно введены данные, пожалуйста  повторите попытку".format(
                                 message.from_user), reply_markup=create_menus.markup_range_type)


    async def get_type_range_as(message):
        if (message.text == "Назад" or message.text == "Меню"):
            await collect_inf.collecting_inf(message)
        else:

            if(message.text[0] == '1' or message.text[0] == '2' or message.text[0] == '3' ):
                collect_inf.user_dict[message.chat.id].get_step( 1)
                collect_inf.user_dict[message.chat.id].get_type_range (message.text[0])
                bot.register_next_step_handler(message, collect_inf.get_range)
                bot.send_message(message.chat.id, text=(
                        "Введите диапозон например: " + f"{await collect_inf.out_exam(message)}").format(
                    message.from_user), reply_markup=create_menus.markup_menu_collect_inf)

            else:
                bot.send_message(message.chat.id,
                                 text="Не верно введены данные, пожалуйста  повторите попытку".format(
                                     message.from_user), reply_markup=create_menus.markup_range_type)
                bot.register_next_step_handler(message, collect_inf.get_type_range)


    def get_range(message):
        try:
           asyncio.run(collect_inf.get_range_as(message))
        except:
            bot.register_next_step_handler(message, collect_inf.get_range)
            bot.send_message(message.chat.id,
                             text="Не верно введены данные, пожалуйста  повторите попытку".format(
                                 message.from_user), reply_markup=create_menus.markup_range_type)

    async def get_range_as(message):
        if (message.text == "Назад" or message.text == "Меню"):
            await collect_inf.collecting_inf(message)

        else:
            collect_inf.user_dict[message.chat.id].get_step_null()
            await collect_inf.processing_range_str(message.text, message)
            database_methods.add_request(message.chat.id,collect_inf.user_dict[message.chat.id].sphere,collect_inf.user_dict[message.chat.id].city)
            bot.send_message(message.chat.id,
                             text=f"Спасибо за подробности\n"
                                  f"Откуда вы хотите брать информацию из бд или сайта\n"
                                  f"С сайта придется немного подольше подождать, но информация свежая\n"
                                  f"С базы данных быстрее, но не факт что информация не устарела".format(
                                 message.from_user),reply_markup= create_menus.markup_menu_parse_or_bd)
            output_ad.down_ad(message,collect_inf.user_dict[message.chat.id])


