import calendar
import datetime
import numpy as np
import matplotlib.pyplot as plt
from datetime import date

fig = plt.figure(figsize=(6, 4))
ax = fig.add_subplot()

def grp(step,mass,list_x):

    x = [f'{list_x[i]}'for i in range(step)] # кол-во столбцов , так же подпись снизу
    y = mass #
    ax.bar(x, y)
    #plt.plot(10,5,1)

    #plt.savefig('saved_figure.png')
    plt.show()

def week_day():
    today = datetime.date.today()
    week_day= []
    for i in range(0, 7):
        week_day[i] = (today - datetime.timedelta(days=i)).weekday()

    return week_day


grp(5,[10,5,6,8,18],week_day())
['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']