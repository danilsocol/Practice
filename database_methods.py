import sqlite3
import json
import asyncio
import datetime
import avito_parser as pa
import Youla_parser as yp

class database_methods:

    #добавление пользователя в бд
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


    #TODO прием кол-во койнов и id чтоб изменить койны в бд
    def add_coins(self, user_id, coins_number):
        user = self.get_user_data(user_id)



    #Todo забрать 50 койнов у пользователя



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

        #TODO: Выдать список новых пользователей зарегистрированных за промежуток времени
        #вернуть словарь: день - количество человек
        #потом добавить масштаб (день-неделя)

    @staticmethod
    #def get_list_rookie(start_date, end_date=datetime.date.now()):
     #   conn = sqlite3.connect('BuyBot.db')
      #  cur = conn.cursor()
       # start_date = datetime.date.strptime(start_date)
        #end_date = datetime.date.strptime(end_date)
        #days_count = datetime.timedelta(end_date - start_date)
        #cur.execute("""
          #  SELECT * FROM Users
           # WHERE registration_date =:outer
            #""")
        # result = cur.fetchall()
        # cur.close()
        # return #list

    #TODO: Выдать список активных за промежуток времени
    @staticmethod
    def get_active_users(date):
        return list

    #TODO: Кол-во запросов за промежуток времени
    @staticmethod
    def get_requests_list():
      return list

    #добавляем в таблицу запросов
    def add_request(self, outer_user, request):
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

    #объявления с авито
    def get_avito_ads(self,  outer_user_id, city, request, lower_bound=None, upper_bound=None):
        #user = self.get_user_data(user_id=outer_user_id)
        #p = pa.AvitoParse(user[1], outer_user_id)
        p = pa.AvitoParse(city, outer_user_id)
        p.start()
        self.add_request(outer_user_id, request)
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
        return data_list

    #получаем объявления с юлы
    def get_youla_ads(self, outer_user_id, city, request, lower_bound=None, upper_bound=None):
        #user = self.get_user_data(user_id=outer_user_id)
        #y = yp.YoulaParser(user[1])
        y = yp.YoulaParser(city)
        y.start()
        self.add_request(outer_user_id, request)
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

    #добавить в избранное по ссылке
    def add_fav(self, outer_user_id, url):
        conn = sqlite3.connect('BuyBot.db')
        cur = conn.cursor()
        cur.execute("""
            SELECT price FROM Buffer
            WHERE url = :url
            """, {'url': url})
        price = cur.fetchone()[0]
        cur.execute("""
            INSERT INTO Favourites (user_id,url,price) 
            VALUES (:user_id, :url, :price)
            """, {'user_id': outer_user_id, 'url': url, 'price': price})
        conn.commit()
        cur.close()
        conn.close()
