from enum import Enum
from typing_extensions import Self
from PJ.utils.urls import url_parameters, remove_query as remove_params, unparse_url
from PJ.model.variable import FixedVariable, InjectableVariable

class ExportIdentifier(Enum):
    URL = "url"
    INJECTABLE_VARAIBLE = "variables"
    FIXED_VARAIBLE = "Fixed"

class Url:
    def __init__(self, url : str, injectable_varaible : list[InjectableVariable]=[], fixed_variable : list[FixedVariable]=[] ,vars_in_url_are_fixed=True) -> None:
        parameters = url_parameters(url)
        self.__url = remove_params(url)
        self.__fixed_vars = fixed_variable
        self.__variable = injectable_varaible

        if vars_in_url_are_fixed is True:
            for name, value in zip(parameters):
                self.__fixed_vars.append(FixedVariable(name, content=value))
        
        elif vars_in_url_are_fixed is False:
            for name, value in zip(parameters):
                self.__variable.append(InjectableVariable(name))
    
    def inject(self, payload : str) -> str:
        for i in self.__variable:
            i.inject(payload)
        
        return self.__str__
    
    def __str__(self) -> str:
        return unparse_url(self.get_url(), self.get_params())

    def get_url(self) -> str:
        return self.__url

    def get_injectable_list(self) -> list:
        return [x.to_dict() for x in self.__variable]
    
    def get_injectable_dict(self) -> dict:
        rtr = {}
        map(lambda x : rtr.update(x), self.get_injectable_list())
        return rtr
    
    def get_fixed_list(self) -> list:
        return [x.to_dict() for x in self.__fixed_vars]
    
    def get_fixed_dict(self) -> dict:
        rtr = {}
        map(lambda x : rtr.update(x), self.get_fixed_list())
        return rtr

    def get_params(self) -> dict:
        vars = self.get_injectable_dict()
        vars.update(self.get_fixed_dict())
        return vars
    
    def to_dict(self) -> dict:
        return {ExportIdentifier.URL.value : self.__url, ExportIdentifier.INJECTABLE_VARAIBLE.value : self.get_injectable_dict(), ExportIdentifier.FIXED_VARAIBLE.value : self.get_fixed_dict()}

    @classmethod
    def from_dict(raw : dict) -> Self:
        injecatbles = [InjectableVariable(key, content=value) for key, value in raw[ExportIdentifier.INJECTABLE_VARAIBLE.value].items()]
        fixed = [FixedVariable(key, content=value) for key, value in raw[ExportIdentifier.FIXED_VARAIBLE.value].items()]

        return Url(raw[ExportIdentifier.URL], injectable_varaible=injecatbles, fixed_variable=fixed)