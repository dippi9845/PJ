from PJ.model.url import Url
from single_url_injector import SingleUrlInjector

class InjectorList:
    def __init__(self, injectors : list[SingleUrlInjector]):
        self.__injectors = injectors

    def __iter__(self):
        return InjectorListIterator(self)

    def inject_all(self):
        for i in self.__injectors:
            i.inject_all()
    
    def split(self, num : int) -> list:
        rtr = [self.__injectors[x:x+num] for x in range(0, len(self.__injectors), num)]
        rtr = [InjectorList(x.copy()) for x in rtr]
        return rtr

class InjectorListIterator:
    def __init__(self) -> None:
        pass
    
    def __iter(self):
        pass

'''
    create an Injector list by values, with payloads different by every Single Url Injector
'''
def by_values(urls : list[Url], payloads : list[str]) -> InjectorList:
    return InjectorList([SingleUrlInjector(x, payloads) for x in urls])
