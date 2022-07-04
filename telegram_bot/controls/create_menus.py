import asyncio

from telebot import types


class create_menus:
    markup_start_menu = 0
    markup_adm_menu = 0
    markup_menu_collect_inf = 0
    markup_range_type = 0
    markup_main_menu = 0
    markup_menu_technical_support = 0
    markup_menu_interval_selection = 0

    def create_markup(self):

        create_menus.markup_start_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        asyncio.run(create_menus.create_start_menu(create_menus.markup_start_menu))

        create_menus.markup_adm_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        asyncio.run(create_menus.create_adm_menu(create_menus.markup_adm_menu))

        create_menus.markup_menu_collect_inf = types.ReplyKeyboardMarkup(resize_keyboard=True)
        asyncio.run(create_menus.create_menu_collect_inf(create_menus.markup_menu_collect_inf))

        create_menus.markup_range_type = types.ReplyKeyboardMarkup(resize_keyboard=True)
        asyncio.run(create_menus.create_range_selection(create_menus.markup_range_type))

        create_menus.markup_main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        asyncio.run(create_menus.create_main_menu(create_menus.markup_main_menu))

        create_menus.markup_menu_technical_support = types.ReplyKeyboardMarkup(resize_keyboard=True)
        asyncio.run(create_menus.create_menu_technical_support(create_menus.markup_menu_technical_support))

        create_menus.markup_menu_interval_selection = types.ReplyKeyboardMarkup(resize_keyboard=True)
        asyncio.run(create_menus.create_menu_technical_support(create_menus.markup_menu_technical_support))



    async def create_adm_menu(markup):
        btn_activity = types.KeyboardButton("Активность")
        btn_number_of_requests = types.KeyboardButton("Кол-во запросов")
        btn_number_of_new_users = types.KeyboardButton("Кол-во новых пользователей")
        btn_normal_mode = types.KeyboardButton("Режим посетителя")
        markup.add(btn_activity, btn_number_of_requests, btn_number_of_new_users,  btn_normal_mode)


    async def create_start_menu(markup):
        btn_menu = types.KeyboardButton("Меню")
        btn_technical_support = types.KeyboardButton("Техподдержка")
        markup.add(btn_menu, btn_technical_support)


    async def create_main_menu(markup):
        btn_back = types.KeyboardButton("Назад")
        btn_favourites = types.KeyboardButton("Избранное")
        btn_view_ads = types.KeyboardButton("Просмотреть объявления")
        btn_search_history = types.KeyboardButton("История")
        btn_notifications = types.KeyboardButton("Уведомления")
        markup.add(btn_view_ads, btn_favourites, btn_notifications, btn_search_history, btn_back)


    async def create_menu_technical_support(markup):
        btn_contact_administrator = types.KeyboardButton("Связаться с администратором")
        back = types.KeyboardButton("Назад")
        markup.add(btn_contact_administrator, back)


    async def create_range_selection(markup):
        btn_from_to = types.KeyboardButton("1) от __ до __")
        btn_from = types.KeyboardButton("2) от __")
        btn_to = types.KeyboardButton("3) до __")
        btn_menu = types.KeyboardButton("Меню")
        btn_back = types.KeyboardButton("Назад")
        markup.add(btn_from_to,btn_from,btn_to,btn_back,btn_menu)


    async def create_menu_collect_inf(markup):
        btn_menu = types.KeyboardButton("Меню")
        btn_back = types.KeyboardButton("Назад")
        markup.add(btn_back, btn_menu)


    async def create_menu_interval_selection(markup):
        btn_day = types.KeyboardButton("День")
        btn_week = types.KeyboardButton("Неделя")
        btn_month = types.KeyboardButton("Месяц")
        btn_year = types.KeyboardButton("Год")
        markup.add(btn_day, btn_week, btn_month, btn_year)

