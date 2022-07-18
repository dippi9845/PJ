from cProfile import run
from enum import Enum
from PJ.model.variable import FixedVariable, InjectableVariable, Variable, from_dict
from json import loads
from PJ.model.url import Url

'''
Da rifare tutto:
    option ora contiene:
        1) i vari file dei payload
        2) i vari file dove trovare gli oggetti da iniettare Url
        3) quanti threa creare per l'iniezione
    
    option deve essere esportabile via file

'''

class InjectionType(Enum):
    URL = "1"
    WEBDRIVER = "2"

class Configuration:
    def __init__(self, config_name : str="Default Config", injection_type : InjectionType=InjectionType.URL, url : list[Url]=[], payloads : list[str]=[]) -> None:
        self.config_name = config_name
        self.injection_type = injection_type
        self.url = url
        self.payloads = payloads
        

    def add_url(self, url : str) -> None:
        self.url.append(url)
    
    def add_variable(self, var : Variable) -> None:
        
        if type(var) is InjectableVariable:
            self.variable.append(var)
        
        elif type(var) is FixedVariable:
            self.fixed_variable.append(var)
        
        else:
            raise TypeError("this variable is not supported")
    
    def to_dict(self) -> dict:
        if self.injection_type is InjectionType.URL:
            variable = map(lambda x: x.to_dict(), self.variable)
            fixed_variable = map(lambda x: x.to_dict(), self.fixed_variable)

            rtr = self.__dict__
            rtr["variable"] = variable
            rtr["fixed_variable"] = fixed_variable

            return rtr

        elif self.injection_type is InjectionType.WEBDRIVER:
            pass
            

def by_file(filename : str) -> Configuration:
    with open(filename, "r") as f:
        data = loads(f.read())
        tmp = Configuration(data["injection_type"], data["url"], data["payloads"])
        
        if data["injection_type"] is InjectionType.URL.value:
            
            tmp.variable = map(from_dict, data["variable"])
            tmp.fixed_variable = map(from_dict, data["fixed_variable"])

            return tmp
        
        elif data["injection_type"] is InjectionType.WEBDRIVER.value:
            pass
        
