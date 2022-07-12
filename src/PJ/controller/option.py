from enum import Enum
from PJ.model.variable import FixedVariable, InjectableVariable, Variable

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

    def add_url(self, url : str) -> None:
        if type(self.url) == str:
            self.url = [self.url, url]
        
        elif type(self.url) == list[str]:
            self.url.append(url)

        else:
            raise TypeError("Unsupported url type")
    
    def add_variable(self, var : Variable) -> None:
        
        if type(var) == InjectableVariable:
            self.variable.append(var)
        
        elif type(var) == FixedVariable:
            self.fixed_variable.append(var)
        
        else:
            raise TypeError("this variable is not supported")
    
    def to_dict(self) -> dict:
        pass

def by_file(filename : str) -> Option:
    pass