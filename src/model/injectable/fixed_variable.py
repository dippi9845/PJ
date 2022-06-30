from injectable import Injectable
from ..variable import Variable

''' 
This is a variable that can't be injected anything
'''
class FixedVariable(Injectable, Variable):

    def __init__(self, var_name : str, protocol : str, content="") -> None:
        super().__init__(var_name, protocol, content)