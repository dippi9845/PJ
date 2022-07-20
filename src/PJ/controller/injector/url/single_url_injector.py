from PJ.model.url import Url
from PJ.utils.urls import url_request

# TODO : use injector

class SingleUrlInjector:

    def __init__(self, url : Url, payloads : list[str], request: function=url_request) -> None:
        self.__url = url
        self.__payloads = payloads
        self.__request = request
    
    def get_url(self) -> str:
        return self.__url.get_url()

    def __iter__(self):
        return SingleUrlInjectorIterator(self)

    def _get_payload(self, index : int) -> str:
        '''
        Returns the payload at the given position
        '''
        return self.__payloads[index]

    def _get_payload_num(self) -> int:
        '''
        Return the number of payloads stored
        '''
        return len(self.__payloads)

    def _inject_payload(self, payload : str):
        '''
        Inject to url the given, the specified payload
        '''
        self.__url.inject(payload)
    
    def _inject_by_index(self, payload_inedex : int):
        '''
        Inject the payload, in the position given by the parameter
        '''
        self.__url.inject(self._get_payload(payload_inedex))

    def inject_all(self):
        '''
        Inject all payloads, to a given url
        '''
        for payload in self.__payloads:
            self.__url.inject(payload)
            self.__request(self.__url.get_url(), self.__url.get_params())

class SingleUrlInjectorIterator:

    def __init__(self, url_injector : SingleUrlInjector) -> None:
        self.__index = 0
        self.__url_injector = url_injector
    
    def __is_over(self) -> bool:
        self.__index < self.__url_injector._get_payload_num()
    
    def __get_payload_at_index(self) -> SingleUrlInjector:
        return self.__url_injector._get_payload(self.__index)

    def __inject(self, payload : str) -> None:
        self.__url_injector._inject_payload(payload)

    def __next__(self) -> str:
        if self.__is_over():
            payload = self.__get_payload_at_index()
            self.__inject(payload)
            self.__index += 1
            return payload
        else:
            raise StopIteration