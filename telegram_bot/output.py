from database_methods import database_methods
from settings import bot
from telegram_bot.controls.create_menus import create_menus


class output_ad:

    def output(message, ad):
        count = 0
        while(True):
            try:
                ad_youla = database_methods.get_youla_ads(message.chat.id, ad.city, ad.sphere, ad.range[0], ad.range[1])
                break
            except:
                continue
        while (True):
            try:
                ad_avito = database_methods.get_avito_ads(message.chat.id, ad.city, ad.sphere, ad.range[0], ad.range[1])
                break
            except:
                continue

        for i in range(0,5):
            bot.send_message(message.chat.id,
                         text=f"Название: {ad_youla[count]['title']}\n"
                              f"Цена: {ad_youla[count]['price']}\n"
                              f"Ссылка: {ad_youla[count]['url']}".format(
                             message.from_user))
            count += 1
        for i in range(0,5):
            bot.send_message(message.chat.id,
                         text=f"Название: {ad_avito[count]['title']}\n"
                              f"Цена: {ad_avito[count]['price']}\n"
                              f"Ссылка: {ad_avito[count]['url']}".format(
                             message.from_user))
            count += 1

        bot.register_next_step_handler(message, output_ad.editor)


    def editor(message):
        bot.send_message(message.chat.id,
                         text="Вы ещё?".format(
                             message.from_user), reply_markup=create_menus.markup_menu_yes_no)

        if(message.text == "Да"):
            #TODO койны гони
            output_ad.output(message)

        elif(message.text == "Нет"):
            bot.send_message(message.chat.id,
                             text="Вы вернулись в меню".format(
                                 message.from_user), reply_markup=create_menus.markup_main_menu)

        else:
            bot.send_message(message.chat.id,
                             text="Я вас не понял".format(
                                 message.from_user), reply_markup=create_menus.markup_menu_yes_no)