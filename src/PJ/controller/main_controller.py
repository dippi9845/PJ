from enum import Enum

class InjectionType(Enum):
    URL = 1
    WEBDRIVER = 2

class MainController:

    def __init__(self, injection_type : InjectionType) -> None:
        self.__injection_type = injection_type
    
    def 