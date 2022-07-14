from PJ.view.main_view import MainView
from option import Option
from option import by_file as option_by_file

class MainController:

    def __init__(self, run : Option, view : MainView) -> None:
        self.set_option(run)
        self.__view = view
    
    def complete_option():
        pass

    def set_option(self, run : Option) -> None:
        self.__run = run

    def start_injecting(self):
        pass

def by_file(filename : str, view : MainView) -> MainController:
    return MainController(option_by_file(filename), view);