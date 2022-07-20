from abc import ABC, abstractmethod

class Injectable(ABC):
    '''
    An interface that model a whatever thing that can be injected a payload
    '''

    @abstractmethod
    def _clear():
        '''
        Clear the value in the injectable
        '''
        pass

    @abstractmethod
    def inject(payload : str):
        '''
        inject the given payload
        '''
        pass
