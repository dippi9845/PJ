import injectable.Injectable as Injectable

class WebPage:

    def __init__(self, URL : str, *injectables : Injectable) -> None:
        self.__URL = URL

        for i in injectables:
            if not isinstance(Injectable):
                raise TypeError("The element " + i + " was not an instance of injectable")

        self.__injectables = list(injectables)
    
    def __init__(self, URL : str, injectables : list) -> None:
        self.__URL = URL

        for i in injectables:
            if not isinstance(Injectable):
                raise TypeError("The element " + i + " was not an instance of injectable")
        
        self.__injectables = injectables
    
    def addIjectable(self, inj : Injectable) -> None:
        self.__injectables.add(inj)
    
    def getInjectables(self) -> dict:
        return dict(self.__injectables)
    
    