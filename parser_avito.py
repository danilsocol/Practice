from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


class AvitoParse:

    def __init__(self, request, city, price_from=None, price_to=None):
        self.driver = webdriver.Chrome()
        self.request = request
        self.city = city
        self.price_from = price_from
        self.price_to = price_to

    def __del__(self):
        self.driver.close()

    def avito_start(self):
        self.driver.get('https://www.avito.ru/')  # открывает главную страницу авито
        time.sleep(3)  # ждем 3 секунды, чтобы избежать блока

        self.driver.find_element(By.CLASS_NAME, "main-locationWrapper-R8itV").click()  # выбор города
        self.driver.find_element(By.CLASS_NAME, "suggest-input-rORJM").send_keys(
            f"{self.city}")  # вписываем нужный город, который передал пользователь
        time.sleep(3)
        self.driver.find_element(By.XPATH,
                                 '//*[@id="app"]/div[2]/div/div[2]/div/div[6]/div/div/span/div/div[1]/div[2]/div/ul/li[1]').click()
        time.sleep(3)
        self.driver.find_element(By.XPATH,
                                 '//*[@id="app"]/div[2]/div/div[2]/div/div[6]/div/div/span/div/div[3]/div/div[2]/div/button').click()  

    def get_ads(self):
        self.driver.find_element(By.CLASS_NAME, "input-input-Zpzc1").send_keys(f"{self.request}\n")

        if self.price_from == None and self.price_to == None:
            pass
        elif self.price_from == None:
            self.driver.find_element(By.XPATH,
                                     '//*[@id="app"]/div[3]/div[3]/div[1]/div/div[2]/div[1]/form/div[5]/div/div[2]/div/div/div/div/div/div/label[2]/input').send_keys(
                f"{self.price_to}")
            self.driver.find_element(By.XPATH,
                                     '//*[@id="app"]/div[3]/div[3]/div[1]/div/div[2]/div[2]/div/button[1]').click()
        elif self.price_to == None:
            self.driver.find_element(By.XPATH,
                                     '//*[@id="app"]/div[3]/div[3]/div[1]/div/div[2]/div[1]/form/div[5]/div/div[2]/div/div/div/div/div/div/label[1]/input').send_keys(
                f"{self.price_from}")
            self.driver.find_element(By.XPATH,
                                     '//*[@id="app"]/div[3]/div[3]/div[1]/div/div[2]/div[2]/div/button[1]').click()
        else:
            self.driver.find_element(By.XPATH,
                                     '//*[@id="app"]/div[3]/div[3]/div[1]/div/div[2]/div[1]/form/div[5]/div/div[2]/div/div/div/div/div/div/label[1]/input').send_keys(
                f"{self.price_from}")
            self.driver.find_element(By.XPATH,
                                     '//*[@id="app"]/div[3]/div[3]/div[1]/div/div[2]/div[1]/form/div[5]/div/div[2]/div/div/div/div/div/div/label[2]/input').send_keys(
                f"{self.price_to}")
            self.driver.find_element(By.XPATH,
                                     '//*[@id="app"]/div[3]/div[3]/div[1]/div/div[2]/div[2]/div/button[1]').click()
        time.sleep(2)
        links_on_page = self.driver.find_elements(By.CLASS_NAME, "iva-item-content-rejJg")[:20]
        try:
            vip = self.driver.find_element(By.CLASS_NAME, "items-vip-KXPvy").find_elements(By.CLASS_NAME,
                                                                                           "iva-item-content-rejJg")
            [links_on_page.remove(i) for i in vip]
        except:
            pass

        return links_on_page

    def parse_card(self, card_element):
        card = dict()
        card['url'] = card_element.find_element(By.TAG_NAME, "a").get_attribute('href')  # ссылка
        card['title'] = card_element.find_element(By.TAG_NAME, "h3").text  # название
        card['price'] = card_element.find_elements(By.TAG_NAME, "meta")[1].get_attribute('content')  # цена
        card['description'] = card_element.find_element(By.CLASS_NAME,
                                                        "iva-item-descriptionStep-C0ty1").text  # описание
        return card

    def parse_20_cards(self):
        mass_of_cards = []
        for el in self.get_ads():
            mass_of_cards.append(self.parse_card(el))
        return mass_of_cards

p = AvitoParse("Видеокарты", "Екатеринбург", 100, 20000)
p.avito_start()
p.parse_20_cards()
