#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import json
import asyncio
import datetime


import avito_parser as pa
import Youla_parser as yp
from dateutil.relativedelta import relativedelta
import math

from settings import bot
from telegram_bot.controls.create_menus import create_menus


class database_methods:

    #добавление пользователя в бд
    @staticmethod
    def create_user(chat_id, city):
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        cur.execute("""
        SELECT strftime('%Y-%m-%d', DATETIME('now'))
        """)
        time = str(cur.fetchone()[0])
        cur.execute("""
        INSERT INTO Users VALUES (:chat_id, :city, :reg, :last_active, 0)
        """, {'chat_id': chat_id, 'city': city, 'reg': time, 'last_active': time})
        conn.commit()
        cur.close()
        conn.close()


    #метод выдачи данных пользователя (койны имя фамилия город) - сделано!!!
    @staticmethod
    def get_user_data(user_id):
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        cur.execute("""
        SELECT * FROM Users
        WHERE user_id = :outer
        """, {'outer': user_id})
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result


    #прием кол-во койнов и id чтоб изменить койны в бд
    #чтобы отнять, вводим отрицательное число
    #если не передавать число, вычитаются 50
    @staticmethod
    def change_coins(user_id, coins_count=-50):
        user = database_methods.get_user_data(user_id)
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        cur.execute("""
        UPDATE Users 
        SET (coins) = (coins+:add)
        WHERE user_id = :user_id
        """, {'add': coins_count, 'user_id': user_id})
        conn.commit()
        cur.close()
        conn.close()

    #проверить есть ли id чата в бд - сделано!!!!
    @staticmethod
    def check_first_start(outer_user_id):
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        cur.execute("""
        SELECT COUNT(*) FROM Users
        WHERE user_id =:outer
        """, {'outer': outer_user_id})
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result[0] > 0    #bool

    #Выдать количество новых пользователей зарегистрированных за промежуток времени
    #вернуть словарь: день (в виде даты) - количество человек
    #потом добавить масштаб (день-неделя) - не сделано
    @staticmethod
    def get_list_rookie(start_date, end_date=None):
        if end_date == None:
            end_date = datetime.date.today()
        days_count = (end_date-start_date).days
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        result = {}
        for i in range(0, days_count+1):
            key = start_date + datetime.timedelta(days=i)
            cur.execute("""
            SELECT COUNT(*) FROM Users
            WHERE registration_date =:outer
            """, {'outer': key})
            temp = cur.fetchone()
            result[key] = temp[0]
        cur.close()
        conn.close()
        return result #list


    #в параметрах любой день в нужном месяце и количество следующих месяцев
    @staticmethod
    def get_list_rookie_months(start_date, months_count):
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        result = {}
        for i in range(0, months_count+1):
            key = start_date + relativedelta(months=i)
            cur.execute("""
            SELECT COUNT(*) FROM Users
            WHERE 
            strftime('%Y-%m', registration_date) = strftime('%Y-%m', :outer)
            """, {'outer': key})
            temp = cur.fetchone()
            result[key] = temp[0]
        cur.close()
        conn.close()
        return result #list

    #Выдать список активных за промежуток времени
    @staticmethod
    def get_active_users(start_date, end_date=None):
        if end_date == None:
            end_date = datetime.date.today()
        days_count = (end_date-start_date).days
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        result = 0
        for i in range(0, days_count+1):
            key = start_date + datetime.timedelta(days=i)
            cur.execute("""
            SELECT COUNT(*) FROM Users
            WHERE last_activity =:outer
            """, {'outer': key})
            temp = cur.fetchone()
            result += temp[0]
        cur.close()
        conn.close()
        return result

    #Кол-во запросов за промежуток времени
    @staticmethod
    def get_requests_count(start_date, end_date=None):
        if end_date == None:
            end_date = datetime.date.today()
        days_count = (end_date - start_date).days
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        result = 0
        for i in range(0, days_count + 1):
            key = start_date + datetime.timedelta(days=i)
            cur.execute("""
          SELECT COUNT(*) FROM Requests
          WHERE strftime('%Y-%m-%d', date_time) =:outer
          """, {'outer': key})
            temp = cur.fetchone()
            result += temp[0]
        cur.close()
        conn.close()
        return result

    #добавляем в таблицу запросов
    @staticmethod
    def add_request(outer_user, request, city):
        #user = self.get_user_data(outer_user)
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO Requests(user_id, text, date_time, city) VALUES (:user_id, :text, datetime('now'), :city)
        """, {'user_id': outer_user, 'text': request, 'city':city}
        )
        conn.commit()
        cur.close()
        conn.close()

    #объявления с авито
    @staticmethod
    def get_avito_ads(outer_user_id, city, request,lower_bound=None, upper_bound=None):
        #user = self.get_user_data(user_id=outer_user_id)
        #p = pa.AvitoParse(user[1], outer_user_id)
        p = pa.AvitoParse(city, outer_user_id)
        p.start()
        database_methods.add_request(outer_user_id, request, city)
        data = p.parse(request, lower_bound, upper_bound)
        data_list = json.dumps(data)
        # data_list = json.dumps(data_list,
        #                   sort_keys=False,
        #                   indent=4,
        #                   ensure_ascii=False,
        #                   separators=(',', ': '))
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        cur.executemany('INSERT INTO Buffer (user_id,url,title,price, city) '
                        'VALUES (:user_id,:url,:title,:price, :city)', json.loads(data_list))
        conn.commit()
        cur.close()
        conn.close()
        return data

    #получаем объявления с юлы
    @staticmethod
    def get_youla_ads(outer_user_id, city, request,str, lower_bound=None, upper_bound=None):
    #def get_youla_ads(outer_user_id, city, request, lower_bound=None, upper_bound=None):
        #user = self.get_user_data(user_id=outer_user_id)
        #y = yp.YoulaParser(user[1])

        bot.send_message(outer_user_id, text=str[0])

        y = yp.YoulaParser(city)

        bot.send_message(outer_user_id, text=str[1])

        y.start()
        database_methods.add_request(outer_user_id, request, city)

        bot.send_message(outer_user_id, text=str[2])

        y.get_ads(lower_bound, upper_bound, request)
        data = y.parse(outer_user_id)
        data_list = json.dumps(data)
        # data_list = json.dumps(data_list,
        #                   sort_keys=False,
        #                   indent=4,
        #                   ensure_ascii=False,
        #                   separators=(',', ': '))
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        cur.executemany('INSERT INTO Buffer (user_id,url,title,price, city) '
                        'VALUES (:user_id, :url, :title, :price, :city)', json.loads(data_list))
        conn.commit()
        cur.close()
        conn.close()
        return data

#Открываю браузер
#Ищу объявления по запросу
#Собираю данные

    #добавить в избранное по ссылке
    @staticmethod
    def add_fav(outer_user_id, part_url):
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        cur.execute("""
            SELECT price, url FROM Buffer
            WHERE instr(url, :url) > 0 
            """, {'url': part_url})
        temp = cur.fetchone()
        price = temp[0]
        url = temp[1]
        cur.execute("""
            INSERT INTO Favourites (user_id,url,price) 
            VALUES (:user_id, :url, :price)
            """, {'user_id': outer_user_id, 'url': url, 'price': price})
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def get_fav(user_id):
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM Favourites
            WHERE :user_id = user_id
            """, {'user_id': user_id})
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result


    #обновить всё
    @staticmethod
    def update_all_favorite_prices():
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        cur.execute("""
        SELECT url, user_id FROM Favourites
        """)
        dict = cur.fetchall()

        for t in dict:
            cur.execute("""
            SELECT price FROM Buffer
            WHERE url = :url
            """, {'url':t[0]})
            old_price = cur.fetchone()[0]
            if str(t[0]).find('avito.ru') > 0:
                avito = pa.AvitoParse('',0)
                try:
                    new_price = avito.check_price_change(t[0])
                except Exception:
                    new_price = 0
            else:
                youla = yp.YoulaParser('')
                try:
                    new_price = youla.change_price(t[0])
                except Exception:
                    new_price = 0
            cur.execute("""
                        UPDATE Favourites 
                        SET (price) = (:new_price)
                        WHERE url = :url
                        """, {'new_price': new_price, 'url': t[0]})
            conn.commit()

            if (abs(new_price-old_price) > 0.1*old_price):
                database_methods.notify_price_change(t[0], new_price, t[1])
        cur.close()
        conn.close()

    #все обновления товара по части ссылки
    @staticmethod
    def fav_updates(user_id, part_url):
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        cur.execute("""
        SELECT id FROM Favourites
        WHERE :user_id = user_id AND instr(url, :part)>0
        """, {'user_id': user_id, 'part': part_url})
        temp = cur.fetchall()
        for t in temp:
            cur.execute("""
            SELECT updated, price FROM Favourites_price_updates
            WHERE fav_id = :outer
            """, {'outer': t[0]})
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    #тело придумайте сами
    @staticmethod
    def notify_price_change(url, price, user_id):
        bot.send_message(user_id,
                         text=f"Здраствуейте, у товара изменилась цена!\n"
                              f"Новая цена: {price}\n"
                              f"{url}")


    @staticmethod
    def get_fav(user_id):
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM Favourites
            WHERE :user_id = user_id
            """, {'user_id': user_id})
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    #убрать из избранного
    @staticmethod
    def remove_fav(user_id, part_url):
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        cur.execute("""
                DELETE FROM Favourites
                WHERE :user_id = user_id AND instr(url, :part) > 0 
                """, {'user_id': user_id, 'part': part_url})
        conn.commit()
        cur.close()
        conn.close()

    #список пользовательских запросов
    @staticmethod
    def get_user_requests(user_id):
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        cur.execute("""
                    SELECT * FROM Requests
                    WHERE :user_id = user_id
                    """, {'user_id': user_id})
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result


    #получаем объявления из бд
    @staticmethod
    def get_ads_from_db(user_id, request, city, lower_bound=0, upper_bound=1_000_000):
        if(lower_bound == None):
            lower_bound = 0
        if(upper_bound == None):
            upper_bound = 1_000_000
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        database_methods.add_request(user_id,request,city)
        cur.execute("""
        SELECT * FROM Buffer
        WHERE instr(title, :request)>0 AND city=:city AND price BETWEEN :lower_bound AND :upper_bound
        """, {'request': request, 'city': city, 'lower_bound': lower_bound, 'upper_bound': upper_bound})
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result