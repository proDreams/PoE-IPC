from itertools import zip_longest

from tabulate import tabulate

from app.config import Configuration
from app.model import Data


class MainMenuView:

    def __init__(self):
        conf = Configuration()
        self.version_text = {1: "Обновление не требуется", 2: "Требуется обновление",
                             3: "Требуется обновление\nОбновление будет загружено автоматически."}
        self.menu_headers = ["Номер", "Пункт", "Версия"]
        self.main_menu_text = [[1, "Обмен предметов"],
                               [2, "Обновление базы предметов", self.version_text[conf.version_equals()]],
                               [3, "Сменить язык"], [4, "Выбрать лигу"], [5, "Выход"]]
        self.parser_menu_text = [[1, "Обновить базу предметов с сервера"], [2, "Обновить базу локально"],
                                 [3, "Назад"]]
        self.parser_service_info = [["База предметов на сервере:", conf.server_item_version],
                                    ["Локальная база предметов:", conf.local_item_version]]
        self.menu_service_info = [[f"Версия приложения: {conf.version}"],
                                  [f"Выбранный язык: {conf.current_language}"],
                                  [f"Актуальная лига: {conf.actual_league}"],
                                  [f"Выбранная лига: {conf.selected_league}"],
                                  [f"Режим обмена: {conf.version}"]]
        self.welcome_message_text = [["Добро пожаловать бла бла"], ["Для продолжения нажмите любую клавишу"]]

    def print_welcome_message(self):
        print(tabulate(self.welcome_message_text))
        input()

    def print_main_menu(self):
        print(tabulate(self.menu_service_info))
        print(tabulate(self.main_menu_text, headers=self.menu_headers, stralign="left"))

    def print_parser_menu(self):
        print(tabulate(self.parser_service_info))
        print(tabulate(self.parser_menu_text, headers=self.menu_headers, stralign="left"))

    @staticmethod
    def choose_league(league_list):
        leagues_list = [[pos, name] for pos, name in enumerate(league_list, 1)]
        print(tabulate(leagues_list))

    @staticmethod
    def print_result(count, price):
        print(f"Вы получите {price} сфер хаоса за {count}")
        print(f"~price {price}/{count} chaos")


class UpdaterViews:
    operations = {1: "Операция обновления выполнена успешно"}

    def print_update_operation(self, point):
        print(self.operations[point])


class Inputs:
    input_words = {0: "Неверная команда, попробуйте ещё раз", 1: "Введите номер пункта меню: ",
                   2: "Введите количество: ", 3: "Для возврата в меню, нажмите любую кнопку."}

    def menu_selector(self, point):
        return input(self.input_words[point])

    def wrong_input_message(self):
        return self.input_words[0]

    def any_key(self):
        print(self.input_words[3])


class ParserEvents:
    events = {1: "Началось обновление базы, пожалуйста, подождите...", 2: "Обновление выполнено успешно."}

    def print_event(self, event):
        print(self.events[event])


class ChooseItem:
    def print_category_and_items(self, items: dict, category=None):
        if category is None:
            key_list = list(items.keys())
            event = 1
        else:
            key_list = list(items[category].keys())
            event = 2
        item_key_list = self.get_list(key_list)
        print(tabulate(item_key_list))
        while True:
            try:
                selector = int(input(self.print_event(event)))
                if selector > len(key_list):
                    print(Inputs().wrong_input_message())
                else:
                    break
            except ValueError:
                print(Inputs().wrong_input_message())
        if category is None:
            return key_list[selector - 1]
        else:
            return items[category][key_list[selector - 1]]

    @staticmethod
    def get_list(items):
        index = 1
        rows = round(len(items) / 3)
        row_num = 0
        result = [[] for _ in range(rows)]
        while index <= len(items):
            if row_num > rows - 1:
                row_num = 0
            result[row_num].append(index)
            result[row_num].append(items[index - 1])
            index += 1
            row_num += 1
        return result

    @staticmethod
    def print_event(point):
        message = {1: 'Выберете раздел: ', 2: 'Выберете предмет: '}
        return message[point]
