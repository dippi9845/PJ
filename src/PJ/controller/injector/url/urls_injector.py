from PJ.controller.injector.url.single_url_injector import SingleUrlInjector
from ....model.injectable.injectable_variable import InjectableVariable
from single_url_injector import SingleUrlInjector

class UrlsInjector:

    def __init__(self, urls: list[str], payloads : list[str], vars : list[InjectableVariable], vars_in_url_are_fixed=True, fixed_vars=[]) -> None:
        self.__urls = map(lambda x: SingleUrlInjector(x, payloads, vars, vars_in_url_are_fixed=vars_in_url_are_fixed, fixed_vars=fixed_vars), urls)
    
    '''
    lo farei pure iterabile
    '''
    
    def inject_all(self):
        for i in self.__urls:
            i.inject_all()
