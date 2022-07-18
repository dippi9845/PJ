from enum import Enum
from PJ.model.variable import from_dict
from json import loads
from PJ.model.url import Url
from injector.url.injector_list import InjectorList

class InjectionType(Enum):
    URL = "1"
    WEBDRIVER = "2"

class Configuration:
    def __init__(self, config_name : str="Default Config", payloads : set[str] = {}, payload_files : set[str] = {}, payload_file_separetor : str="\n") -> None:
        self.config_name = config_name
        self.payload_files = payload_files
        self.payload_files_to_add = payload_files
        self.payload_file_separetor = payload_file_separetor
        self.payloads = payloads

        self.load_payload_file()
    
    def add_payload_file(self, payload_file : str) -> None:
        if type(payload_file) is str:
            self.payload_files_to_add.add(payload_file)

        elif type(payload_file) is list:
            self.payload_files_to_add.update(set(payload_file))
        
        elif type(payload_file) is set:
            self.payload_files_to_add.update(payload_file)

    def load_payload_file(self) -> None:
        for i in self.payload_files_to_add:
            with open(i, "r") as f:
                self.payloads += f.read().split(self.payload_file_separetor)
        
        self.payload_files_to_add = {}
    
    def build_injector(self):
        raise NotImplementedError("build_injetor() method need to be implemented in subclasses")

    def to_dict(self) -> dict:
        return {"Injection Type": "Not defined", "Name" : self.config_name, "Payloads" : self.payloads, "Payload Files" : self.payload_files}


class UrlConfiguration(Configuration):
    
    def __init__(self, config_name: str = "Default Config", payloads: set[str] = {}, payload_files: set[str] = {}, payload_file_separetor : str="\n", url : list[Url] = []) -> None:
        super().__init__(config_name, payloads, payload_files, payload_file_separetor)
        self.url = url
    
    def add_url(self, url : str) -> None:
        self.url.append(url)
    
    def build_injector(self) -> InjectorList:
        raise NotImplementedError("build_injetor() not yet implemented")
    
    def to_dict(self) -> dict:
        return super().to_dict().update({"Injection Type": InjectionType.URL.value, "Urls" : [i.to_dict() for i in self.url]})
        

def by_file(filename : str) -> Configuration:
    with open(filename, "r") as f:
        data = loads(f.read())
        
        if data["injection_type"] is InjectionType.URL.value:
            pass
        
        elif data["injection_type"] is InjectionType.WEBDRIVER.value:
            raise NotImplementedError("Web driver as injection type is not implemented yet")
        
