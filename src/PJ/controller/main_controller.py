from __future__ import annotations
from PJ.controller.injector.injector import Injector
from PJ.view.main_view import MainView
from PJ.model.configuration import Configuration, InjectionType
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
    
    def set_config_property(self, key : str, value : str | list | dict) -> None:
        self.__config[key] = value
    
    def add_injector(self, injector : Injector) -> None:
        self.__config.add_injector(injector)

    def add_global_payload(self, key : InjectionType | str, payload : str | list[str] | set[str]) -> None:
        
        if type(key) is InjectionType:
            key = key.value
        
        self.__config.add_global_payload(key, payload)
    
    def add_global_payload_file(self, key : InjectionType | str, filename : str | list[str] | set[str]) -> None:
        
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

    @classmethod
    def from_file(cls, view : MainView, filename : str) -> MainController:
        return cls(view, option=Configuration.from_file(filename))