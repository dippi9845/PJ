from abc import ABC, abstractmethod

'''
An interface that model a whatever thing that can be injected a payload
'''
class Injectable(ABC):

    @abstractmethod
    def _clear():
        pass

    @abstractmethod
    def inject(payload : str):
        pass
