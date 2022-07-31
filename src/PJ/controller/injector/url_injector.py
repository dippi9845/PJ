from __future__ import annotations
from PJ.model.url import Url
from PJ.utils.urls import get_request
from PJ.controller.injector.injector import Injector, InjectorIterator, InjectorList

class SingleUrlInjector(Injector):

    def __init__(self, url : Url, payloads : list[str], request: function=get_request) -> None:
        self.__url = url
        self.__payloads = payloads
        self.__request = request
    
    def get_url(self) -> str:
        return self.__url.get_url()

    def __iter__(self) -> SingleUrlInjectorIterator:
        return SingleUrlInjectorIterator(self)
    
    def __len__(self) -> int:
        return len(self.__payloads)

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
    
    @classmethod
    def from_values(urls : list[Url], payloads : list[str]) -> InjectorList:
        '''
        Create an Injector list by values, with payloads different by every Single Url Injector
        '''
        return InjectorList([SingleUrlInjector(x, payloads) for x in urls])


class SingleUrlInjectorIterator(InjectorIterator):
    def __init__(self, url_injector: SingleUrlInjector) -> None:
        super().__init__(url_injector, len(url_injector))
