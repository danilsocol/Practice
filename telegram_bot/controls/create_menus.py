from telebot import types




async def create_adm_menu(markup,chat_id):
    btn_activity = types.KeyboardButton("Активность")
    btn_number_of_requests = types.KeyboardButton("Кол-во запросов")
    btn_number_of_new_users = types.KeyboardButton("Кол-во новых пользователей")
    btn_number_of_ads = types.KeyboardButton("Кол-во объявлений")
    btn_normal_mode = types.KeyboardButton("Режим посетителя")
    markup.add(btn_activity, btn_number_of_requests, btn_number_of_new_users, btn_number_of_ads, btn_normal_mode)


async def create_start_menu(markup,chat_id):
    btn_menu = types.KeyboardButton("Меню")
    btn_technical_support = types.KeyboardButton("Техподдержка")
    markup.add(btn_menu, btn_technical_support)


async def create_main_menu(markup, chat_id):
    btn_back = types.KeyboardButton("Назад")
    btn_favourites = types.KeyboardButton("Избранное")
    btn_view_ads = types.KeyboardButton("Просмотреть объявления")
    btn_search_history = types.KeyboardButton("История")
    btn_notifications = types.KeyboardButton("Уведомления")
    markup.add(btn_view_ads, btn_favourites, btn_notifications, btn_search_history, btn_back)