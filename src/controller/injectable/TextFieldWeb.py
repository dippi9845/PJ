from ..driver.WebDriver import WebDriver
from ....src.model.injectable import TextField
from ..driver import Type

class TextFieldWeb(TextField):
    
    def __init__(self, driver : WebDriver, location : str, type : Type) -> None:
        self.__driver = driver
        self.__element = driver.getElementBy(location, type)
    
    
