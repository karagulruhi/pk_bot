from seleniumwire import webdriver
from selenium.webdriver.common.by import By


class Driver:
    driver = None

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(options=options)

    def maximizeWindow(self):
        self.driver.maximize_window()

    def getWindow(self, url = "*************"):
        self.driver.get(url)
    
    def close(self):
        self.driver.close()