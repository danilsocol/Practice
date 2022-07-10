from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import json
import lxml
from Parser import Parser
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class AvitoParse(Parser):
    def __init__(self, city, user_id):
        self.option = webdriver.ChromeOptions()
        # self.option.add_argument('headless')
        self.capa = DesiredCapabilities.CHROME
        self.capa["pageLoadStrategy"] = "none"
        self.driver = webdriver.Chrome(desired_capabilities=self.capa, options=self.option)
        self.driver.maximize_window()
        self.city = city
        self.user_id = user_id

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
            if self.city == 'Челябинск':
                pass
            else:
                self.driver.find_element(By.CLASS_NAME, "main-locationWrapper-R8itV").click()  # выбор города
                time.sleep(1)
                self.driver.find_element(By.CLASS_NAME, "suggest-input-rORJM").send_keys(f"{self.city}")
                time.sleep(2)
                self.driver.find_element(By.XPATH,
                                         "//ul[@data-marker='suggest-list']//li[@data-marker='suggest(0)']").click()
                time.sleep(2)
                self.driver.find_element(By.XPATH, "//div[@class='popup-buttons-WICnh']//button").click()
        except NoSuchElementException:
            self.driver.refresh()
            time.sleep(10)
            self.driver.find_element(By.CLASS_NAME, "main-locationWrapper-R8itV").click()
            # вписываем нужный город, который передал пользователь
            self.driver.find_element(By.CLASS_NAME, "suggest-input-rORJM").send_keys(f"{self.city}")

    def get_ads(self, request, price_from: None, price_to: None):
        time.sleep(2)
        self.driver.find_element(By.CLASS_NAME, "input-input-Zpzc1").send_keys(f"{request}\n")
        time.sleep(10)
        input_prices = self.driver.find_element(By.CLASS_NAME, "styles-root-vSsLn")

        if price_from is None and price_to is None:
            pass
        elif price_from is None:
            input_prices.find_elements(By.TAG_NAME, "input")[1].send_keys(f"{price_to}")
            self.driver.find_element(By.CLASS_NAME, "styles-box-Up_E3").click()
            time.sleep(1)
        elif price_to is None:
            input_prices.find_elements(By.TAG_NAME, "input")[0].send_keys(f"{price_from}")
            self.driver.find_element(By.CLASS_NAME, "styles-box-Up_E3").click()
            time.sleep(1)
        else:
            input_prices.find_elements(By.TAG_NAME, "input")[0].send_keys(f"{price_from}")
            input_prices.find_elements(By.TAG_NAME, "input")[1].send_keys(f"{price_to}")
            time.sleep(1)
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
    def parse_card(card_element, user_id, city):
        card = dict()
        card['user_id'] = user_id
        card['url'] = card_element.find_element(By.TAG_NAME, "a").get_attribute('href')  # ссылка
        card['title'] = card_element.find_element(By.TAG_NAME, "h3").text  # название
        card['price'] = card_element.find_elements(By.TAG_NAME, "meta")[1].get_attribute('content')  # цена
        card['city'] = city
        # card['description'] = card_element.find_element(By.CLASS_NAME,
        #                                                 "iva-item-descriptionStep-C0ty1").text  # описание
        return card

    def parse(self, request, price_from, price_to):
        mass_of_cards = []
        for el in self.get_ads(request, price_from, price_to):
            mass_of_cards.append(self.parse_card(el, self.user_id, self.city))
        return mass_of_cards

    def check_price_change(self, url_ad):
        self.driver.get(url_ad)
        soup = BeautifulSoup(self.driver.page_source, features="lxml")
        price = int(soup.find('span', {'itemprop': 'price'}).get_text().replace('\xa0', ''))
        return price


#user_city = "Владивосток"
#user_request = "Телевизор"
#user_price_from = None
#user_price_to = 20000

# p = AvitoParse(user_city)
# p.start()
# to_json = p.parse(user_request, user_price_from, user_price_to)
# with open('itmes_Avito.json', 'w', encoding='windows-1251') as file: #запись в json файл
#     json.dump(to_json, file, indent=2, ensure_ascii=False)

# url = 'https://www.avito.ru/chelyabinsk/tovary_dlya_kompyutera/videokarta_rtx_3070_m_laptop_8gb_66_mhs_2485106585'
