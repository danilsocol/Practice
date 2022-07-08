import calendar
import datetime
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
import pandas as pd

fig = plt.figure(figsize=(6, 4))
ax = fig.add_subplot()

class graph_creater:

    def graph_creat(step,mass,list_x):

        x = [f'{list_x[i]}'for i in range(step)] # кол-во столбцов , так же подпись снизу
        y = mass #
        ax.bar(x, y)
        plt.xlabel('Time', fontsize=14)
        plt.ylabel('Count', fontsize=14)
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontsize(4)

        plt.savefig('graph', dpi= 1000)
        #plt.show()

    def week_day(self):
        today = datetime.date.today()
        week_day = []
        for i in range(0, 7):
            week_day.append(calendar.day_name[(datetime.date.today() - datetime.timedelta(days=i)).weekday()])

        return week_day


    def month(self):
        today = datetime.date.today()
        end_date = today - datetime.timedelta(days=30)
        res = pd.date_range(
            min(today, end_date),
            max(today, end_date)
        ).strftime('%d.%m').tolist()
        return res

    def year(self):
        today = datetime.date.today()
        month = []
        step = today.month
        for i in range(0, 12):
            month.append(calendar.month_abbr[step])
            step -= 1
            if (step == 0):
                step = 12

        return month

# graph_creater.graph_creat(20,[10,5,6,8,18,7,5,8,6,7,1,8,7,3,5,47,9,2,7,6],graph_creater.month(0))
