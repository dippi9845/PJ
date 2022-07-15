from PJ.view.main_view import MainView
from option import Option
from option import by_file as option_by_file

class MainController:

    def __init__(self, view : MainView , option=None) -> None:
        self.__view = view
        self.set_option(option)

    def _complete_option(self):
        pass

    def set_option(self, option : Option) -> None:
        if option == None:
            self._complete_option()
        else:
            self.__option = option

    def start_injecting(self):
        pass

def by_file(filename : str, view : MainView) -> MainController:
    return MainController(option_by_file(filename), view)