from ....model.variable import InjectableVariable
from functools import reduce
import urls

class SingleUrlInjector:

    def __init__(self, url: str, payloads : list[str], vars : list[InjectableVariable], vars_in_url_are_fixed=True, fixed_vars=[], request=urls.url_request) -> None:
        self.__url = url
        self.__payloads = payloads
        self.__vars = vars
        self.__fixed_vars = fixed_vars
        self.__request = request
    
    def __iter__(self):
        return SingleUrlInjectorIterator(self)

    def _get_payload(self, index : int):
        return self.__payloads[index]

    def _inject_all_variable(self, payload : str) -> None:
        for var in self.__vars:
            var.inject(payload)

    '''
    Inject all payloads, to a given url
    '''
    def inject_all(self):
        # TODO: __inject_all_variable non è definita
        for payload in self.__payloads:
            self.__inject_all_variable(payload)
            
            dicts = map(lambda x: x.to_dict(), self.__vars) + map(lambda x: x.to_dict(), self.__fixed_vars)
            params = reduce(lambda x,y : x.update(y), dicts)

            self.__request(self.url, params)

class SingleUrlInjectorIterator:

    def __init__(self, url_injector : SingleUrlInjector) -> None:
        self.__index = 0
        self.__url_injector = url_injector
    
    def __next__(self) -> str:
        # TODO: self.__payloads non è definita
        if self.__index < len(self.__payloads):
            payload = self.__url_injector._get_payload(self.__index)
            self.__url_injector._inject_all_variable(payload)
            self.__index += 1
            return payload
        else:
            raise StopIteration