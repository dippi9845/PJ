from __future__ import annotations
from abc import ABC, abstractmethod
from math import floor
from PJ.model.configuration import INJECTOR_TO_INJECTORTYPE, ExportIdentifier

class Injector(ABC):
    
    def _get_dict_with_type(self):
        return {ExportIdentifier.INJECTOR_TYPE.value: INJECTOR_TO_INJECTORTYPE[type(self)]}
    
    @abstractmethod
    def _get_injection(self, index : int) -> str | Injector:
        pass
    
    @abstractmethod
    def _inject_by_index(self, index : int) -> None:
        pass
    
    @abstractmethod
    def inject_all(self) -> None:
        pass
    
    @abstractmethod
    def to_dict(self) -> dict:
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, dictionary : dict) -> Injector:
        pass

class InjectorIterator:
    def __init__(self, injector : Injector, injection_num : int) -> None:
        self.__injector = injector
        self.__injection_num = injection_num
        self.__index = 0
    
    def _is_over(self) -> bool:
        return self.__index < self.__injection_num

    def _get_injector_at_index(self) -> str | Injector:
        return self.__injector._get_injection(self.__index)

    def __next__(self) -> str | Injector:
        if self._is_over():
            self.__injector._inject_by_index(self.__index)
            rtr = self._get_injector_at_index()
            self.__index += 1
            return rtr
        else:
            raise StopIteration


class InjectorList(Injector):
    def __init__(self, injectors : list[Injector]):
        self.__injectors = injectors

    def __len__(self):
        return len(self.__injectors)

    def __iter__(self):
        return InjectorListIterator(self)
    
    def _inject_by_index(self, index : int) -> None:
        '''
        Can't inject an injector, so do nothing
        '''
        raise NotImplementedError("This function can not be called, it can't be implemented")

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

class InjectorListIterator(InjectorIterator):
    def __init__(self, injector: InjectorList) -> None:
        super().__init__(injector, len(injector))