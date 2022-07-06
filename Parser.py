from selenium import webdriver
from abc import ABC, abstractmethod


class Parser(ABC):
    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__init__()

    @abstractmethod
    def get_ads(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def parse(self):
        pass
