import os
from tabulate import tabulate

from app.parser.parser import FileUpdater, BrowserUpdater


class AppMenu:
    current_language = "En"
    current_league = "Sanctum"
    version_items = FileUpdater().check_version()
    version_browser = BrowserUpdater()

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
            menu_text = [[1, "Обмен валюты"], [2, "Обновление базы предметов", self.version_items],
                         [3, "Сменить язык"], [4, "Выход"]]
            headers = ["Номер", "Пункт", "База предметов"]
            print(tabulate(menu_text, headers=headers, stralign="left"))
            num = input("Введите номер пункта меню: ")
            os.system("CLS")
            match num:
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
        os.system("CLS")
        service_info = [["Версия установленного браузера:", self.version_browser.browser_version],
        ["Версия установленного веб драйвера:", self.version_browser.webdriver_version],
        ["", self.version_browser.check_version()], [], ["База предметов:", self.version_items]]
        print(tabulate(service_info))
        input()
