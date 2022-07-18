from PJ.model.url import Url
from ....utils.urls import url_request

class SingleUrlInjector:

    def __init__(self, url : Url, payloads : list[str], request: function=url_request) -> None:
        self.__url = url
        self.__payloads = payloads
        self.__request = request
    
    def __iter__(self):
        return SingleUrlInjectorIterator(self)

    def _get_payload(self, index : int) -> str:
        return self.__payloads[index]

    def _get_payload_num(self) -> int:
        return len(self.__payloads)

    '''
    Inject all payloads, to a given url
    '''
    def inject_all(self):
        for payload in self.__payloads:
            self.__url.inject(payload)
            self.__request(self.__url.get_url(), self.__url.get_params())

class SingleUrlInjectorIterator:

    def __init__(self, url_injector : SingleUrlInjector) -> None:
        self.__index = 0
        self.__url_injector = url_injector
    
    def __next__(self) -> str:
        if self.__index < self.__url_injector._get_payload_num():
            payload = self.__url_injector._get_payload(self.__index)
            self.__url_injector._inject_all_variable(payload)
            self.__index += 1
            return payload
        else:
            raise StopIteration