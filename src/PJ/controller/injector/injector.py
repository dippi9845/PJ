from abc import ABC, abstractmethod
from __future__ import annotations

class Injector(ABC):
    
    @abstractmethod
    def _get_injection(self, index : int) -> str | Injector:
        pass
    
    @abstractmethod
    def _inject_by_index(self, index : int) -> None:
        pass
    
    @abstractmethod
    def inject_all(self) -> None:
        pass

class InjectorIterator:
    def __init__(self, injector : Injector, injection_num : int) -> None:
        self.__injector = injector
        self.__injection_num = injection_num
        self.__index = 0
    
    def _is_over(self) -> bool:
        self.__index < self.__injection_num

    def _get_injector_at_index(self) -> str | Injector:
        return self.__injector._get_injection(self.__index)

    def __next__(self):
        if self._is_over():
            injector = self._get_injector_at_index()
            self.__index += 1
            return injector
        else:
            raise StopIteration
