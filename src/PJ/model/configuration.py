from __future__ import annotations
from enum import Enum
from abc import abstractmethod
from json import loads
from PJ.model.url import Url
from PJ.controller.injector.injector import InjectorList, Injector, INJECTORLIST_EMPTY

class InjectionType(Enum):
    URL = "url"
    WEBDRIVER = "webdriver"

class ExportIdentifier(Enum):
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
    IGNORE_GLOBAL_PAYLOADS = "Ignore global payload"

class ConfigVersion(Enum):
    FIRST_VERSION = "1.0.0"
    
class Configuration:
    def __init__(self, config_version : ConfigVersion=ConfigVersion.FIRST_VERSION, config_name : str="Default Config", global_payloads : dict[str, set]={}, global_payload_files : dict[str, set]={}, payload_file_separetor : str="\n", injectors_serialized : list=[dict], injector_list : InjectorList=INJECTORLIST_EMPTY) -> None:
        self.config_name = config_name
        self.config_version = config_version
        
        self.global_payload_files = global_payload_files
        self.global_payloads = global_payloads
        
        self.payload_files_to_add = global_payload_files
        self.payload_file_separetor = payload_file_separetor
        
        self.injectors_serialized = injectors_serialized + injector_list.to_dict()

        self.load_payload_file()
    
    def add_payload_file_by_key(self, key : str, payload_file : str | list[str] | set[str]) -> None:
        if type(payload_file) is str:
            self.payload_files_to_add[key].add(payload_file)

        elif type(payload_file) is list:
            self.payload_files_to_add[key].update(set(payload_file))
        
        elif type(payload_file) is set:
            self.payload_files_to_add[key].update(payload_file)
        
    def add_payload_file_by_dict(self, payload_dict : dict) -> None:
        for key, value in payload_dict.items():
            self.add_payload_file_by_key(key, value)

    def load_payload_file(self) -> None:
        for key, values in self.payload_files_to_add.items():
            for file in values:
                with open(file, "r") as f:
                    self.global_payloads[key].update(set(f.read().split(self.payload_file_separetor)))
        
        self.payload_files_to_add = {}
    
    def add_injector(self, injector : Injector | InjectorList | dict) -> None:
        
        if isinstance(injector, InjectorList):
            self.injectors_serialized += injector.to_dict()
        
        elif isinstance(injector, Injector):
            self.injectors_serialized.append(injector.to_dict())
        
        elif type(injector) is dict:
            self.injectors_serialized.append(injector)
    
    def build_injectors(self) -> InjectorList:
        pass

    # self.global_payloads è un dizionario non una lista
    # self.global_payload_files è un dizionario non una lista
    def to_dict(self) -> dict:
        global_payloads_list = {}
        for key, value in self.global_payloads:
            global_payloads_list[key] = list(value)
        
        global_payload_files_list = {}
        for key, value in self.global_payload_files:
            global_payload_files_list[key] = list(value)
        
        return {
                ExportIdentifier.VERSION.value : self.config_version.value,
                ExportIdentifier.CONFIGURATION_NAME.value : self.config_name,
                ExportIdentifier.GLOBAL_PAYLOADS.value : global_payloads_list,
                ExportIdentifier.GLOBAL_PAYLOAD_FILES.value : global_payload_files_list,
                ExportIdentifier.GLOBAL_PAYLOAD_FILE_SEPARETOR.value : self.payload_file_separetor,
                ExportIdentifier.INJECTORS.value : self.injectors_serialized
            }

    @classmethod
    def from_file(cls, filename : str) -> Configuration:
        with open(filename, "r") as f:
            data = loads(f.read())
            
            if not data.__contains__(ExportIdentifier.VERSION.value):
                raise ValueError(f"{filename} doesn't contains the version")
            
            config_version = data[ExportIdentifier.VERSION.value]
            config_name = filename
            
            if data.__contains__(ExportIdentifier.CONFIGURATION_NAME.value):
                config_name = data[ExportIdentifier.CONFIGURATION_NAME.value]
            
            global_payloads = {}
            
            if data.__contains__(ExportIdentifier.GLOBAL_PAYLOADS.value):
                global_payloads = data[ExportIdentifier.GLOBAL_PAYLOADS.value]
            
            global_payloads_files = {}
            
            if data.__contains__(ExportIdentifier.GLOBAL_PAYLOAD_FILES.value):
                global_payloads_files = set(data[ExportIdentifier.GLOBAL_PAYLOAD_FILES.value])
            
            global_payloads_file_separetor = "\n"
            
            if data.__contains__(ExportIdentifier.GLOBAL_PAYLOAD_FILE_SEPARETOR.value):
                global_payloads_file_separetor = data[ExportIdentifier.GLOBAL_PAYLOAD_FILE_SEPARETOR.value]
            
            if not data.__contains__(ExportIdentifier.INJECTORS.value):
                raise ValueError(f"{filename} doesn't contains any injector")

            injectors = data[ExportIdentifier.INJECTORS.value]
            
            return cls(config_name=config_name, config_version=config_version, global_payloads=global_payloads, global_payload_files=global_payloads_files, global_payload_file_separetor=global_payloads_file_separetor, injectors_serialized=injectors)

