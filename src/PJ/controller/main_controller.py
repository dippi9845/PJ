from __future__ import annotations
from PJ.model.url import Url
from PJ.view.main_view import MainView
from PJ.model.variable import InjectableVariable, FixedVariable
from PJ.model.configuration import InjectionType, Configuration
from injector.injector import InjectorList
from typing import Optional

class MainController:

    def __init__(self, view : MainView , config : Optional[Configuration]=None) -> None:
        self.__view = view
        self.__config = Configuration() if config is None else config
        
    def set_configuration(self, config : Configuration=None) -> Configuration:
        if config == None:
            self.__config = Configuration()
        else:
            self.__config = config

    def start_injecting(self):
        to_inject = self.__config.build_injectors()

        for single in to_inject:
            self.__view.log_info("Injecting: " + single.get_url(), level_of_log=4)
            for payload in single:
                self.__view.log_info("Tryied this payload: " + payload, level_of_log=6)
        
    
    def inject_all(self):
        to_inject = self.__config.build_injectors()
        to_inject.inject_all()

    @classmethod
    def from_file(cls, filename : str, view : MainView) -> MainController:
        return cls(view, option=Configuration.from_file(filename))