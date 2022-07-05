import sqlite3
import json
import asyncio
import datetime
#TODO: асинхронность

class database_methods:
    #добавление пользователя в бд
    def create_user(chat_id, city):
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO Users VALUES (chat_id, city, datetime(now))
        """)
        cur.commit()

    #получение объявлений с авито
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

        #TODO: Выдать список новых пользователей зарегистрированных за промежуток времени
        #вернуть словарь: день - количество человек
        #потом добавить масштаб (день-неделя)
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

        #TODO: Выдать список активных за промежуток времени
    async def get_list_act(date):
        return list

        #TODO: Кол-во запросов за промежуток времени
    async def get_list_requests():
      return list