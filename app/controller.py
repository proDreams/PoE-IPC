import os
import sys

from app.config import Configuration
from app.model import GetFromApi, Parse, Data
from app.views import MainMenuView, Inputs, UpdaterViews, ParserEvents, ChooseItem


def clear_console():
    os.system("CLS")


class AppMenu:
    menu_depth = 1

    def __init__(self):
        MainMenuView().print_welcome_message()
        self.main_menu()

    def main_menu(self):
        while self.menu_depth == 1:
            clear_console()
            MainMenuView().print_main_menu()
            select = Inputs().menu_selector(1)
            clear_console()
            match select:
                case "1":
                    while True:
                        clear_console()
                        items = Data().get_items(Configuration().current_language)
                        category = ChooseItem().print_category_and_items(items)
                        clear_console()
                        print(category)
                        item = ChooseItem().print_category_and_items(items, category)
                        count = int(Inputs().menu_selector(2))
                        if Configuration().trade_mode == "bulk":
                            price = GetFromApi().get_currency_price(item, Configuration().selected_league, count)
                        else:
                            price = GetFromApi().get_currency_price(item, Configuration().selected_league)
                        result_price, result_count = GetFromApi().calculate_result(count, price)
                        MainMenuView().print_result(result_count, result_price)
                        if Inputs().any_key() == "1":
                            break
                case "2":
                    self.menu_depth = 2
                    self.parser_menu()
                case "3":
                    self.choose_language()
                case "4":
                    self.choose_league_menu()
                case "5":
                    self.choose_mode()
                case "6":
                    sys.exit(0)
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
                    Data().update_file()
                    UpdaterViews().print_update_operation(1)
                case "2":
                    ParserEvents().print_event(1)
                    Parse().parse(actual_league=Configuration().actual_league,
                                  poesessid=Configuration().poesessid)
                    ParserEvents().print_event(2)
                case "3":
                    self.menu_depth = 1
                case _:
                    Inputs().wrong_input_message()

    @staticmethod
    def choose_league_menu():
        clear_console()
        leagues = GetFromApi().get_leagues()
        MainMenuView().choose_league(leagues)
        select = Inputs().menu_selector(1)
        Configuration().set_league(leagues[int(select) - 1])

    @staticmethod
    def choose_mode():
        mode_dict = {1: "bulk", 2: "retail"}
        clear_console()
        MainMenuView().choose_mode()
        select = Inputs().menu_selector(4)
        Configuration().set_mode(mode_dict[int(select)])

    @staticmethod
    def choose_language():
        langs = {1: "ru", 2: "en"}
        clear_console()
        MainMenuView().choose_lang()
        select = Inputs().menu_selector(5)
        Configuration().set_lang(langs[int(select)])
