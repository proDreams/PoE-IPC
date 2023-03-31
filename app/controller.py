import os
from tabulate import tabulate

from app.parser.parser import FileUpdater, BrowserUpdater, Parse


class AppMenu:
    current_language = "En"
    current_league = "Sanctum"
    version_items = FileUpdater()
    version_browser = BrowserUpdater()
    headers = ["Номер", "Пункт", "Версия"]

    def __init__(self):
        print("Добро пожаловать бла бла")
        print("Для продолжения нажмите любую клавишу")
        input()
        self.main_menu()

    def main_menu(self):
        os.system("CLS")
        running = True
        while running:
            print(f"Текущая лига: {self.current_league}")
            menu_text = [[1, "Обмен валюты"],
                         [2, "Обновление базы предметов", self.version_items.check_local_version()],
                         [3, "Сменить язык"], [4, "Выход"]]
            print(tabulate(menu_text, headers=self.headers, stralign="left"))
            select = input("Введите номер пункта меню: ")
            os.system("CLS")
            match select:
                case "1":
                    pass
                case "2":
                    self.parser_menu()
                case "3":
                    pass
                case "4":
                    running = False
                case _:
                    "Неверная команда, попробуйте ещё раз"

    def parser_menu(self):
        running = True
        os.system("CLS")
        while running:

            service_info = [["Версия установленного браузера:", self.version_browser.browser_version],
                            ["Версия установленного веб драйвера:", self.version_browser.webdriver_version],
                            ["", self.version_browser.check_version()], [],
                            ["База предметов на сервере:", self.version_items.check_server_version()],
                            ["Локальная база предметов:", self.version_items.check_local_version()]]
            print(tabulate(service_info))
            parser_menu_text = [[1, "Обновить базу предметов с сервера"], [2, "Обновить базу локально"], [3, "Назад"]]
            print(tabulate(parser_menu_text, headers=self.headers, stralign="left"))
            select = input("Введите номер пункта меню: ")
            os.system("CLS")
            match select:
                case "1":
                    print(self.version_items.update_file())
                case "2":
                    Parse().parse()
                    print("Обновление выполнено2")
                case "3":
                    running = False
                case _:
                    "Неверная команда, попробуйте ещё раз"
