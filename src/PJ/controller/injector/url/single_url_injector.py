from PJ.model.variable import Variable
from ....model.injectable.injectable import Injectable
from ....model.injectable.fixed_variable import FixedVariable
from ....model.injectable.injectable_variable import InjectableVariable
from functools import reduce
from ..url import urls

class SingleUrlInjector:

    def __init__(self, url: str, payloads : list[str], vars : list[InjectableVariable], vars_in_url_are_fixed=True, fixed_vars=[], request=urls.url_request) -> None:
        self.__url = url
        self.__payloads = payloads
        self.__vars = vars
        self.__fixed_vars = fixed_vars
        self.__request = request
    
    '''
    lo farei pure iterabile
    '''

    def __inject_all_variable(self, payload : str) -> None:
        for var in self.__vars:
            var.inject(payload)

    '''
    Inject all payloads, to a given url
    '''
    def inject_all(self):
        for payload in self.__payloads:
            self.__inject_all_variable(payload)
            
            dicts = map(lambda x: x.to_dict(), self.__vars) + map(lambda x: x.to_dict(), self.__fixed_vars)
            params = reduce(lambda x,y : x.update(y), dicts)

            self.__request(self.url, params)