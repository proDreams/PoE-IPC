import os

from app.config import Configuration
from app.model import GetFromApi, Parse, FileUpdater, VersionInfo
from app.views import MainMenuView, Inputs, UpdaterViews, ParserEvents


def clear_console():
    os.system("CLS")


class AppMenu:
    menu_depth = 1

    def __init__(self):
        MainMenuView().print_welcome_message()
        self.main_menu()

    def main_menu(self):
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
                    self.choose_league_menu()
                case "5":
                    self.menu_depth = 0
                case _:
                    Inputs().wrong_input_message()

    def parser_menu(self):
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

    @staticmethod
    def choose_league_menu():
        leagues = GetFromApi().get_leagues()
        MainMenuView().choose_league(leagues)
        select = Inputs().menu_selector(1)
        Configuration().set_league(leagues[int(select) - 1])


class StartUpConfiguration:
    Configuration().local_item_version = VersionInfo().check_local_version()
    Configuration().server_item_version = VersionInfo().check_server_version()
    Configuration().browser_version = VersionInfo().browser_version
    Configuration().webdriver_version = VersionInfo().webdriver_version
    Configuration().browser_version_status = VersionInfo().check_browser_version()
    Configuration().actual_league = GetFromApi().get_leagues()[2]
    AppMenu()
