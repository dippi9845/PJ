from PJ.controller.main_controller import MainController
from PJ.view.terminal_view import TerminalView

controller = MainController(TerminalView())
controller.main_menu()