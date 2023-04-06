from tabulate import tabulate

from app.config import Configuration


class MainMenuView:
    def __init__(self):
        conf = Configuration()
        self.lang = conf.current_language
        mode_dict = {"ru": {1: "Оптовый", 2: "Штучный"},
                     "en": {1: "Bulk", 2: "Retail"}}
        mode = mode_dict[self.lang][1] if conf.trade_mode == 'bulk' else mode_dict[self.lang][2]
        self.version_text = {"ru": {1: "Обновление не требуется", 2: "Требуется обновление",
                                    3: "Требуется обновление\nОбновление будет загружено автоматически."},
                             "en": {1: "Update not required", 2: "Required update",
                                    3: "Required update\n"
                                       "Update will be downloaded automatically."}}
        self.version_equals = self.version_text[self.lang][conf.version_equals()]
        self.menu_headers = {"ru": ["Номер", "Пункт", "Версия"],
                             "en": ["Number", "Point", "Version"]}
        self.main_menu_text = {"ru": [[1, "Проверка стоимости предметов"],
                                      [2, "Обновление базы предметов", self.version_equals],
                                      [3, "Сменить язык / Change language"], [4, "Выбрать лигу"],
                                      [5, "Сменить режим торговли"],
                                      [6, "Выход"]],
                               "en": [[1, "Convert items price"],
                                      [2, "Update items base", self.version_equals],
                                      [3, "Change language / Сменить язык"], [4, "Choose league"],
                                      [5, "Change trade mode"],
                                      [6, "Exit"]]}
        self.parser_menu_text = {
            "ru": [[1, "Обновить базу предметов с сервера"], [2, "Обновить базу локально парсером"],
                   [3, "Назад"]],
            "en": [[1, "Update items base from server"], [2, "Update items base by local parser"],
                   [3, "Back"]]}
        self.server_item_version = conf.server_item_version
        self.local_item_version = conf.local_item_version
        self.parser_service_info = {"ru": [["База предметов на сервере:", self.server_item_version],
                                           ["Локальная база предметов:", self.local_item_version]],
                                    "en": [["Items base on server:", self.server_item_version],
                                           ["Local items base:", self.local_item_version]]}
        self.version = conf.version
        self.actual_version = conf.actual_version
        self.current_language = conf.current_language
        self.actual_league = conf.actual_league
        self.selected_league = conf.selected_league
        self.menu_service_info = {"ru": [[f"Версия приложения: {self.version}"],
                                         [f"Актуальная версия приложения: {self.actual_version}"],
                                         [f"Выбранный язык / Current language: {self.current_language}"],
                                         [f"Актуальная лига: {self.actual_league}"],
                                         [f"Выбранная лига: {self.selected_league}"],
                                         [f"Режим обмена: {mode}"]],
                                  "en": [[f"Program version: {self.version}"],
                                         [f"Actual program version: {self.actual_version}"],
                                         [f"Current language / Текущий язык: {self.current_language}"],
                                         [f"Actual league: {self.actual_league}"],
                                         [f"Selected league: {self.selected_league}"],
                                         [f"Trade mode: {mode}"]]}
        self.welcome_message_text = {
            "ru": [["Добро пожаловать в приложение PoETRY"],
                   ["Приложение для расчёта оптимального соотношения цены предмета к сферам хаоса"],
                   [""], ["Автор: Иван 'proDream' Ашихмин"], ["Поддержать автора: https://boosty.to/prodream/donate"],
                   [""], ["Для продолжения нажмите любую клавишу"]],
            "en": [["Welcome in PoETRY"],
                   ["Application for calculating the optimal ratio of the price of an item to chaos orbs"],
                   [""], ["Author: Ivan 'proDream' Ashikhmin"], ["Donate: https://boosty.to/prodream/donate"],
                   [""], ["To continue, press any key"]]}

    def print_welcome_message(self):
        print(tabulate(self.welcome_message_text[self.lang]))
        input()

    def print_main_menu(self):
        print(tabulate(self.menu_service_info[self.lang]))
        print(tabulate(self.main_menu_text[self.lang], headers=self.menu_headers[self.lang], stralign="left"))

    def print_parser_menu(self):
        print(tabulate(self.parser_service_info[self.lang]))
        print(tabulate(self.parser_menu_text[self.lang], headers=self.menu_headers[self.lang], stralign="left"))

    @staticmethod
    def choose_league(league_list):
        leagues_list = [[pos, name] for pos, name in enumerate(league_list, 1)]
        print(tabulate(leagues_list))

    def choose_mode(self):
        modes = {"ru": [[1, "Оптовый"], ["", "Режим в котором учитывается количество валюты на руках"],
                        [2, "Штучный"], ["", "Режим в котором количество валюты на руках не учитывается"]],
                 "en": [[1, "Bulk"],
                        ["", "The mode in which the amount of currency on hand is taken into account"],
                        [2, "Retail"],
                        ["", "A mode in which the amount of currency on hand is not taken into account"]]}
        print(tabulate(modes[self.lang]))

    @staticmethod
    def choose_lang():
        langs = [[1, "Russian", "Русский"], [2, "English", "Английский"]]
        print(tabulate(langs))

    def print_result(self, count, price):
        result = {"ru": [[f"Вы получите {price} сфер хаоса за {count}"], [f"~price {price}/{count} chaos"]],
                  "en": [[f"You will receive {price} orb of chaos for {count}"], [f"~price {price}/{count} chaos"]]}
        print(tabulate(result[self.lang]))


class UpdaterViews:
    operations = {"ru": {1: "Операция обновления выполнена успешно"},
                  "en": {1: "Update successful"}}

    def print_update_operation(self, point):
        print(self.operations[MainMenuView().lang][point])


class Inputs:
    input_words = {"ru": {0: "Неверная команда, попробуйте ещё раз", 1: "Введите номер пункта меню: ",
                          2: "Введите количество: ", 3: "Для возврата к выбору категории, нажмите любую кнопку.\n"
                                                        "Для возврата в меню введите 1: ",
                          4: "Выберите режим: ", 5: "Выберите язык / Select language: "},
                   "en": {0: "Wrong input, try again", 1: "Select a menu item: ",
                          2: "Enter quantity: ", 3: "For back to select check another item, press any key.\n"
                                                    "For back to main menu, input 1: ",
                          4: "Select mode: ", 5: "Select language / Выберите язык: "}}

    def menu_selector(self, point):
        return input(self.input_words[MainMenuView().lang][point])

    def wrong_input_message(self):
        return self.input_words[MainMenuView().lang][0]

    def any_key(self):
        return input(self.input_words[MainMenuView().lang][3])


class ParserEvents:
    events = {"ru": {1: "Началось обновление базы, пожалуйста, подождите...", 2: "Обновление выполнено успешно."},
              "en": {1: "Start update item base, please wait...", 2: "Update successful."}}

    def print_event(self, event):
        print(self.events[MainMenuView().lang][event])


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
        message = {"ru": {1: 'Выберете раздел: ', 2: 'Выберете предмет: '},
                   "en": {1: 'Select category: ', 2: 'Select item: '}}
        return message[MainMenuView().lang][point]
