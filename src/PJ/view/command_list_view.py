from __future__ import annotations
from main_view import MainView

class CommandListView(MainView):
    
    def __init__(self, commands : list[str]) -> None:
        super().__init__()
        self.__commands = commands
    
    def add_command(self, command : str) -> None:
        self.__commands.append(command)
    
    
    def _get_next_command(self) -> str:
        return self.__commands.pop(0)
    
    
    def introduction(self):
        pass
    
    
    def ask_input(self, string : str) -> str:
        return self._get_next_command()
    
    
    def log(self, string : str, end='\n'):
        pass
    
    
    def ask_for_multiple(self, message: str, elements : list) -> dict:
        rtr = {}
        
        for i in elements:
            rtr[i] = self._get_next_command()
        
        return rtr
    
    
    def menu(self, message: str, choices: list[str], descriptions: list[str]) -> str:
        cmd = self._get_next_command()
        if cmd in choices: return cmd
        else: raise ValueError(f"Command {cmd} not valid")
    
    
    @classmethod
    def from_string(cls, string : str, separetor : str=" ") -> CommandListView:
        return cls(string.split(separetor))