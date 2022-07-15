from enum import Enum
from ..model.variable import FixedVariable, InjectableVariable, Variable
from ..model.variable import from_dict
from json import loads

class InjectionType(Enum):
    URL = 1
    WEBDRIVER = 2

class Option:
    def __init__(self, injection_type : InjectionType, url, payloads : list[str]) -> None:
        self.injection_type = injection_type
        self.url = url
        self.payloads = payloads

        if self.injection_type == InjectionType.URL:
            self.variable = []
            self.fixed_variable = []

    def add_url(self, url : str) -> None:
        if type(self.url) == str:
            self.url = [self.url, url]
        
        elif type(self.url) == list:
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
    with open(filename, "r") as f:
        data = loads(f.read())
        
        if data["injection_type"] == InjectionType.URL:
            tmp = Option(data["injection_type"], data["url"], data["payloads"])
            
            tmp.variable = map(from_dict, data["variable"])
            tmp.fixed_variable = map(from_dict, data["fixed_variable"])


        
        elif data["injection_type"] == InjectionType.WEBDRIVER:
            pass
        
        else:
            raise TypeError("value of injection_type is not recognised")