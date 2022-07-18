from functools import reduce
from ..view.main_view import MainView
from option import Option, InjectionType, by_file as option_by_file
from ..model.variable import Variable, FixedVariable

class MainController:

    def __init__(self, view : MainView , option=None) -> None:
        self.__view = view
        self.set_option(option)

    def _ask_for_multiple(self, question : str) -> list:
        tmp = " "
        rtr = []
        
        while tmp is not "":
            tmp = self.__view.ask_input(question)
            rtr.append(tmp)
        
        rtr.pop()
        
        return rtr

    def _get_payloads_from_file(filename : str, split_flag="\n") -> list:
        with open(filename, "r") as f:
            return f.read().split(split_flag)

    def _complete_option(self):
        in_type = self.__view.ask_input("what kind of injection would you like to perform ? \n" + InjectionType.URL.value + " : to perform url injection\n" + InjectionType.WEBDRIVER.value + " : to perform web page injection")
        
        in_type = InjectionType(in_type)

        urls = self._ask_for_multiple("Insert an url (hit enter to exit)\n")
        
        if urls is []:
            raise TypeError("A least one url need to be setted")
        
        payloads = self._ask_for_multiple("Inesert path of file that contais payloads (hit enter to exit)\n")
        payloads = list(map(self._get_payloads_from_file, payloads))
        payloads = reduce(lambda x, y: x + y, payloads)

        self.__option = Option(in_type, urls, payloads)

        variables = self._ask_for_multiple("Insert varaible name, and value separed by a space (hit enter to exit)\n")
        variables = list(map(lambda x: x.split(" "), variables))
        variables = list(map(lambda x: Variable(x[0], content=x[1]), variables))
        self.__option.variable = variables

        fixed_varariables = self._ask_for_multiple("Insert fixed varaible name, and value separed by a space (hit enter to exit)\n")
        fixed_varariables = list(map(lambda x: x.split(" "), fixed_varariables))
        fixed_varariables = list(map(lambda x: FixedVariable(x[0], content=x[1]), fixed_varariables))
        self.__option.fixed_variable = fixed_varariables

    def set_option(self, option : Option) -> None:
        if option == None:
            self._complete_option()
        else:
            self.__option = option

    def start_injecting(self):
        pass

def by_file(filename : str, view : MainView) -> MainController:
    return MainController(view, option=option_by_file(filename))