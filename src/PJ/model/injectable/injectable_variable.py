from injectable import Injectable
from ..variable import Variable

class InjectableVariable(Injectable, Variable):
    def __init__(self, var_name : str, protocol : str, content="") -> None:
        super().__init__(var_name, protocol, content)

    def _clear(self) -> None:
        self._set_content("")

    def inject(self, payload : str) -> None:
        self._set_content(payload)
    
