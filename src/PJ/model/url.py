from ..utils.urls import url_parameters, remove_query as remove_params
from ..model.variable import FixedVariable, Variable
class Url:
    def __init__(self, url : str, injectable_varaible=[], fixed_variable=[] ,vars_in_url_are_fixed=True) -> None:
        parameters = url_parameters(url)
        self.__url = remove_params(url)
        self.__fixed_vars = fixed_variable
        self.__variable = injectable_varaible

        if vars_in_url_are_fixed is True:
            for name, value in zip(parameters):
                self.__fixed_vars.append(FixedVariable(name, content=value))
        
        elif vars_in_url_are_fixed is False:
            for name, value in zip(parameters):
                self.__variable.append(Variable(name))
        
