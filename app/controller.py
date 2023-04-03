import os

from app.config import Configuration
from app.parser import Parse, FileUpdater, VersionInfo


def clear_console():
    os.system("CLS")


class AppMenu:
    menu_depth = 1

    def __init__(self):
        from app.views import MainMenuView

        MainMenuView().print_welcome_message()
        self.main_menu()

    def main_menu(self):
        from app.views import MainMenuView, Inputs

        clear_console()
        while self.menu_depth == 1:
            MainMenuView().print_main_menu()
            select = Inputs().menu_selector(1)
            clear_console()
            match select:
                case "1":
                    pass
                case "2":
                    self.menu_depth = 2
                    self.parser_menu()
                case "3":
                    pass
                case "4":
                    self.menu_depth = 0
                case _:
                    Inputs().wrong_input_message()

    def parser_menu(self):
        from app.views import MainMenuView, UpdaterViews, ParserEvents, Inputs

        clear_console()
        while self.menu_depth == 2:
            MainMenuView().print_parser_menu()
            select = Inputs().menu_selector(1)
            clear_console()
            match select:
                case "1":
                    FileUpdater().update_file()
                    UpdaterViews().print_update_operation(1)
                case "2":
                    ParserEvents().print_event(1)
                    Parse().parse()
                    ParserEvents().print_event(2)
                case "3":
                    self.menu_depth = 1
                case _:
                    Inputs().wrong_input_message()


class StartUpConfiguration:
    Configuration().set_versions(VersionInfo().check_local_version(), VersionInfo().check_server_version(),
                                 VersionInfo().browser_version, VersionInfo().webdriver_version,
                                 VersionInfo().check_browser_version())
    AppMenu()
