from PJ.view.main_view import MainView
from colorama import Fore

class TerminalView(MainView):
    
    INTRODUCTION_FILE = "../../../../res/view/introduction.txt"

    WARINING_SEGNALATION = "[" + Fore.YELLOW + "WARINIG" + Fore.WHITE + "] "
    ERROR_SEGNALATION = "[" + Fore.RED + "ERROR" + Fore.WHITE + "] "
    INFO_SEGNALATION = "[" + Fore.CYAN + "INFO" + Fore.WHITE +"] "

    def __init__(self) -> None:
        self.introduction()

    def introduction(self):
        with open(self.INTRODUCTION_FILE) as file:
            print(file.read())

    def ask_input(string : str) -> str:
        return input(string)

    def log(self, string: str, end='\n'):
        print(string, end=end)
    
    def log_warning(self, string: str):
        return super().log_warning(self.WARINING_SEGNALATION + string)
    
    def log_error(self, string: str):
        return super().log_error(self.ERROR_SEGNALATION + string)
    
    def log_info(self, string: str, level_of_log=3):
        
        if level_of_log == 3:
            return super().log_info(self.INFO_SEGNALATION + string, level_of_log)
        else:
            return super().log_info(string, level_of_log)
        
    def ask_for_multiple(self, message: str, elements: list) -> dict:
        tmp = " "
        rtr = {}
        
        for i in elements:
            while tmp is not "":
                tmp = self.ask_input(message + " " + i)
            
            rtr[i] = tmp
        
        return rtr
    
    def main_menu(self):
        pass