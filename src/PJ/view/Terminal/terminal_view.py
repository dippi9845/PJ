from ..main_view import MainView

class TerminalView(MainView):
    
    INTRODUCTION_FILE = "../../../../res/view/introduction.txt"

    def __init__(self) -> None:
        self.introduction()

    def introduction(self):
        with open(self.INTRODUCTION_FILE) as file:
            print(file.read())

    def ask_input(string : str) -> str:
        return input(string)

    def log(self, string: str):
        print(string)