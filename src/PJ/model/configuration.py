from enum import Enum
from abc import abstractmethod
from json import loads
from PJ.controller.injector.injector import Injector
from PJ.model.url import Url, from_dict as url_from_dict
from PJ.controller.injector.url.injector_list import InjectorList

class InjectionType(Enum):
    URL = "1"
    WEBDRIVER = "2"

# TODO : marcare come classmethod tutte le factory in tutti i moduli

class ExportIdntifier(Enum):
    INJECTION_TYPE = "Injection Type"
    CONFIGURATION_NAME = "Name"
    PAYLOADS = "Payloads"
    PAYLOAD_FILES = "Payload Files"
    PAYLOAD_FILE_SEPARETOR = "Payload File Separetor"

    URLS = "Urls"

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
    
    @abstractmethod
    def build_injector(self) -> Injector:
        pass

    def to_dict(self) -> dict:
        return {ExportIdntifier.INJECTION_TYPE.value : None, ExportIdntifier.CONFIGURATION_NAME.value : self.config_name, ExportIdntifier.PAYLOADS.value : list(self.payloads), ExportIdntifier.PAYLOAD_FILES.value : list(self.payload_files), ExportIdntifier.PAYLOAD_FILE_SEPARETOR.value : self.payload_file_separetor}


class UrlConfiguration(Configuration):
    
    def __init__(self, config_name: str = "Default Config", payloads: set[str] = {}, payload_files: set[str] = {}, payload_file_separetor : str="\n", url : list[Url] = []) -> None:
        super().__init__(config_name, payloads, payload_files, payload_file_separetor)
        self.url = url
    
    def add_url(self, url : Url) -> None:
        self.url.append(url)
    
    # TODO : implementare sta roba
    def build_injector(self) -> InjectorList:
        pass
    
    def to_dict(self) -> dict:
        return super().to_dict().update({ExportIdntifier.INJECTION_TYPE.value: InjectionType.URL.value, ExportIdntifier.URLS.value : [i.to_dict() for i in self.url]})
        

def by_file(filename : str) -> Configuration:
    with open(filename, "r") as f:
        data = loads(f.read())
        
        if data[ExportIdntifier.INJECTION_TYPE.value] is InjectionType.URL.value:
            name = data[ExportIdntifier.CONFIGURATION_NAME.value]
            payloads = set(data[ExportIdntifier.PAYLOADS.value])
            files = set(data[ExportIdntifier.PAYLOAD_FILES.value])
            separetor = data[ExportIdntifier.PAYLOAD_FILE_SEPARETOR.value]
            raw_list = data[ExportIdntifier.URLS.value]
            urls = [url_from_dict(u) for u in raw_list]

            return UrlConfiguration(name, payloads=payloads, payload_files=files, payload_file_separetor=separetor, url=urls)
        
        elif data[ExportIdntifier.INJECTION_TYPE.value] is InjectionType.WEBDRIVER.value:
            raise NotImplementedError("Web driver as injection type is not implemented yet")
        
