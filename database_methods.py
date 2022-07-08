import sqlite3
import json
import asyncio
import datetime
import avito_parser as pa
import Youla_parser as yp

class database_methods:

    #добавление пользовател€ в бд
    @staticmethod
    def create_user(chat_id, city):
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        cur.execute("""
        SELECT strftime('%d.%m.%Y %H:%M', DATETIME('now'))
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

    #TODO: ¬ыдать список новых пользователей зарегистрированных за промежуток времени
    #вернуть словарь: день - количество человек
    #потом добавить масштаб (день-недел€)

        # ¬ыдать количество новых пользователей зарегистрированных за промежуток времени
        # вернуть словарь: день (в виде даты) - количество человек
        # потом добавить масштаб (день-недел€) - не сделано
    @staticmethod #TODO такой же метод только вернуть мес€цами
    def get_list_rookie(start_date, end_date=None):
        if end_date == None:
            end_date = datetime.date.today()
        days_count = (end_date - start_date).days
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        result = {}
        for i in range(0, days_count + 1):
            key = start_date + datetime.timedelta(days=i)
            cur.execute("""
            SELECT COUNT(*) FROM Users
            WHERE registration_date =:outer
            """, {'outer': key})
            temp = cur.fetchone()
            result[key] = temp[0]
        cur.close()
        conn.close()
        return result  # list

    #TODO: ¬ыдать список активных за промежуток времени
    @staticmethod
    def get_active_users(date):
        return list

    #TODO:  ол-во запросов за промежуток времени
    @staticmethod
    def get_requests_list():
      return list

    #добавл€ем в таблицу запросов
    @staticmethod
    def add_request(outer_user, request):
        #user = self.get_user_data(outer_user)
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO Requests(user_id, text, date_time) VALUES (:user_id, :text, datetime('now'))
        """, {'user_id': outer_user, 'text': request}
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
        database_methods.add_request(outer_user_id, request)
        data = p.parse(request, lower_bound, upper_bound)
        data_list = json.dumps(data)
        # data_list = json.dumps(data_list,
        #                   sort_keys=False,
        #                   indent=4,
        #                   ensure_ascii=False,
        #                   separators=(',', ': '))
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        cur.executemany('INSERT INTO Buffer (user_id,url,title,price) '
                        'VALUES (:user_id,:url,:title,:price)', json.loads(data_list))
        conn.commit()
        cur.close()
        conn.close()
        return data

    #получаем объ€влени€ с юлы
    @staticmethod
    def get_youla_ads(outer_user_id, city, request, lower_bound=None, upper_bound=None):
        #user = self.get_user_data(user_id=outer_user_id)
        #y = yp.YoulaParser(user[1])
        y = yp.YoulaParser(city)
        y.start()
        database_methods.add_request(outer_user_id, request)
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
        cur.executemany('INSERT INTO Buffer (user_id,url,title,price) '
                        'VALUES (:user_id, :url, :title, :price)', json.loads(data_list))
        conn.commit()
        cur.close()
        conn.close()
        return data

    # добавить в избранное по ссылке
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