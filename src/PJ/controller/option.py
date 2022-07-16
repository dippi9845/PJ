from enum import Enum
from ..model.variable import FixedVariable, InjectableVariable, Variable, from_dict
from json import loads

class InjectionType(Enum):
    URL = 1
    WEBDRIVER = 2

class Option:
    def __init__(self, injection_type : InjectionType, url, payloads : list[str]) -> None:
        self.__injection_type = injection_type
        self.url = url
        self.payloads = payloads

        if self.__injection_type is InjectionType.URL:
            self.variable = []
            self.fixed_variable = []
        
        elif self.__injection_type is InjectionType.WEBDRIVER:
            pass
            
        else:
            raise TypeError("Type of injection is not valid, or supported")
        

    def add_url(self, url : str) -> None:
        if type(self.url) is str:
            self.url = [self.url, url]
        
        elif type(self.url) is list:
            self.url.append(url)

        else:
            raise TypeError("Unsupported url type")
    
    def add_variable(self, var : Variable) -> None:
        
        if type(var) is InjectableVariable:
            self.variable.append(var)
        
        elif type(var) is FixedVariable:
            self.fixed_variable.append(var)
        
        else:
            raise TypeError("this variable is not supported")
    
    def to_dict(self) -> dict:
        if self.__injection_type is InjectionType.URL:
            variable = map(lambda x: x.to_dict(), self.variable)
            fixed_variable = map(lambda x: x.to_dict(), self.fixed_variable)

            rtr = self.__dict__
            rtr["variable"] = variable
            rtr["fixed_variable"] = fixed_variable

            return rtr

        elif self.__injection_type is InjectionType.WEBDRIVER:
            pass
            

def by_file(filename : str) -> Option:
    with open(filename, "r") as f:
        data = loads(f.read())
        tmp = Option(data["injection_type"], data["url"], data["payloads"])
        
        if int(data["injection_type"]) is InjectionType.URL.value:
            
            tmp.variable = map(from_dict, data["variable"])
            tmp.fixed_variable = map(from_dict, data["fixed_variable"])

            return tmp
        
        elif int(data["injection_type"]) is InjectionType.WEBDRIVER.value:
            pass
        
