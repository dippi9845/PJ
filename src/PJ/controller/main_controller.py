from PJ.controller.option import InjectionType
from PJ.view.main_view import MainView
from option import Option
from option import by_file as option_by_file

class MainController:

    def __init__(self, view : MainView , option=None) -> None:
        self.__view = view
        self.set_option(option)

    def _ask_for_multiple(self, question : str) -> list:
        tmp = " "
        rtr = []
        
        while tmp is not "":
            tmp = input(question)
            rtr.append(tmp)
        
        rtr.pop()
        
        return rtr


    def _complete_option(self):
        in_type = self.__view.ask_input("what kind of injection would you like to perform ? \n" + InjectionType.URL.value + " : to perform url injection\n" + InjectionType.WEBDRIVER.value + " : to perform web page injection")
        in_type = InjectionType(int(in_type))


    def set_option(self, option : Option) -> None:
        if option == None:
            self._complete_option()
        else:
            self.__option = option

    def start_injecting(self):
        pass

def by_file(filename : str, view : MainView) -> MainController:
    return MainController(view, option=option_by_file(filename))