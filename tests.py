#!/usr/bin/python
# -*- coding: utf-8 -*-
import database_methods as db
import sqlite3
import avito_parser as pa
import Youla_parser as yp


#db.database_methods.create_user(25102003, 'Chelyabinsk')
#print(db.check_first_start(25102002))


user = db.database_methods.get_user_data(user_id=25102003)
#p = pa.AvitoParse(user[1])
#p.start()
request = 'колонка'
lower_bound = 2_000
upper_bound = 10_000
temp = db.database_methods()
data2 = temp.get_youla_ads(25102003, request, lower_bound, upper_bound)
for i in range(0, len(data2)):
    print(data2[i])
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