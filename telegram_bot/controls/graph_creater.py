import calendar
import datetime
import numpy as np
import matplotlib
from dateutil.relativedelta import relativedelta
from settings import bot

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from datetime import date
import pandas as pd

class graph_creater:

    @staticmethod
    def graph_creat(step,mass,list_x,id,str_x = "Время",str_y = "Кол-во"):
        fig = plt.figure(figsize=(6, 4))
        ax = fig.add_subplot()

        x = [f'{list_x[i]}'for i in range(step)] # кол-во столбцов , так же подпись снизу


        y = mass
        ax.bar(x, y)
        plt.xlabel(str_x, fontsize=14)
        plt.ylabel(str_y, fontsize=14)
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontsize(3)

        plt.savefig(f'graph{id}', dpi= 1000)


    @staticmethod
    def pull_day(step,mass):
        count = []
        date = datetime.date.today() - datetime.timedelta(days=step-1)
        for i in range(0,len(mass)):
            count.append(mass[date])
            date  += datetime.timedelta(days=1)
        return count

    @staticmethod
    def pull_month(step,mass):
        count = []
        date = datetime.date.today() - relativedelta(months = step - 1)
        for i in range(0, len(mass)):
            count.append(mass[date])
            date += relativedelta(months = 1)
        return count


    @staticmethod
    def week_day():
        today = datetime.date.today()
        week_day = []
        for i in range(0, 7):
            week_day.append(calendar.day_name[(datetime.date.today() - datetime.timedelta(days=i)).weekday()])

        return week_day

    @staticmethod
    def month():
        today = datetime.date.today()
        end_date = today - datetime.timedelta(days=30)
        res = pd.date_range(
            min(today, end_date),
            max(today, end_date)
        ).strftime('%d.%m').tolist()
        return res

    @staticmethod
    def year():
        today = datetime.date.today()
        month = []
        step = today.month
        for i in range(0, 12):
            month.append(calendar.month_abbr[step])
            step -= 1
            if (step == 0):
                step = 12

        return month

#graph_creater.graph_creat(20,[0,5,6,8,0,7,5,8,6,7,0,8,7,3,5,0,9,2,7,6],graph_creater.month())
