from single_url_injector import SingleUrlInjector

class InjectorList:
    def __init__(self, injectors : list[SingleUrlInjector]):
        self.__injectors = injectors

    def inject_all(self):
        for i in self.__injectors:
            i.inject_all()