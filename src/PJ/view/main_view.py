class MainView:
    
    MAX_LEVEL_OF_LOG = 6
    WARNING_LOG_LEVEL = 2
    ERROR_LOG_LEVEL = 1

    def __init__(self, level_of_log=3) -> None:
        
        if level_of_log < 1 or level_of_log > self.MAX_LEVEL_OF_LOG:
            raise TypeError("level of log not valid")
        
        self.__level_of_log = level_of_log

    def introduction(self):
        raise NotImplementedError("need to be implemented by superclass")

    def ask_input(self, string : str) -> str:
        raise NotImplementedError("need to be implemented by superclass")

    def log(self, string : str, end='\n'):
        raise NotImplementedError("need to be implemented by superclass")

    def ask_yes_no(self, question : str, yes : str = "y", no : str = "n", suggested : str = "y", case_sensitive : bool = False, yes_to_bool : bool = True) -> bool:
        ch = self.ask_input(question)
        
        if ch == "":
            ch = suggested
        
        if not case_sensitive:
            ch = ch.lower()
        
        if ch is yes:
            return yes_to_bool
        
        elif ch is no:
            return not yes_to_bool
        
        else:
            return None
    
    def ask_for_multiple(self, question : str) -> list:
        tmp = " "
        rtr = []
        
        while tmp is not "":
            tmp = self.__view.ask_input(question)
            rtr.append(tmp)
        
        rtr.pop()
        
        return rtr

    def log_info(self, string : str, level_of_log=3):
        if self.__level_of_log >= level_of_log:
            self.log(string)

    def log_warning(self, string : str):
        if self.__level_of_log >= self.WARNING_LOG_LEVEL:
            self.log(string)

    def log_error(self, string : str):
        if self.__level_of_log >= self.ERROR_LOG_LEVEL:
            self.log(string)