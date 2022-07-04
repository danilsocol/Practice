import asyncio
import copy
from settings import bot
from telegram_bot.controls.create_menus import create_menus


class collect_inf:
    user_dict = dict()

    async def collecting_inf(message):

        if (message.text == "Меню"):
            bot.send_message(message.chat.id, text="Вы в меню!)", reply_markup=create_menus.markup_start_menu)

        elif (message.text == "Назад"):
            collect_inf.user_dict[message.chat.id].step -= 1
            if(collect_inf.user_dict[message.chat.id].step == 0):
                bot.register_next_step_handler(message, collect_inf.get_city)
                bot.send_message(message.chat.id, text="Введите название города")

            elif (collect_inf.user_dict[message.chat.id].step == 1):
                bot.register_next_step_handler(message, collect_inf.get_sphere)
                bot.send_message(message.chat.id, text="Что вы собираетесь искать")

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
        arr = []
        str = text.split(" ")
        arr.append(int(str[1]))
        if (len(str) > 2):
            arr.append(int(str[3]))
        collect_inf.user_dict[message.chat.id].range = copy.deepcopy(arr)


    def get_city(message):
        asyncio.run(collect_inf.get_city_as(message))


    async def get_city_as(message):
        if(message.text == "Назад" or message.text == "Меню"):
            await collect_inf.collecting_inf(message)
        else:
            collect_inf.user_dict[message.chat.id].step+=1
            collect_inf.user_dict[message.chat.id].city = message.text
            bot.register_next_step_handler(message, collect_inf.get_sphere)
            bot.send_message(message.chat.id,
                             text="Что вы собираетесь искать?".format(
                                 message.from_user), reply_markup=create_menus.markup_menu_collect_inf)


    def get_sphere(message):
        asyncio.run(collect_inf.get_sphere_as(message))

    async def get_sphere_as(message):
        if (message.text == "Назад" or message.text == "Меню"):
            await collect_inf.collecting_inf(message)
        else:
            collect_inf.user_dict[message.chat.id].step += 1
            collect_inf.user_dict[message.chat.id].sphere = message.text
            bot.register_next_step_handler(message, collect_inf.get_type_range)
            bot.send_message(message.chat.id,
                             text="Выберете тип диапазона цены".format(
                                 message.from_user), reply_markup=create_menus.markup_range_type)



    def get_type_range(message):
        asyncio.run(collect_inf.get_type_range_as(message))

    async def get_type_range_as(message):
        if (message.text == "Назад" or message.text == "Меню"):
            await collect_inf.collecting_inf(message)
        else:
            collect_inf.user_dict[message.chat.id].step += 1
            collect_inf.user_dict[message.chat.id].type_range = message.text[0]
            bot.register_next_step_handler(message, collect_inf.get_range)
            bot.send_message(message.chat.id, text=(
                    "Введите диапозон например: " + f"{await collect_inf.out_exam(message)}").format(
                message.from_user), reply_markup= create_menus.markup_menu_collect_inf)



    def get_range(message):
        asyncio.run(collect_inf.get_range_as(message))


    async def get_range_as(message):
        if (message.text == "Назад" or message.text == "Меню"):
            await collect_inf.collecting_inf(message)
        else:
            collect_inf.user_dict[message.chat.id].step = 0
            await collect_inf.processing_range_str(message.text, message)
            bot.send_message(message.chat.id,
                             text=f"Спасибо за подробности {collect_inf.user_dict[message.chat.id].type_range} "
                                  f"{collect_inf.user_dict[message.chat.id].range} "
                                  f"{collect_inf.user_dict[message.chat.id].city} "
                                  f"{collect_inf.user_dict[message.chat.id].sphere} ".format(
                                 message.from_user),reply_markup= create_menus.markup_menu_collect_inf)