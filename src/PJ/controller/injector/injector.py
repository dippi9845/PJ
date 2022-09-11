from __future__ import annotations
from abc import ABC, abstractmethod
from math import floor
from typing import Iterable, Iterator

class Injector(ABC):
    
    @abstractmethod
    def __iter__(self) -> Iterator[str | Injector]:
        '''
        return iterator for pyaloads or injector
        '''
        pass
    
    @abstractmethod
    def _inject(self, payload : str) -> None:
        '''
        Inject the given payload to the injector
        '''
        pass
    
    @abstractmethod
    def inject_all(self) -> None:
        '''
        Perform a total injection
        '''
        pass
    
    @abstractmethod
    def to_dict(self) -> dict:
        '''
        Export injector to a dict
        '''
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, dictionary : dict) -> Injector:
        '''
        Build an injector from dict
        '''
        pass

class InjectorIterable:
    def __init__(self, injector : Injector, payloads : Iterable) -> None:
        self.__injector = injector
        self.__iter = payloads

    def __next__(self) -> str | Injector:
        pld = next(self.__iter)
        self.__injector._inject(pld)
        return pld


class InjectorList(Injector):
    def __init__(self, injectors : list[Injector]):
        self.__injectors = injectors

    def __len__(self):
        return len(self.__injectors)

    def __iter__(self):
        return InjectorListIterator(self, iter(self.__injectors))
    
    def _inject(self, payload : int) -> None:
        '''
        Can't inject an injector, so do nothing
        '''
        pass

    def _get_injection(self, index : int) -> Injector:
        return self.__injectors[index]

    def add_injector(self, injector : Injector):
        self.__injectors.append(injector)

    def inject_all(self):
        for i in self.__injectors:
            i.inject_all()
    
    def split(self, num : int) -> list[InjectorList]:
        step = floor(len(self.__injectors)/num)
        rtr = [self.__injectors[x:x+step] for x in range(0, len(self.__injectors), step)]
        rtr = [InjectorList(x.copy()) for x in rtr]
        return rtr
    
    def to_dict(self) -> list[dict]:
        return list(map(lambda i: i.to_dict(), self.__injectors))
    
    @classmethod
    def from_dict(cls, dictionary : list[dict]) -> Injector:
        cls(list(map(lambda x: Injector.from_dict(x), dictionary)))
    

INJECTORLIST_EMPTY = InjectorList([])

class InjectorListIterator(InjectorIterable):
    def __init__(self, injector: InjectorList, payloads : Iterable) -> None:
        super().__init__(injector, payloads)