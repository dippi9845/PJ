from injectable import Injectable

class Variable(Injectable):

    def __init__(self, varName : str, protocol : str, content="", variable=False):
        self.__varName =  varName
        self.__protocol = protocol
        self.__content = content
        self.__isVariable = variable
    
    def __str__(self):
        return self.__varName + "=" + self.__content
    
    def get_variable_name(self):
        return self.__varName
    
    def get_protocol(self):
        return self.__protocol
    
    def is_varaible(self):
        return self.__isVariable
    
    def get_content(self):
        return self.__content

    def _clear(self):
        self.__content = ""

    def inject(self, payload : str):
        if self.__variable == True:
            self._clear()
            self.__content = payload
    
