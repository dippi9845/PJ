from injectable import Injectable
from __future__ import annotations


class Variable:
    '''
    This class model a varaible in the url
    '''
    def __init__(self, var_name : str, protocol="GET", content="") -> None:
        self.__var_name =  var_name
        self.__protocol = protocol
        self.__content = content
    
    def _set_content(self, content : str) -> None:
        self.__content = content

    def get_protocol(self) -> str:
        return self.__protocol
    
    def get_variable_name(self) -> str:
        return self.__var_name

    def get_content(self) -> str:
        return self.__content
    
    def to_dict(self) -> dict:
        return {self.__var_name : self.__content}

    @classmethod
    def from_dict(value : dict) -> Variable | list[Variable]:
        
        rtr = []
        
        for name, content in value.items():
            rtr.append(Variable(name, content=content))

        if len(rtr) == 1:
            return rtr[0]
        else:
            return rtr


class FixedVariable(Injectable, Variable):
    ''' 
    This is a variable that can't be injected anything
    '''
    def __init__(self, var_name : str, protocol="GET", content="") -> None:
        super().__init__(var_name, protocol, content)

    @classmethod
    def from_variable(variable : Variable) -> FixedVariable:
        return FixedVariable(variable.get_variable_name(), protocol=variable.get_protocol(), content=variable.get_content())


class InjectableVariable(Injectable, Variable):
    '''
    A variable that can be injected a payload
    '''
    def __init__(self, var_name : str, protocol="GET", content="") -> None:
        super().__init__(var_name, protocol, content)

    def _clear(self) -> None:
        self._set_content("")

    def inject(self, payload : str) -> None:
        self._set_content(payload)

    @classmethod
    def from_variable(variable : Variable) -> InjectableVariable:
        return InjectableVariable(variable.get_variable_name(), protocol=variable.get_protocol(), content=variable.get_content())
