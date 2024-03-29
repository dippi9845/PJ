from __future__ import annotations
from enum import Enum
from io import TextIOWrapper
from json import loads
from PJ.controller.injector.url_injector import UrlInjector, ExportUtils as URLExport
from PJ.controller.injector.injector import InjectorList, Injector, INJECTORLIST_EMPTY
from os.path import basename

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
    INJECTOR_TYPE = "Injector type"
    
    INJECTION_TYPE = "Injection Type"
    PAYLOADS = "Payloads"
    PAYLOAD_FILES = "Payload Files"
    PAYLOAD_FILE_SEPARETOR = "Payload File Separetor"
    IGNORE_GLOBAL_PAYLOADS = "Ignore global payload"


class ConfigVersion(Enum):
    FIRST_VERSION = "1.0.0"


INJECTORTYPE_TO_INJECTOR = {
    InjectionType.URL.value : UrlInjector
}

INJECTORTYPE_TO_EXPORT = {
    InjectionType.URL.value : {
        ExportIdentifier.PAYLOADS.value : URLExport.PAYLOADS.value
    }
}

INJECTOR_TO_INJECTORTYPE = {
   UrlInjector: InjectionType.URL.value
}


class Configuration:
    def __init__(self, config_version : ConfigVersion=ConfigVersion.FIRST_VERSION.value, config_name : str="Default Config", global_payloads : dict[str, set]={}, global_payload_files : dict[str, set]={}, global_payload_file_separetor : str="\n", injectors_serialized : list[dict]=[], injector_list : InjectorList=INJECTORLIST_EMPTY) -> None:
        self.config_name = config_name
        self.config_version = config_version
        
        self.global_payloads = self.get_empty_payload_dict() if global_payloads == {} else global_payloads
        self.global_payload_files_added = self.get_empty_payload_dict()
        self.payload_files_to_add = self.get_empty_payload_dict() if global_payload_files == {} else global_payload_files
        self.payload_file_separetor = global_payload_file_separetor
        
        self.injectors_serialized = injectors_serialized + list(map(lambda x: self.serialize_injector(x), injector_list))

    
    def add_payload_file_by_key(self, key : str, payload_file : str | list[str] | set[str]) -> None:
        if type(payload_file) is str:
            self.payload_files_to_add[key].append(payload_file)

        elif type(payload_file) is list:
            self.payload_files_to_add[key] += payload_file
        
        elif type(payload_file) is set:
            self.payload_files_to_add[key] += list(payload_file)
        
    def add_payload_file_by_dict(self, payload_dict : dict) -> None:
        for key, value in payload_dict.items():
            self.add_payload_file_by_key(key, value)

    def load_payload_file(self) -> None:
        for key, values in self.payload_files_to_add.items():
            for file in values:
                
                # this duplicate check sucks
                if file in self.global_payload_files_added[key]:
                    continue
                
                self.global_payload_files_added[key].append(file)
                with open(file, "r") as f:
                    self.global_payloads[key] += f.read().split(self.payload_file_separetor)
        
        self.payload_files_to_add = self.get_empty_payload_dict()
    
    def add_injector(self, injector : Injector | InjectorList | dict) -> None:
        
        if isinstance(injector, InjectorList):
            self.injectors_serialized += list(map(lambda x: self.serialize_injector(x), injector))
        
        elif isinstance(injector, Injector):
            self.injectors_serialized.append(self.serialize_injector(injector))
        
        elif type(injector) is dict:
            if not ExportIdentifier.INJECTOR_TYPE.value in injector:
                raise ValueError("Injector type is not specified")
            
            self.injectors_serialized.append(injector)
    
    def build_injectors(self) -> InjectorList:
        ilist = []
        payloads_to_load = self.get_empty_payload_dict()
        
        for key, values in self.payload_files_to_add.items():
            for file in values:
                
                # this duplicate check sucks
                if file in self.global_payload_files_added[key]:
                    continue
                
                with open(file, "r") as f:
                    payloads_to_load[key] += f.read().split(self.payload_file_separetor)
        
        for i in self.injectors_serialized:
            injector_type = i[ExportIdentifier.INJECTOR_TYPE.value]
            payload_idn = INJECTORTYPE_TO_EXPORT[injector_type][ExportIdentifier.PAYLOADS.value]
            
            i[payload_idn] += self.global_payloads[injector_type] + payloads_to_load[injector_type]
            ilist.append(INJECTORTYPE_TO_INJECTOR[injector_type].from_dict(i))
            
        return InjectorList(ilist)

    def to_dict(self) -> dict:
        return {
            ExportIdentifier.VERSION.value : self.config_version,
            ExportIdentifier.CONFIGURATION_NAME.value : self.config_name,
            ExportIdentifier.GLOBAL_PAYLOADS.value : self.global_payloads,
            ExportIdentifier.GLOBAL_PAYLOAD_FILES.value : self.payload_files_to_add,
            ExportIdentifier.GLOBAL_PAYLOAD_FILE_SEPARETOR.value : self.payload_file_separetor,
            ExportIdentifier.INJECTORS.value : self.injectors_serialized
        }
    
    @staticmethod
    def get_empty_payload_dict(type=list) -> dict[str, set | list]:
        rtr = {}
        for i in [member.value for member in InjectionType]:
            rtr[i] = type()
        return rtr

    @staticmethod
    def serialize_injector(injector : Injector) -> dict:
        rtr = injector.to_dict()
        rtr.update({ExportIdentifier.INJECTOR_TYPE.value: INJECTOR_TO_INJECTORTYPE[type(injector)]})
        return rtr
    
    @classmethod
    def from_file_descriptor(cls, file_descriptor: TextIOWrapper) -> Configuration:
        data = loads(file_descriptor.read())
        name = basename(file_descriptor.name).split('/')[-1] # only the file name
        
        return cls.from_dict(data, default_name=name)
        
    @classmethod
    def from_dict(cls, data : dict, default_name="unamed config"):
        if not ExportIdentifier.VERSION.value in data:
            raise ValueError(f"{default_name} doesn't contains the version")
        
        config_version = data[ExportIdentifier.VERSION.value]
        config_name = default_name
        
        if ExportIdentifier.CONFIGURATION_NAME.value in data:
            config_name = data[ExportIdentifier.CONFIGURATION_NAME.value]
        
        global_payloads = {}
        
        if ExportIdentifier.GLOBAL_PAYLOADS.value in data:
            global_payloads = data[ExportIdentifier.GLOBAL_PAYLOADS.value]
        
        global_payloads_files = {}
        
        if ExportIdentifier.GLOBAL_PAYLOAD_FILES.value in data:
            global_payloads_files = data[ExportIdentifier.GLOBAL_PAYLOAD_FILES.value]
        
        global_payloads_file_separetor = "\n"
        
        if ExportIdentifier.GLOBAL_PAYLOAD_FILE_SEPARETOR.value in data:
            global_payloads_file_separetor = data[ExportIdentifier.GLOBAL_PAYLOAD_FILE_SEPARETOR.value]
        
        if not ExportIdentifier.INJECTORS.value in data:
            raise ValueError(f"{default_name} doesn't contains any injector")

        injectors = data[ExportIdentifier.INJECTORS.value]
        
        return cls(config_name=config_name, config_version=config_version, global_payloads=global_payloads, global_payload_files=global_payloads_files, global_payload_file_separetor=global_payloads_file_separetor, injectors_serialized=injectors)

    @classmethod
    def from_file(cls, filename):
        with open(filename, "r") as fd:
            return cls.from_file_descriptor(fd)