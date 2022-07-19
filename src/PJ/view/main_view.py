class MainView:
    
    MAX_LEVEL_OF_LOG = 6
    WARNING_LOG_LEVEL = 2
    ERROR_LOG_LEVEL = 1

    def __init__(self, level_of_log=3) -> None:
        
        if level_of_log < 1 or level_of_log > self.MAX_LEVEL_OF_LOG:
            raise TypeError("level of log not valid")
        
        self.__level_of_log = level_of_log

    def introduction(self):
        pass

    def ask_input(self, string : str) -> str:
        pass

    def ask_yes_no(self, question : str) -> bool:
        pass

    def log(self, string : str, end='\n'):
        pass

    def log_info(self, string : str, level_of_log=3):
        if self.__level_of_log >= level_of_log:
            self.log(string)

    def log_warning(self, string : str):
        if self.__level_of_log >= self.WARNING_LOG_LEVEL:
            self.log(string)

    def log_error(self, string : str):
        if self.__level_of_log >= self.ERROR_LOG_LEVEL:
            self.log(string)