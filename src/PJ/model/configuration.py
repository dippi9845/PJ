from __future__ import annotations
from enum import Enum
from abc import abstractmethod
from json import loads
from PJ.controller.injector.injector import Injector
from PJ.model.url import Url
from PJ.controller.injector.injector import InjectorList

class InjectionType(Enum):
    URL = "url"
    WEBDRIVER = "webdriver"

class ExportIdntifier(Enum):
    VERSION = "Config version"
    CONFIGURATION_NAME = "Name"
    GLOBAL_PAYLOADS = "Global Payloads"
    GLOBAL_PAYLOAD_FILES = "Global Payload Files"
    GLOBAL_PAYLOAD_FILE_SEPARETOR = "Global Payload File Separetor"
    INJECTORS = "Injectors"
    
    INJECTION_TYPE = "Injection Type"
    PAYLOADS = "Payloads"
    PAYLOAD_FILES = "Payload Files"
    PAYLOAD_FILE_SEPARETOR = "Payload File Separetor"

class ConfigVersion(Enum):
    FIRST_VERSION = "1.0.0"
    
class Configuration:
    def __init__(self, config_version : ConfigVersion=ConfigVersion.FIRST_VERSION, config_name : str="Default Config", global_payloads : dict[str, set]={}, global_payload_files : dict[str, set]={}, payload_file_separetor : str="\n") -> None:
        self.config_name = config_name
        self.config_version = config_version
        
        self.global_payload_files = global_payload_files
        self.global_payloads = global_payloads
        
        self.payload_files_to_add = global_payload_files
        self.payload_file_separetor = payload_file_separetor

        self.load_payload_file()
    
    def add_payload_file_by_key(self, key : str, payload_file : str) -> None:
        if type(payload_file) is str:
            self.payload_files_to_add[key].add(payload_file)

        elif type(payload_file) is list:
            self.payload_files_to_add[key].update(set(payload_file))
        
        elif type(payload_file) is set:
            self.payload_files_to_add[key].update(payload_file)
        
    def add_payload_file_by_dict(self, payload_dict : dict):
        for key, value in payload_dict.items():
            self.add_payload_file_by_key(key, value)

    def load_payload_file(self) -> None:
        for key, values in self.payload_files_to_add.items():
            for file in values:
                with open(file, "r") as f:
                    self.global_payloads[key].update(set(f.read().split(self.payload_file_separetor)))
        
        self.payload_files_to_add = {}
    
    def build_injectors(self) -> InjectorList:
        pass

    def to_dict(self) -> dict:
        return {
                ExportIdntifier.VERSION.value : self.config_version.value,
                ExportIdntifier.CONFIGURATION_NAME.value : self.config_name,
                ExportIdntifier.GLOBAL_PAYLOADS.value : list(self.global_payloads),
                ExportIdntifier.GLOBAL_PAYLOAD_FILES.value : list(self.global_payload_files),
                ExportIdntifier.GLOBAL_PAYLOAD_FILE_SEPARETOR.value : self.payload_file_separetor
            }

    @classmethod
    def from_file(cls, filename : str) -> Configuration:
        with open(filename, "r") as f:
            data = loads(f.read())
            
            if data[ExportIdntifier.INJECTION_TYPE.value] is InjectionType.URL.value:
                
                if not data.__contains__(ExportIdntifier.GLOBAL_PAYLOADS.value) and not data.__contains__(ExportIdntifier.GLOBAL_PAYLOAD_FILES.value):
                    raise IOError("The configuration file doesn't contains any payloads to inject")
                
                elif not data.__contains__(ExportIdntifier.URLS.value):
                    raise IOError("The configuration file doesn't contains any url to be injected")
                
                if data.__contains__(ExportIdntifier.CONFIGURATION_NAME.value):
                    name = data[ExportIdntifier.CONFIGURATION_NAME.value]
                
                else:
                    name = "Unamed url configuration"
                
                payloads = set(data[ExportIdntifier.GLOBAL_PAYLOADS.value])
                files = set(data[ExportIdntifier.GLOBAL_PAYLOAD_FILES.value])
                separetor = data[ExportIdntifier.GLOBAL_PAYLOAD_FILE_SEPARETOR.value]
                raw_list = data[ExportIdntifier.URLS.value]
                urls = [Url.from_dict(u) for u in raw_list]

                
            
            elif data[ExportIdntifier.INJECTION_TYPE.value] is InjectionType.WEBDRIVER.value:
                raise NotImplementedError("Web driver as injection type is not implemented yet")
        


        
