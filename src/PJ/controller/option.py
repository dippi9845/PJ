from enum import Enum

class InjectionType(Enum):
    URL = 1
    WEBDRIVER = 2

class Option:
    def __init__(self, injection_type : InjectionType, url : str) -> None:
        self.injection_type = injection_type
        self.url = url

        if self.injection_type == InjectionType.URL:
            self.variable = []
            self.fixed_variable = []

    def add_url(self, url : str):
        if type(self.url) == str:
            self.url = [self.url, url]
        
        elif type(self.url) == list[str]:
            self.url.append(url)

        else:
            raise TypeError("Unsupported url type")