#!/usr/bin/python
# -*- coding: utf-8 -*-
import database_methods as db
import sqlite3
import avito_parser as pa
import Youla_parser as yp


#db.database_methods.create_user(25102003, 'Chelyabinsk')
#print(db.check_first_start(25102002))


#user = db.database_methods.get_user_data(user_id=25102003)
#p = pa.AvitoParse(user[1])
#p.start()
request = 'бампер'
lower_bound = 200
upper_bound = 10_000
temp = db.database_methods()

#print(db.database_methods.get_avito_ads(25102003, 'Челябинск', request, lower_bound, upper_bound))

print(db.database_methods.fav_updates(25102003, 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/sportivnyy_kostyum_muzhskoy_novyy_2488170415'))

#print(db.database_methods.get_ads_from_db(25102003, 'скетчбук', 'Чебоксары'))
#db.database_methods.add_fav(25102003,'https://www.avito.ru/nizhniy_novgorod/orgtehnika_i_rashodniki/sketchbuk_2407110124?slocation=662210')
#db.database_methods.update_all_favorite_prices()
#db.database_methods.remove_fav(25102003, '662210')
#db.database_methods.get_youla_ads(25102003, 'Вологда',request ,lower_bound,upper_bound)
#print(db.database_methods.remove_fav(25102003, '2488170415'))
#temp.add_fav(25102003, 'https://youla.ru/moskva/zhenskaya-odezhda/aksessuary/ochki-62c5d430678d15570c6ccffc')

#data2 = temp.get_avito_ads(25102003, 'Хабаровск', request, lower_bound, upper_bound)
#for i in range(0, len(data2)):
#    print(data2[i])
#хз что возвращается, главное что в бд залезло!
#UPD: возвращается строка, постараюсь поправить
#UPD2: возвращается list

#db.database_methods.add_request(user[0], request)
#data = p.parse(request, lower_bound, upper_bound)
#for i in range(0, len(data)):
 #   pass

#y = yp.YoulaParser(user[1])
#y.start()
#y.get_ads(lower_bound, upper_bound, request)
#data2 = y.parse()
#for i in range(0, len(data2)):
#    print(data2[i])