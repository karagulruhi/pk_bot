import time
import json

from seleniumwire.utils import decode
from selenium.webdriver.common.by import By


class Login:
    USERNAME = ""
    PASSWORD = ""

    driver = None

    def __init__(self, driver):
        self.driver = driver
        self.USERNAME = "*****"
        self.PASSWORD = "*********"

    def loginSystem(self):
        inputs = self.driver.find_elements(By.TAG_NAME, "input")

        for input in range(len(inputs)):
            if(inputs[input].get_attribute('placeholder') == 'Kullanıcı adınızı girin'):
                userNameInput = inputs[input]
            if(inputs[input].get_attribute('placeholder') == 'Parolanızı girin'):
                passwordInput = inputs[input]

        self.driver.execute_script(
            "arguments[0].setAttribute('value','" + self.USERNAME + "')", userNameInput)
        self.driver.execute_script(
            "arguments[0].setAttribute('value','" + self.PASSWORD + "')", passwordInput)

        loginButton = self.driver.find_element(By.ID, "login")
        loginButton.click()
        time.sleep(1)


        
        for request in self.driver.requests:
            if request.response:
                if(request.url.startswith('**************')):
                    authResponse = json.loads((decode(
                        request.response.body, request.response.headers.get('Content-Encoding', 'identity'))))
                    if(authResponse['error'] == "invalid"):
                        return False
        
        return True
