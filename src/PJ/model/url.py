from ..utils.urls import url_parameters, remove_query as remove_params, unparse_url
from ..model.variable import FixedVariable, InjectableVariable
from functools import reduce

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
        params = map(lambda x: x.to_dict(), self.__variable) + map(lambda x: x.to_dict(), self.__fixed_vars)
        params = reduce(lambda x,y : x.update(y), params)
        return unparse_url(self.__url, params)
