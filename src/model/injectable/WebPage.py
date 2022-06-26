import Injectable

class WebPage:

    def __init__(self, URL : str, *injectables : Injectable) -> None:
        self.__URL = URL
        self.__injectables = list(injectables)
    
    def __init__(self, URL : str, injectables : list) -> None:
        self.__URL = URL

        for i in injectables:
            if not isinstance(Injectable):
                raise TypeError("The element " + i + " was not an instance of injectable")
        
        self.__injectables = injectables
    
    