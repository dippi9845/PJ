from PJ.model.url import Url
from single_url_injector import SingleUrlInjector
from __future__ import annotations
from PJ.controller.injector.injector import Injector, InjectorIterator

class InjectorList(Injector):
    def __init__(self, injectors : list[SingleUrlInjector]):
        self.__injectors = injectors

    def __iter__(self):
        return InjectorListIterator(self)
    
    def _get_injection(self, index : int) -> SingleUrlInjector:
        return self.__injectors[index]

    def inject_all(self):
        for i in self.__injectors:
            i.inject_all()
    
    def split(self, num : int) -> list:
        rtr = [self.__injectors[x:x+num] for x in range(0, len(self.__injectors), num)]
        rtr = [InjectorList(x.copy()) for x in rtr]
        return rtr
    
    @classmethod
    def from_values(urls : list[Url], payloads : list[str]) -> InjectorList:
        '''
        Create an Injector list by values, with payloads different by every Single Url Injector
        '''
        return InjectorList([SingleUrlInjector(x, payloads) for x in urls])


class InjectorListIterator(InjectorIterator):
    def __init__(self, injector: InjectorList) -> None:
        super().__init__(injector, len(injector))



