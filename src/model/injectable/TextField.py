import Injectable
'''
This class in not instantiable, need to be defined _clear and inject,
in the controller, couse is up to the controller how to inject the
payload inside the web page, and how to clear that
'''
class TextField(Injectable):
    def __init__(self, path : str, type : str):
        self.__path = path
        self.__type = type
    
    def getPath(self):
        return self.__path
    
    def getType(self):
        return self.__type

    def _clear():
        pass

    def inject(payload : str):
        pass

