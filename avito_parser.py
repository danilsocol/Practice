from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import json
import lxml
from Parser import Parser


class AvitoParse(Parser):
    def __init__(self, city):
        self.driver = webdriver.Chrome()
        self.city = city

    def __del__(self):
        self.driver.close()

    def start(self):
        try:
            self.driver.get('https://www.avito.ru/')  # открывает главную страницу Авито
            time.sleep(3)
            self.driver.find_element(By.CLASS_NAME, "styles-title-UgMQ7")
        except NoSuchElementException:
            self.driver.refresh()
        try:
            self.driver.find_element(By.CLASS_NAME, "main-locationWrapper-R8itV").click()  # выбор города
            self.driver.find_element(By.CLASS_NAME, "suggest-input-rORJM").send_keys(
                    f"{self.city}")
        except NoSuchElementException:
            self.driver.refresh()
            self.driver.find_element(By.CLASS_NAME, "main-locationWrapper-R8itV").click()
            # вписываем нужный город, который передал пользователь
            self.driver.find_element(By.CLASS_NAME, "suggest-input-rORJM").send_keys(f"{self.city}")
        time.sleep(2)
        self.driver.find_element(By.XPATH,
                                 '//*[@id="app"]/div[2]/div/div[2]/div/div[6]/div/div/span/div/div[1]/div[2]/div/ul/li[1]').click()
        time.sleep(2)
        self.driver.find_element(By.XPATH,
                                 '//*[@id="app"]/div[2]/div/div[2]/div/div[6]/div/div/span/div/div[3]/div/div[2]/div/button').click()

    def get_ads(self, request, price_from: None, price_to: None):
        self.driver.find_element(By.CLASS_NAME, "input-input-Zpzc1").send_keys(f"{request}\n")
        input_prices = self.driver.find_element(By.CLASS_NAME, "styles-root-vSsLn")

        if price_from is None and price_to is None:
            pass
        elif price_from is None:
            input_prices.find_elements(By.TAG_NAME, "input")[1].send_keys(f"{price_to}")
            self.driver.find_element(By.CLASS_NAME, "styles-box-Up_E3").click()
        elif price_to is None:
            input_prices.find_elements(By.TAG_NAME, "input")[0].send_keys(f"{price_from}")
            self.driver.find_element(By.CLASS_NAME, "styles-box-Up_E3").click()
        else:
            input_prices.find_elements(By.TAG_NAME, "input")[0].send_keys(f"{price_from}")
            input_prices.find_elements(By.TAG_NAME, "input")[1].send_keys(f"{price_to}")
            self.driver.find_element(By.CLASS_NAME, "styles-box-Up_E3").click()

        time.sleep(2)
        links_on_page = self.driver.find_elements(By.CLASS_NAME, "iva-item-content-rejJg")[:20]
        try:
            vip = self.driver.find_element(By.CLASS_NAME, "items-vip-KXPvy").find_elements(By.CLASS_NAME,
                                                                                           "iva-item-content-rejJg")
            [links_on_page.remove(i) for i in vip]
        except NoSuchElementException:
            pass

        return links_on_page

    @staticmethod
    def parse_card(card_element):
        card = dict()
        card['url'] = card_element.find_element(By.TAG_NAME, "a").get_attribute('href')  # ссылка
        card['title'] = card_element.find_element(By.TAG_NAME, "h3").text  # название
        card['price'] = card_element.find_elements(By.TAG_NAME, "meta")[1].get_attribute('content')  # цена
        # card['description'] = card_element.find_element(By.CLASS_NAME,
        #                                                 "iva-item-descriptionStep-C0ty1").text  # описание
        return card

    def parse(self, request, price_from, price_to):
        mass_of_cards = []
        for el in self.get_ads(request, price_from, price_to):
            mass_of_cards.append(self.parse_card(el))
        return mass_of_cards

    # def check_price_change(self, url_ad):
    #     self.driver.get(url_ad)
    #     soup = BeautifulSoup(self.driver.page_source, features="lxml")
    #     price = int(soup.find('span', {'itemprop': 'price'}).get_text().replace('\xa0', ''))
    #     return price



user_city = "Челябинск"
user_request = "Машины"
user_price_from = None
user_price_to = None

p = AvitoParse(user_city)
p.start()
to_json = p.parse(user_request, user_price_from, user_price_to)
# with open('itmes_Avito.json', 'w', encoding='windows-1251') as file: #запись в json файл
#     json.dump(to_json, file, indent=2, ensure_ascii=False)

# url = 'https://www.avito.ru/chelyabinsk/tovary_dlya_kompyutera/videokarta_rtx_3070_m_laptop_8gb_66_mhs_2485106585'