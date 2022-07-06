#!/usr/bin/python
# -*- coding: utf-8 -*-
import database_methods as db
import sqlite3
import avito_parser as pa



#db.database_methods.create_user(25102003, 'Chelyabinsk')
#print(db.check_first_start(25102002))


user = db.database_methods.get_user_data(user_id=25102003)
p = pa.AvitoParse(user[1])
p.start()
request = 'утюг'
lower_bound = None
upper_bound = 10_000
db.database_methods.add_request(user[0], request)
data = p.parse(request, lower_bound, upper_bound)
for i in range(0, len(data)):
    print(data[i])