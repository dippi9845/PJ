from PJ.controller.injector.url.single_url_injector import SingleUrlInjector
from ....model.injectable.injectable_variable import InjectableVariable
from single_url_injector import SingleUrlInjector
from injector_list import InjectorList

class UrlsInjector:

    def __init__(self, urls: list[str], payloads : list[str], vars : list[InjectableVariable], vars_in_url_are_fixed=True, fixed_vars=[]) -> None:
        self.__injectors = map(lambda x: SingleUrlInjector(x, payloads, vars, vars_in_url_are_fixed=vars_in_url_are_fixed, fixed_vars=fixed_vars), urls)
    
    '''
    lo farei pure iterabile
    '''
    
    def inject_all(self):
        for i in self.__injectors:
            i.inject_all()
    
    def split(self, num : int) -> list:
        rtr = [self.__injectors[x:x+num] for x in range(0, len(self.__injectors), num)]
        rtr = map(lambda x: InjectorList(x), rtr)
        return rtr

