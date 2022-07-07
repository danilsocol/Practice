import json
import time
import lxml
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from Parser import Parser


class YoulaParser(Parser):
    def __init__(self, city):
        self.option = webdriver.ChromeOptions()
        # self.option.add_argument('headless')
        self.driver = webdriver.Chrome(options=self.option)
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.static_URL = 'https://youla.ru'
        self.city = city

    def __del__(self):
        self.driver.close()

    def start(self):  # открытие юлы, вписывание города (доделывается)
        try:
            self.driver.get(self.static_URL)
            time.sleep(1)
        except NoSuchElementException:
            self.driver.refresh()
        self.driver.find_element(By.TAG_NAME, 'button').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//li[@role='button']//span[text()='Город']").click()
        time.sleep(1)
        towns = self.driver.find_elements(By.XPATH, "//div[@data-test-component='GeolocationModal']//div[@width=240]")
        for i in towns:
            town = i.text
            if town == self.city:
                i.click()
                break
            else:
                continue ##Здесь можно обработать ошибку на ввод города

    def get_ads(self, from_, to_, input_text):  # поиск товара, фильтры ввода цены, установка цены от, до.
        time.sleep(1)
        self.driver.find_element(By.TAG_NAME, 'input').send_keys(f"{input_text}\n")
        if from_ is None and to_ is None:
            pass
        elif from_ is None:
            self.driver.find_element(By.NAME, 'to').send_keys(f"{to_}")
            time.sleep(1)
        elif to_ is None:
            self.driver.find_element(By.NAME, 'from').send_keys(f"{from_}")
            time.sleep(1)
        else:
            self.driver.find_element(By.NAME, 'from').send_keys(f"{from_}")
            time.sleep(1)
            self.driver.find_element(By.NAME, 'to').send_keys(f"{to_}")
            time.sleep(1)

    def parse(self, user_id):  # запуск парсера, поиск элементов с атрибутом 'data-test-component': 'ProductCard', а также запись ссылки, названия и цены товара в соответствующие списки, закрытие драйвера
        time.sleep(2)
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        cards = soup.find_all('figure', {'data-test-component': 'ProductCard'})

        new_links = []  # список ссылок
        names = []  # список названий
        prices = []  # список цен

        for i in cards:
            new_links.append(self.static_URL + i.find_previous('a').get('href'))
            names.append(i.find_previous('a').get('title'))
            prices.append(i
                          .find('span', {'data-test-component': 'Price'})
                          .get_text()
                          .replace('\u205f', '')
                          .replace('\xa0₽', ''))

        new_prices = [price.replace('Цена по запросу', 'Цена не указана')
                      if price == 'Цена по запросу' else price for price in prices]

        for j in range(len(new_prices)):
            new_prices[j] = new_prices[j].replace('руб.', '')

        return self.get_result(names, new_prices, new_links, user_id)

    @staticmethod
    def get_result(names, new_prices, new_links, user_id=0):
        result = []

        for name, price, link in zip(names, new_prices, new_links):
            data = {}
            if user_id != 0:
                data['user_id'] = user_id
            data['url'] = link
            data['title'] = name
            data['price'] = price
            result.append(data)

        return result


#input_text = 'Машины'  # ввод товара (можно изменять)
#input_city = 'Челябинск'   # ввод города (можно изменять)
#from_ = None  # Ввод поля от какого диапазона цен (можно изменять)
#to_ = None  # Ввод поля до какого диапазона цен (можно изменять)

#youla = YoulaParser(input_city)
#youla.start()
#youla.get_ads(from_, to_, input_text)
#to_json = youla.parse()
# with open('itmes_Youla.json', 'w', encoding='windows-1251') as file:  # запись в json файл
#     json.dump(to_json, file, indent=2, ensure_ascii=False)
