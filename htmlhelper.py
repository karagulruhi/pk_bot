import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC, select
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup


class HtmlHelper:
    driver = None

    def __init__(self, driver):
        self.driver = driver

    def getHtmlElementByXPath(self, xpath):
        return self.driver.find_element(By.XPATH, xpath)

    def convertHtmlToSoup(self, htmlElement):
        return BeautifulSoup(htmlElement.get_attribute('innerHTML'), "html.parser")

    def findAllElement(self, soupElement, findingElement, attrs={}):
        return soupElement.find_all(findingElement, attrs)

    def getAllA(self):
        productsContainerText = self.getHtmlElementByXPath(
            '//*[@id="productsContainer"]/div/table')
        productContainerHtml = self.convertHtmlToSoup(
            productsContainerText)

        allA = []

        for idx, i in enumerate(self.findAllElement(productContainerHtml, 'tr'), start=0):
            for k in self.findAllElement(i, 'td'):
                for q in self.findAllElement(k, 'a', {'target': '_blank'}):
                    allA.append([q.text, idx, q["href"]])

        return allA
