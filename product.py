import time
import pyperclip 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from Model.OrderModel import Order
from playhouse.shortcuts import *
import math


class Product:
    driver = None
    orderText = None
    id = 0

    starting_point = 5

    def __init__(self, driver, id):
        self.driver = driver
        self.id = id
        order = Order.select().where(Order.Id == id).get()
        self.orderText = (model_to_dict(order)['OrderText'])

    def openOrderPopup(self):
        newOrderButton = self.driver.find_element(By.XPATH, '//*[@id="page"]/div/div[2]/div/div[1]/a')
        newOrderButton.click()
        time.sleep(1)

    def pasteOrderText(self):
        pasteArea = self.driver.find_element(By.ID, 'pasteDataSensationArea')

        time.sleep(1)
        pyperclip.copy(self.getOrderText())
        time.sleep(1)
        pasteArea.send_keys(Keys.CONTROL, 'v')

    def getOrderText(self):
        return str(self.orderText)

    def getOrderSplitText(self):
        orderSplit = str(self.orderText).splitlines()
        return orderSplit

    def getOrderList(self):
        orderSplit = ''.join(self.orderText).splitlines()
        productList = []

        isShoesNumberLastLime = False
        lastShoesNumber = 0
        
        try:
            lastShoesNumber = math.ceil((float(orderSplit[-1].replace(" ", ""))))
            isShoesNumberLastLime = True 
        except:
            isShoesNumberLastLime = False
        
        for idx, i in enumerate(orderSplit, start = 0):
            if(idx > self.starting_point):
                addProduct = None
                if i == orderSplit[-1] and isShoesNumberLastLime:
                    break
                if isShoesNumberLastLime:
                    addProduct = [i, lastShoesNumber, idx]
                else:
                    x=i.replace(" ", "")
                    y=(x[-2:])
                    z=(x[-4:])
                    if(y == ".5"):
                        addProduct = [i.replace(z, "").replace(" ", "").rstrip(), math.ceil(float(z)),idx]
                    else:
                        addProduct = [i.replace(y, "").replace(" ", "").rstrip(), y,idx]
                    
                productList.append(addProduct)

        return productList