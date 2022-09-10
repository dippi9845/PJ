from __future__ import annotations
from enum import Enum
from PJ.model.url import Url
from PJ.utils.urls import Urls
from PJ.controller.injector.injector import Injector, InjectorIterable, InjectorList
from typing import Callable, Iterable

class ExportUtils(Enum):
    PAYLOADS = "Payloads"
    URL = "Url"
    REUQEST_TYPE = "Request"
    
    POST_REQUEST = "POST"
    GET_REQUEST = "GET"
    
    REQUESTS_FUNC = {GET_REQUEST: Urls.get_request, POST_REQUEST : Urls.post_request}
    FUNC_REQUESTS = {Urls.get_request: GET_REQUEST, Urls.post_request: POST_REQUEST}

class UrlInjector(Injector):

    def __init__(self, url : Url, payloads : Iterable[str], request: Callable=Urls.get_request) -> None:
        self.__url = url
        self.__payloads = payloads
        self.__request = request
    
    def get_url(self) -> str:
        return self.__url.get_url()

    def __iter__(self) -> UrlInjectorIterable:
        return UrlInjectorIterable(self)
    
    def _inject(self, payload : str):
        '''
        Inject the payload, in the position given by the parameter
        '''
        self.__url.inject(payload)
        self.__request(self.__url.get_url(), self.__url.get_params())

    def inject_all(self):
        '''
        Inject all payloads, to a given url
        '''
        for payload in self.__payloads:
            self.__url.inject(payload)
            self.__request(self.__url.get_url(), self.__url.get_params())
    
    def to_dict(self):
        return {
            ExportUtils.PAYLOADS.value : self.__payloads,
            ExportUtils.URL.value : self.__url.to_dict(),
            ExportUtils.REUQEST_TYPE.value: ExportUtils.FUNC_REQUESTS.value[self.__request]
        }
    
    @classmethod
    def from_dict(cls, dictionary: dict) -> Injector:
        return cls(Url.from_dict(dictionary[ExportUtils.URL.value]), dictionary[ExportUtils.PAYLOADS.value], request=ExportUtils.REQUESTS_FUNC.value[dictionary[ExportUtils.REUQEST_TYPE.value]])
    
    @classmethod
    def from_values(cls, urls : list[Url], payloads : list[str]) -> InjectorList:
        '''
        Create an Injector list by values, with payloads different by every Single Url Injector
        '''
        return InjectorList([cls(x, payloads) for x in urls])


class UrlInjectorIterable(InjectorIterable):
    def __init__(self, url_injector: UrlInjector, payloads : Iterable) -> None:
        super().__init__(url_injector, payloads)
