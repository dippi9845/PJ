from enum import Enum

class InjectionType(Enum):
    URL = 1
    WEBDRIVER = 2

class Option:
    def __init__(self, injection_type : InjectionType, url : str) -> None:
        self.injection_type = injection_type
        self.url = url
        self.variable = []
        self.fixed_variable = []
        