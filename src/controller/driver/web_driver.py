from selenium import webdriver
import Type
'''
An abstraction to the selenium web driver
'''
class WebDriver(webdriver):
    '''
    By an existing webdriver
    '''
    def __init__(self, driver=webdriver.Firefox()) -> None:
        self.__driver = driver
    
    def __init__(self, url : str, driver=webdriver.Firefox()) -> None:
        self.__driver = driver
        self.setUrl(url)

    def get_web_driver(self) -> webdriver:
        return self.__driver

    def get_element_by(self, locate : str, type : Type):
        return self.__driver.find_element(type, locate)
    
    def set_url(self, url : str):
        return self.__driver.get(url=url)

    def set_text(self, element, text : str):
        element.send_keys(text)
    
    def click_on_element(self, element):
        element.click()