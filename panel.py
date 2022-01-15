import time
from typing import Text
from playhouse.shortcuts import *
from Model.OrderModel import Order
from login import Login
from product import Product
from sequence import Sequence
from driver import Driver

from datetime import datetime

def panel():
    unPaneledList = Order.select().where(Order.IsComplete == False)

    if(unPaneledList.count() > 0):

        chromeDriver = Driver()
        chromeDriver.maximizeWindow()
        chromeDriver.getWindow()
        login = Login(chromeDriver.driver)

        if(login.loginSystem()):
            for unPanaledOrder in unPaneledList:

                product = Product(chromeDriver.driver, unPanaledOrder)
                product.getOrderList()
                sequence = Sequence(chromeDriver.driver, unPanaledOrder)
  

                time.sleep(3)

                product.openOrderPopup()
                product.pasteOrderText()
                time.sleep(2)
                sequence.addButton()
                time.sleep(1)
            chromeDriver.close()
            print('Sistemi kapattık!')

        else:
            print('Sisteme giriş sağlanamadı!')

    else:
        print("Sipariş adedi 3'dan fazla olmadığı için başlayamadık!..Eklediğiniz Sipariş Sayısı : {}".format(unPaneledList.count()))
