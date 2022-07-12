class MainController:

    def __init__(self, injection_type : InjectionType) -> None:
        self.__injection_type = injection_type
        self.__urls = []
        self.__payloads = []
    
    def 