import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC, select
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup
import difflib
from difflib import SequenceMatcher
from product import Product
from htmlhelper import HtmlHelper
import json
from seleniumwire import webdriver  # Import from seleniumwire
from seleniumwire.utils import decode
from Model.OrderModel import Order
import collections
from collections import OrderedDict




class Sequence:
    driver = None
    product = None
    htmlHelper = None
    id = 0

    def __init__(self, driver, id):
        self.driver = driver
        self.product = Product(driver, id)
        self.htmlHelper = HtmlHelper(driver)
        self.id = id

    def findTrueSquance(self):
        
        allA = self.htmlHelper.getAllA()
        orderList = self.product.getOrderList()
        addingProductList = []
        
        
        #bir tane modelden kaç tane oldugunu bakmaca
        numberofPieces=[]  

        for i in orderList:
            count=0
            for item in orderList:
               if i[:2] ==item[:2]:
                    count+=1
            numberofPieces.append(count)
       
        for idx ,item in enumerate(orderList,start=0):
            addingProductItem = None
            max = 0
            sequence = 0

            for a in allA:
                sequence = SequenceMatcher(None, item[0], a[0]).ratio()
                if sequence > max:
                    max = sequence
                    addingProductItem = [a[0], a[2], item[1], a[1], numberofPieces[idx]]
                    # model--hedr--numara--row--count
            if (addingProductItem != None):
                addingProductList.append(addingProductItem)
               
        return addingProductList

    def addButton(self):
        web = WebDriverWait(self.driver, 60)
        modelList = self.findTrueSquance()
        print(modelList)
        #tamamen aynı ürün sayısını teke düşürmece
        CustomerOrders=[]
        counts = collections.Counter(map(tuple, modelList))
    
        for k in OrderedDict.fromkeys(counts):
            CustomerOrders.append(list(k))
       
        print(CustomerOrders)
        
        modelStr = ""

        
        for i in CustomerOrders:
            modelStr += i[0] + " , "

            xpath_num = ("//*[@id='productsContainer']/div/table/tbody/tr[" +
                         str(i[3])+"]/td[7]/select//option[@value="+str(i[2])+"]")
            xpath_piece=(
                    "//*[@id='productsContainer']/div/table/tbody/tr["+str(i[3])+"]/td[8]/select//option[@value="+str(i[4])+"]")
            xpath_add = (
                "//*[@id='productsContainer']/div/table/tbody/tr["+str(i[3])+"]/td[9]/button")         
            if i[4]>1:
                
        
                web.until(EC.visibility_of_element_located(
                (By.XPATH, xpath_num))).click()  
                
                time.sleep(2)
                
                web.until(EC.visibility_of_element_located(
                (By.XPATH, xpath_piece))).click()
                
                time.sleep(2)
                
                web.until(EC.visibility_of_element_located(
                (By.XPATH, xpath_add))).click()
            else:
                
                web.until(EC.visibility_of_element_located(
                (By.XPATH, xpath_num))).click()

                time.sleep(2)
                
                web.until(EC.visibility_of_element_located(
                (By.XPATH, xpath_add))).click()

        web.until(EC.visibility_of_element_located(
                (By.XPATH, """//*[@id="productsContainer"]/a"""))).click()
        time.sleep(1)
        web.until(EC.visibility_of_element_located(
                (By.XPATH, """//*[@id="createOrderWizardCompleteButton"]"""))).click()
        for request in self.driver.requests:
            if request.response:
                if(request.url.startswith('***********************')):
                    addingProductResponse = json.loads((decode(
                        request.response.body, request.response.headers.get('Content-Encoding', 'identity'))))
                    if(addingProductResponse['result']['saleId']):
                        query = (Order
                                .update({Order.PanelId: addingProductResponse['result']['saleId'], Order.IsComplete: True, Order.PanelProduct: modelStr})
                                .where(Order.Id == self.id))
                        query.execute()
        time.sleep(3)
