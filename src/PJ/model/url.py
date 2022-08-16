from __future__ import annotations
from enum import Enum
from PJ.utils.urls import Urls
from PJ.model.variable import FixedVariable, InjectableVariable

class ExportIdentifier(Enum):
    URL = "url"
    INJECTABLE_VARAIBLE = "variables"
    FIXED_VARAIBLE = "Fixed"

class Url:
    def __init__(self, url : str, injectable_varaible : list[InjectableVariable]=[], fixed_variable : list[FixedVariable]=[] ,vars_in_url_are_fixed=True) -> None:
        parameters = Urls.url_parameters(url)
        self.__url = Urls.remove_query(url)
        self.__fixed_vars = fixed_variable.copy()
        self.__variable = injectable_varaible.copy()

        if vars_in_url_are_fixed is True:
            for name, value in parameters.items():
                self.__fixed_vars.append(FixedVariable(name, content=value))
        
        elif vars_in_url_are_fixed is False:
            for name, value in parameters.items():
                self.__variable.append(InjectableVariable(name, content=value))
    
    def inject(self, payload : str) -> str:
        for i in self.__variable:
            i.inject(payload)
        
        return str(self)
    
    def __str__(self) -> str:
        return Urls.unparse_url(self.get_url(), self.get_params())

    def get_url(self) -> str:
        return self.__url
    
    def get_injectable(self) -> dict:
        rtr = {}
        
        for i in self.__variable:
            rtr.update({i.get_variable_name() : i.get_content()})
        
        return rtr
    
    def get_fixed(self) -> dict:
        rtr = {}
        
        for i in self.__fixed_vars:
            rtr.update({i.get_variable_name() : i.get_content()})
        
        return rtr

    def get_params(self) -> dict:
        vars = self.get_injectable()
        vars.update(self.get_fixed())
        return vars
    
    def to_dict(self) -> dict:
        return {
            ExportIdentifier.URL.value : self.__url,
            ExportIdentifier.INJECTABLE_VARAIBLE.value : self.get_injectable(),
            ExportIdentifier.FIXED_VARAIBLE.value : self.get_fixed()
        }

    @classmethod
    def from_dict(cls, raw : dict) -> Url:
        
        if not raw.__contains__(ExportIdentifier.URL.value):
            raise TypeError(f"No key {ExportIdentifier.URL.value} found that specify the actual url to inject")

        if not raw.__contains__(ExportIdentifier.INJECTABLE_VARAIBLE.value):
            raise TypeError(f"No key {ExportIdentifier.INJECTABLE_VARAIBLE.value} found that specify the injectables varaibles")

        if not raw.__contains__(ExportIdentifier.FIXED_VARAIBLE.value):
            raise TypeError(f"No key {ExportIdentifier.FIXED_VARAIBLE.value} found that specify the fixed varaibles")

        injectables = InjectableVariable.from_dict(raw[ExportIdentifier.INJECTABLE_VARAIBLE.value], force_to_list=True)
        fixed = FixedVariable.from_dict(raw[ExportIdentifier.FIXED_VARAIBLE.value], force_to_list=True)
        return cls(raw[ExportIdentifier.URL.value], injectable_varaible=injectables, fixed_variable=fixed)