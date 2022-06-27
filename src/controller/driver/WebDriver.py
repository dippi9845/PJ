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
    
    def getWebDriver(self) -> webdriver:
        return self.__driver

    def getElementBy(self, locate : str, type : Type):
        return self.__driver.find_element(type, locate)
    
    def getElementsBy(self, locate : str, type : Type):
        return self.__driver.find_elements(type, locate)
    
    def clickOnElement(self, element):
        element.click()