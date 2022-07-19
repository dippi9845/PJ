from functools import reduce
from PJ.model.url import Url
from PJ.view.main_view import MainView
from PJ.model.variable import InjectableVariable, Variable, FixedVariable
from configuration import InjectionType, Configuration, UrlConfiguration, by_file as config_by_file

class MainController:

    def __init__(self, view : MainView , config=None) -> None:
        self.__view = view
        self.set_configuration(config)

    def _ask_for_url_varaible(self, url_question : str, injectable_question : str, fixed_question : str) -> list[Url]:
        url = " "
        rtr = []
        
        while url is not "":
            url = self.__view.ask_input(url_question)
            
            if url is not "":
                injectables = self.__view.ask_for_multiple(injectable_question)
                injectables = [InjectableVariable(i) for i in injectables]

                fixed = self.__view.ask_for_multiple(fixed_question)
                fixed = [i.split(" ") for i in fixed]
                fixed = [FixedVariable(i[0], content=i[1]) for i in fixed]

                rtr.append(Url(url, injectable_varaible=injectables, fixed_variable=fixed))
                
        return rtr
    
    def _get_payloads_from_file(filename : str, split_flag="\n") -> list:
        with open(filename, "r") as f:
            return f.read().split(split_flag)

    def _ask_for_url_injection_type(self):
        name = self.__view.ask_input("Insert the name of the configuration")

        urls = self._ask_for_url_varaible()
        
        ch = self.__view.ask_yes_no("Do you want to insert manually the payloads ? (y/N)")
        payloads = []

        # TODO : completare
        if ch is True:
            pass
        
        payload_files = self.__view.ask_for_multiple("Inesert path of file that contais payloads (hit enter to exit)\n")
        
        if payload_files is [] and payloads is []:
            self.__view.log_error("No payload file and no manual payload, provided")
            self._complete_confguration()
        else:
            return UrlConfiguration(config_name=name, url=urls, payloads=payloads, payload_files=payload_files)
    
    def _complete_confguration(self):
        in_type = self.__view.ask_input("what kind of injection would you like to perform ? \n" + InjectionType.URL.value + " : to perform url injection\n" + InjectionType.WEBDRIVER.value + " : to perform web page injection")
        
        in_type = InjectionType(in_type)

        if in_type is InjectionType.URL:
            self._ask_for_url_injection_type()
            
        elif in_type is InjectionType.WEBDRIVER:
            raise NotImplementedError("still not implemented")

        else:
            raise TypeError("Unknown option")
        

    def set_configuration(self, config : Configuration=None) -> None:
        if config == None:
            self._complete_confguration()
        else:
            self.__config = config

# TODO : completare 
    def start_injecting(self):
        pass

def by_file(filename : str, view : MainView) -> MainController:
    return MainController(view, option=config_by_file(filename))