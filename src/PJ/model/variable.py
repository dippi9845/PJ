'''
This class model a varaible in the url
'''
class Variable:

    def __init__(self, var_name : str, protocol : str, content="", value_setter="=") -> None:
        self.__var_name =  var_name
        self.__protocol = protocol
        self.__content = content
        self.__value_setter = value_setter
    
    def _set_content(self, content : str) -> None:
        self.__content = content

    def get_protocol(self) -> str:
        return self.__protocol
    
    def get_variable_name(self) -> str:
        return self.__var_name

    def get_content(self) -> str:
        return self.__content
    
    def __str__(self) -> str:
        return self.__var_name + self.__value_setter + self.__content