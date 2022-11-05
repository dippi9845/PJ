from __future__ import annotations
from enum import Enum
from PJ.controller.injector.injector import Injector
from PJ.controller.injector.url_injector import UrlInjector
from PJ.view.main_view import MainView
from PJ.model.configuration import Configuration, InjectionType
from PJ.model.url import Url
from PJ.model.variable import Variable, FixedVariable
from typing import Optional

class Commands(Enum):
    ADD_GLOBAL_PAYLOAD = "Add Global Payload"
    ADD_GLOBAL_PAYLOAD_FILE = "Add Global Payload File"
    ADD_INJECTOR = "Add Injector"
    LOAD_PAYLOADS_FROM_FILE = "Load Payloads"
    START_INJECTING = "Run"
    INJECT_ALL = "Inject all"
    EXIT = "Exit"

class MainController:

    def __init__(self, view : MainView , config : Optional[Configuration]=None) -> None:
        self.__view = view
        self.__config = Configuration() if config is None else config
        
        self.cmds = {
            Commands.ADD_GLOBAL_PAYLOAD.value : self.add_global_payload_cmd,
            Commands.ADD_GLOBAL_PAYLOAD_FILE.value : self.add_global_payload_file_cmd,
            Commands.ADD_INJECTOR.value : self.add_injector_cmd,
            Commands.LOAD_PAYLOADS_FROM_FILE.value : self.load_payloads_from_file,
            Commands.START_INJECTING.value : self.start_injecting,
            Commands.INJECT_ALL.value : self.inject_all,
            Commands.EXIT.value: self.exit
        }
        
        self.description = {
            Commands.ADD_GLOBAL_PAYLOAD.value : "add to global list a payload",
            Commands.ADD_GLOBAL_PAYLOAD_FILE.value : "add a file global list of file that contains payloads",
            Commands.ADD_INJECTOR.value : "add an injector to the current configuration",
            Commands.LOAD_PAYLOADS_FROM_FILE.value : "move all payoads from the added global file, to global payloads",
            Commands.START_INJECTING.value : "start injection with logs",
            Commands.INJECT_ALL.value : "same as start injection but with no log",
            Commands.EXIT.value : "for close"
        }
        
        self.injectors = {
            InjectionType.URL.value : self._build_url_injector
        }
        
        self.main_menu()
    
    
    def main_menu(self):
        cmds = [x.value for x in Commands]
        desc = list(map(lambda x: self.description[x], cmds))
        ch = ""
        
        while ch != Commands.EXIT.value:
            ch = self.__view.menu("Select the main commands", cmds, desc)
            self.cmds[ch]()
        
    
    def add_global_payload_cmd(self):
        types = [InjectionType.URL.value, InjectionType.WEBDRIVER.value]
        descs = ["Injection by url variables", "Injection by automating the web browser"]
        
        key = self.__view.menu("Which kind of payload you want to add", types, descs)
        paylaod = self.__view.ask_input("Insert the payload")
        
        self._add_global_payload(key, paylaod)
        
    
    def add_global_payload_file_cmd(self):
        types = [InjectionType.URL.value, InjectionType.WEBDRIVER.value]
        descs = ["Injection by url variables", "Injection by automating the web browser"]
        
        key = self.__view.menu("Which kind of payload file you want to add", types, descs)
        paylaod_file = self.__view.ask_input("Insert the payload file")
        
        self._add_global_payload_file(key, paylaod_file)
    
    
    def add_injector_cmd(self):
        injcetors = [InjectionType.URL.value]
        desc = ["Injector using url variables"]
        
        injector_str = self.__view.menu("Which kind of payload file you want to add", injcetors, desc)
        injector = self.injectors[injector_str]()
        self._add_injector(injector)
    
    
    def _build_url_injector(self) -> UrlInjector:
        url = self.__view.ask_input("Insert the url to inject")
        
        variables = []
        fixed = []
        ch = None
        
        while ch is None or ch != "":
            ch = self.__view.ask_yes_no("Do you want to add a variable to the url ?")
            if ch == "y":
                type_v = self.__view.menu("Insert the type of the variable", ["f", "v"], ["Fixed varaible which is needed to be here", "Variable that is going to be injected"])
                name = self.__view.ask_input("Insert the variable name")
                value = self.__view.ask_input("Insert the variable value")
                
                if type_v == "f": fixed.append(FixedVariable(name, value))
                else: variables.append(Variable(name, value))
        
        ch = self.__view.menu("Variable in the url are they Fixed, Varaible, or ignore them ?", ["f", "v", "i"], ["Fixed varaibles", "Variables", "Ignore them"])
        vinurl = True if ch == "f" else False if ch == "v" else None
        
        return UrlInjector(Url(url, injectable_varaible=variables, fixed_variable=fixed, vars_in_url_are_fixed=vinurl), self.__config)
    
    
    def _set_configuration(self, config : Configuration=None) -> Configuration:
        if config == None:
            self.__config = Configuration()
        else:
            self.__config = config
    
    
    def _set_config_property(self, key : str, value : str | list | dict) -> None:
        self.__config[key] = value
    
    
    def _add_injector(self, injector : Injector) -> None:
        self.__config.add_injector(injector)

    
    def _add_global_payload(self, key : InjectionType | str, payload : str | list[str] | set[str]) -> None:
        
        if type(key) is InjectionType:
            key = key.value
        
        self.__config.add_global_payload(key, payload)
    
    
    def _add_global_payload_file(self, key : InjectionType | str, filename : str | list[str] | set[str]) -> None:
        
        if type(key) is InjectionType:
            key = key.value
        
        self.__config.add_payload_file_by_key(key, filename)
    
    
    def load_payloads_from_file(self) -> None:
        self.__config.load_payload_file()

    
    def start_injecting(self):
        to_inject = self.__config.build_injectors()

        for single in to_inject:
            self.__view.log_info("Injecting: " + single.get_url(), level_of_log=4)
            for payload in single:
                self.__view.log_info("Tryied this payload: " + payload, level_of_log=6)
        
    
    def inject_all(self):
        to_inject = self.__config.build_injectors()
        to_inject.inject_all()
    
    
    def exit(self):
        self.__view.log_info("Bye bye")
        del self
    
    
    def __del__(self):
        del self.__view, self.__config, self.injectors, self.description, self.cmds
        

    @classmethod
    def from_file(cls, view : MainView, filename : str) -> MainController:
        return cls(view, option=Configuration.from_file(filename))