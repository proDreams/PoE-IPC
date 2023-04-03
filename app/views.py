from tabulate import tabulate

from app.config import Configuration


class MainMenuView:
    version_text = {1: "Обновление не требуется", 2: "Требуется обновление",
                    3: "Требуется обновление\nОбновление будет загружено автоматически."}
    menu_headers = ["Номер", "Пункт", "Версия"]
    main_menu_text = [[1, "Обмен предметов"],
                      [2, "Обновление базы предметов", version_text[Configuration().local_item_version]],
                      [3, "Сменить язык"], [4, "Выход"]]
    parser_menu_text = [[1, "Обновить базу предметов с сервера"], [2, "Обновить базу локально"],
                        [3, "Назад"]]
    parser_service_info = [["Версия установленного браузера:", Configuration().browser_version],
                           ["Версия установленного веб драйвера:", Configuration().webdriver_version],
                           ["", version_text[Configuration().browser_version_status]], [],
                           ["База предметов на сервере:", version_text[Configuration().server_item_version]],
                           ["Локальная база предметов:", version_text[Configuration().local_item_version]]]
    menu_service_info = [[f"Выбранный язык: {Configuration().current_league}"],
                         [f"Актуальная лига: {Configuration().current_league}"],
                         [f"Выбранная лига: {Configuration().current_language}"]]
    welcome_message_text = [["Добро пожаловать бла бла"], ["Для продолжения нажмите любую клавишу"]]

    def print_welcome_message(self):
        print(tabulate(self.welcome_message_text))
        input()

    def print_main_menu(self):
        print(tabulate(self.menu_service_info))
        print(tabulate(self.main_menu_text, headers=self.menu_headers, stralign="left"))

    def print_parser_menu(self):
        print(tabulate(self.parser_service_info))
        print(tabulate(self.parser_menu_text, headers=self.menu_headers, stralign="left"))


class UpdaterViews:
    operations = {1: "Операция обновления выполнена успешно"}

    def print_update_operation(self, point):
        print(self.operations[point])


class Inputs:
    input_words = {0: "Неверная команда, попробуйте ещё раз", 1: "Введите номер пункта меню: "}

    def menu_selector(self, point):
        return input(self.input_words[point])

    def wrong_input_message(self):
        return self.input_words[0]


class ParserEvents:
    events = {1: "Началось обновление базы, пожалуйста, подождите...", 2: "Обновление выполнено успешно."}

    def print_event(self, event):
        print(self.events[event])
