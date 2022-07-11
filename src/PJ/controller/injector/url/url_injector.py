from PJ.model.variable import Variable
from ....model.injectable.injectable import Injectable
from ....model.injectable.fixed_variable import FixedVariable
from ....model.injectable.injectable_variable import InjectableVariable

class UrlInjector:

    def __init__(self, urls: list[str], payloads : list[str], vars : list[InjectableVariable], vars_in_url_are_fixed=True, fixed_vars=[]) -> None:
        self.__urls = urls
        self.__payloads = payloads
        self.__vars = vars
        self.__fixed_vars = fixed_vars
    
    '''
    lo farei pure iterabile
    '''

    def __inject_all_variable(self, payload : str) -> None:
        for var in self.__vars:
            var.inject(payload)

    '''
    Inject all payloads
    '''
    def inject_all(self):
        for payload in self.__payloads:
            self.__inject_all_variable(payload)