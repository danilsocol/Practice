import json
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

static_URL = 'https://youla.ru'
input_text = 'машины' #ввод текста (можно изменять)
result_URL = static_URL + '/?q=' + input_text
from_ = 30000  # Ввод поля от какого диапазона цен (можно изменять)
to_ = None  # Ввод поля до какого диапазона цен (можно изменять)
new_links = [] #список ссылок
names = [] #список названий
prices = [] #список цен
new_prices = [] #список изменённых цен (.replace('Цена по запросу', 'Цена не указана'))

def bs_initialization(driver):  # получение html кода нужной страницы
    html = driver.page_source
    return BeautifulSoup(html, 'lxml')


def driver_initialization():  # запуск драйвера, открытие нужной веб-страницы, 'headless' - обозначает скрыть открытие браузера, фильтрация по цене
    option = webdriver.ChromeOptions()
    # option.add_argument('headless') ЗАКОМЕНЧЕНО!!! P.S. Потому что с ним не работает :(
    driver = webdriver.Chrome(options=option)
    driver.get(result_URL)
    driver.maximize_window()
    time.sleep(3)

    input_price(driver)  # вызов метода интервала цены
    time.sleep(3)
    return driver


def input_price(driver):  # поиск элемента ввода цены, установка цены от, до.
    if from_ is None and to_ is None:
        pass
    elif from_ is None:
        driver.find_element(By.NAME, 'to').send_keys(f"{to_}")
    elif to_ is None:
        driver.find_element(By.NAME, 'from').send_keys(f"{from_}")
    else:
        driver.find_element(By.NAME, 'from').send_keys(f"{from_}")
        driver.find_element(By.NAME, 'to').send_keys(f"{to_}")


def parse():  # запуск парсера, поиск элементов с атрибутом 'data-test-component': 'ProductCard', а также запись ссылки, названия и цены товара в соответствующие списки, закрытие драйвера
    driver = driver_initialization()
    soup = bs_initialization(driver)
    cards = soup.find_all('figure', {'data-test-component': 'ProductCard'})

    for i in cards:
        new_links.append(static_URL + i.find_previous('a').get('href'))
        names.append(i.find_previous('a').get('title'))
        prices.append(i
                      .find('span', {'data-test-component': 'Price'})
                      .get_text()
                      .replace('\u205f', '')
                      .replace('\xa0₽', ''))

    driver.quit()

    new_prices = [price.replace('Цена по запросу', 'Цена не указана')
    if price == 'Цена по запросу' else price for price in prices]

    return { #возврат словаря с 3-мя списками
        'название': names,
        'цена': new_prices,
        'ссылка': new_links
    }


to_json = parse()
with open('itmes.json', 'w', encoding='windows-1251') as file: #запись в json файл
    json.dump(to_json, file, indent=2, ensure_ascii=False)


# def out():  # метод отображения списков ссылок, названия и цен в консоль (в лист new_prices добавляется соответствующая 'Цена не указана', если в объявлении не указана цена) МЕТОД НУЖЕН ДЛЯ ДЕБАГА!
#
#     for k in new_links:
#         print('URL: ' + k)
#     for s in names:
#         print('NAME: ' + s)
#     for a in new_prices:
#         print('PRICE: ' + a)