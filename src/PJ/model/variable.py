from __future__ import annotations
from .injectable import Injectable


class Variable:
    '''
    This class model a varaible in the url
    '''
    def __init__(self, var_name : str, protocol="GET", content="") -> None:
        self.__var_name =  var_name
        self.__protocol = protocol
        self.__content = content
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Variable):
            return self.get_variable_name() == __o.get_variable_name() and self.get_protocol() == __o.get_protocol()

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
    def from_dict(cls, value : dict, force_to_list=False) -> Variable | list[Variable]:
        
        rtr = []
        
        for name, content in value.items():
            rtr.append(cls(name, content=content))

        if len(rtr) == 1 and force_to_list is False:
            return rtr[0]
        else:
            return rtr


class FixedVariable(Injectable, Variable):
    ''' 
    This is a variable that can't be injected anything
    '''
    def __init__(self, var_name : str, protocol="GET", content="") -> None:
        super().__init__(var_name, protocol, content)
    
    def inject(self, payload: str):
        pass

    def _clear(self):
        pass

    @classmethod
    def from_variable(cls, variable : Variable) -> FixedVariable:
        return cls(variable.get_variable_name(), protocol=variable.get_protocol(), content=variable.get_content())
    
    @classmethod
    def from_dict(cls, value : dict, force_to_list=False) -> FixedVariable | list[FixedVariable]:
        rtr = Variable.from_dict(value, force_to_list=force_to_list)
        
        if type(rtr) == list:
            return list(map(lambda x: cls.from_variable(x), rtr))

        else:
            return FixedVariable.from_variable(rtr)


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
    def from_variable(cls, variable : Variable) -> InjectableVariable:
        return cls(variable.get_variable_name(), protocol=variable.get_protocol(), content=variable.get_content())
    
    @classmethod
    def from_dict(cls, value : dict, force_to_list=False) -> InjectableVariable | list[InjectableVariable]:
        rtr = Variable.from_dict(value, force_to_list=force_to_list)
        
        if type(rtr) == list:
            return list(map(lambda x: cls.from_variable(x), rtr))

        else:
            return FixedVariable.from_variable(rtr)
