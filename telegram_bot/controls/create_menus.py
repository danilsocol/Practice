import asyncio

from telebot import types


class create_menus:
    markup_start_menu = 0
    markup_adm_menu = 0
    markup_menu_collect_inf = 0
    markup_range_type = 0
    markup_main_menu = 0
    markup_menu_back = 0
    markup_menu_interval_selection = 0
    markup_menu_yes_no = 0
    markup_menu_parse_or_bd = 0
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

        create_menus.markup_menu_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
        asyncio.run(create_menus.create_menu_back(create_menus.markup_menu_back))

        create_menus.markup_menu_interval_selection = types.ReplyKeyboardMarkup(resize_keyboard=True)
        asyncio.run(create_menus.create_menu_interval_selection(create_menus.markup_menu_interval_selection))

        create_menus.markup_menu_yes_no = types.ReplyKeyboardMarkup(resize_keyboard=True)
        asyncio.run(create_menus.create_menu_yes_no(create_menus.markup_menu_yes_no))

        create_menus.markup_menu_parse_or_bd = types.ReplyKeyboardMarkup(resize_keyboard=True)
        asyncio.run(create_menus.create_menu_parse_or_bd(create_menus.markup_menu_parse_or_bd))


    async def create_adm_menu(markup):
        btn_activity = types.KeyboardButton("Просмотреть кол-во активности пользователей")
        btn_number_of_requests = types.KeyboardButton("Просмотреть кол-во запросов")
        btn_number_of_new_users = types.KeyboardButton("Просмотреть кол-во новых пользователей")
        btn_add_user_coins = types.KeyboardButton("Добавить пользователю койны")
        btn_upd_fav = types.KeyboardButton("Обновить избранное")
        btn_normal_mode = types.KeyboardButton("Перейти в режим пользователя")
        markup.add(btn_activity, btn_number_of_requests, btn_number_of_new_users,btn_add_user_coins, btn_upd_fav, btn_normal_mode)


    async def create_menu_parse_or_bd(markup):
        btn_parse = types.KeyboardButton("База данных")
        btn_bd = types.KeyboardButton("Сайт")
        markup.add(btn_bd, btn_parse)

    async def create_start_menu(markup):
        btn_menu = types.KeyboardButton("Меню")
        btn_technical_support = types.KeyboardButton("Личный кабинет")
        markup.add(btn_menu, btn_technical_support)


    async def create_main_menu(markup):
        btn_back = types.KeyboardButton("Назад")
        btn_favourites = types.KeyboardButton("Избранное")
        btn_view_ads = types.KeyboardButton("Просмотреть объявления")
        btn_search_history = types.KeyboardButton("История")
        markup.add(btn_view_ads, btn_favourites, btn_search_history, btn_back)


    async def create_menu_back(markup):
        back = types.KeyboardButton("Назад")
        markup.add(back)


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
        btn_week = types.KeyboardButton("Неделя")
        btn_month = types.KeyboardButton("Месяц")
        btn_year = types.KeyboardButton("Год")
        markup.add(btn_week, btn_month, btn_year)

    async def create_menu_yes_no(markup):
        btn_yes =types.KeyboardButton("Да")
        btn_no = types.KeyboardButton("Нет")
        markup.add(btn_no, btn_yes)