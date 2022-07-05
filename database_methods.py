import sqlite3
import json
import asyncio
import datetime
#TODO: асинхронность

class database_methods:
    #добавление пользовател€ в бд
    def create_user(chat_id, city):  #TODO: изменить, принимать данные name, surname, user_city, coins. “ак же добавл€ть в бд дату активности и дату регистрации
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO Users VALUES (chat_id, city, datetime(now))
        """)
        cur.commit()


    #TODO метод выдачи данных пользовател€ (койны им€ фамили€ город)


    #TODO прием кол-во койнов и id чтоб изменить койны в бд

    #получение объ€влений с авито
    #async def get_avito_list(user_id, request, lower_bound, upper_bound):
     #   #TODO: получить город
      #  p = pa.AvitoParse(None)
       # p.avito_start()
        #data = p.parse_20_cards(request, lower_bound, upper_bound)
        #for i in range(0, len(data)):
         #   print(data[i])

        #проверить есть ли id чата в бд - сделано!!!!
    def check_first_start(outer_user_id):
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        cur.execute("""
        SELECT COUNT(*) FROM Users
        WHERE user_id =:outer
        """, {'outer': outer_user_id})
        result = cur.fetchone()
        cur.close()
        return result[0] > 0    #bool

        #TODO: ¬ыдать список новых пользователей зарегистрированных за промежуток времени
        #вернуть словарь: день - количество человек
        #потом добавить масштаб (день-недел€)
    # async def get_list_rookie(start_date, end_date = datetime.datetime.now()):
    #     conn = sqlite3.connect('BuyBot.db')
    #     cur = conn.cursor()
    #     from = datetime
    #     cur.execute("""
    #         SELECT * FROM Users
    #         WHERE registration_date =:outer
    #         """, {'outer': })
    #     result = cur.fetchall()
    #     cur.close()
    #     return #list

        #TODO: ¬ыдать список активных за промежуток времени
    async def get_list_act(date):
        return list

        #TODO:  ол-во запросов за промежуток времени
    async def get_list_requests():
      return list