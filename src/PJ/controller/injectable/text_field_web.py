from ..driver.web_driver import WebDriver
from ...model.injectable import text_field
from ..driver import type

class TextFieldWeb(text_field):
    
    def __init__(self, driver : WebDriver, location : str, type : type) -> None:
        self.__driver = driver
        self.__element = driver.getElementBy(location, type)
    

