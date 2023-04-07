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
                case 1:
                    category_selector = True
                    while category_selector:
                        clear_console()
                        items = Data().get_items(Configuration().current_language)
                        category = ChooseItem().print_category_and_items(items)
                        if category == 0:
                            break
                        clear_console()
                        print(category)
                        item_selector = True
                        while item_selector:
                            item = ChooseItem().print_category_and_items(items, category)
                            if item == 0:
                                break
                            clear_console()
                            count = int(Inputs().menu_selector(2))
                            if count != 0:
                                if Configuration().trade_mode == "bulk":
                                    price = GetFromApi().get_currency_price(item, Configuration().selected_league,
                                                                            count)
                                else:
                                    price = GetFromApi().get_currency_price(item, Configuration().selected_league)
                                result_price, result_count = GetFromApi().calculate_result(count, price)
                                MainMenuView().print_result(result_count, result_price)
                                end = Inputs().any_key()
                                if end == 1:
                                    item_selector = False
                                    category_selector = False
                                elif end == 0:
                                    item_selector = False
                case 2:
                    self.menu_depth = 2
                    self.parser_menu()
                case 3:
                    self.choose_language()
                case 4:
                    self.choose_league_menu()
                case 5:
                    self.choose_mode()
                case 6:
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
                case 1:
                    Data().update_file()
                    UpdaterViews().print_update_operation(1)
                case 2:
                    poesessid = Configuration().poesessid
                    if poesessid == "":
                        poesessid = Inputs().menu_selector(6)
                        Configuration().poesessid = poesessid
                    ParserEvents().print_event(1)
                    Parse().parse(actual_league=Configuration().actual_league,
                                  poesessid=poesessid)
                    ParserEvents().print_event(2)
                case 3:
                    self.menu_depth = 1
                case _:
                    Inputs().wrong_input_message()

    @staticmethod
    def choose_league_menu():
        clear_console()
        leagues = GetFromApi().get_leagues()
        MainMenuView().choose_league(leagues)
        while True:
            select = Inputs().menu_selector(1)
            if select > len(leagues):
                Inputs().wrong_input_message()
            else:
                break
        Configuration().set_league(leagues[int(select) - 1])

    @staticmethod
    def choose_mode():
        mode_dict = {1: "bulk", 2: "retail"}
        clear_console()
        MainMenuView().choose_mode()
        while True:
            select = Inputs().menu_selector(4)
            if select > len(mode_dict):
                Inputs().wrong_input_message()
            else:
                break
        Configuration().set_mode(mode_dict[int(select)])

    @staticmethod
    def choose_language():
        langs = {1: "ru", 2: "en"}
        clear_console()
        MainMenuView().choose_lang()
        while True:
            select = Inputs().menu_selector(5)
            if select > len(langs):
                Inputs().wrong_input_message()
            else:
                break
        Configuration().set_lang(langs[int(select)])
