import sqlite3
import json
import asyncio
import datetime
import avito_parser as pa
import Youla_parser as yp
from dateutil.relativedelta import relativedelta

from settings import bot
from telegram_bot.controls.create_menus import create_menus


class database_methods:

    #добавление пользовател€ в бд
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


    #метод выдачи данных пользовател€ (койны им€ фамили€ город) - сделано!!!
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
    #чтобы отн€ть, вводим отрицательное число
    #если не передавать число, вычитаютс€ 50
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

    #¬ыдать количество новых пользователей зарегистрированных за промежуток времени
    #вернуть словарь: день (в виде даты) - количество человек
    #потом добавить масштаб (день-недел€) - не сделано
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


    #в параметрах любой день в нужном мес€це и количество следующих мес€цев
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

    #¬ыдать список активных за промежуток времени
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

    # ол-во запросов за промежуток времени
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

    #добавл€ем в таблицу запросов
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

    #объ€влени€ с авито
    @staticmethod
    def get_avito_ads(outer_user_id, city, request, lower_bound=None, upper_bound=None):
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

    #получаем объ€влени€ с юлы
    @staticmethod
    def get_youla_ads(outer_user_id, city, request,str, lower_bound=None, upper_bound=None):
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

#ќткрываю браузер
#»щу объ€влени€ по запросу
#—обираю данные

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

    #обновить цены
    #где обнова юлы?
    @staticmethod
    def update_all_favorite_prices():
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        cur.execute("""
        SELECT url FROM Favourites
        """)
        urls = cur.fetchall()

        for url in urls:
            if str(url[0]).find('avito.ru') > 0:
                avito = pa.AvitoParse()
                new_price = avito.check_price_change(url[0])
                cur.execute("""
                UPDATE Favourites 
                SET (price) = (:new_price)
                """, {'new_price': new_price})
                conn.commit()
            else:
                pass
        cur.close()
        conn.close()

    #получить список избранного
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


    #убрать избранную штучку по последним символам
    @staticmethod
    def remove_fav(user_id, part_url):
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        cur.execute("""
                DELETE FROM Favourites
                WHERE :user_id = user_id AND instr(url, :part) > 0 
                """, {'user_id': user_id, 'part': part_url})
        result = cur.fetchall()
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


    #получаем объ€влени€ из бд
    @staticmethod
    def get_ads_from_db(user_id, request, city, lower_bound=0, upper_bound=1_000_000):
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