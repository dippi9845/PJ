from PJ.utils.urls import url_parameters, remove_query as remove_params, unparse_url
from PJ.model.variable import FixedVariable, InjectableVariable

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

    def get_injectable(self) -> dict:
        vars = list(map(lambda x: x.to_dict(), self.__variable))
        rtr = {}
        map(lambda x : rtr.update(x), vars)
        return rtr
    
    def get_fixed(self) -> dict:
        vars = list(map(lambda x: x.to_dict(), self.__fixed_vars))
        rtr = {}
        map(lambda x : rtr.update(x), vars)
        return rtr

    def get_params(self) -> dict:
        vars = self.get_injectable()
        vars.update(self.get_fixed())
        return vars
    
    def to_dict(self) -> dict:
        return {"url" : self.__url, "variable" : self.get_injectable(), "fixed" : self.get_fixed()}
