import os
import requests as requests
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import json


class Parse:
    urls = {"en": "https://www.pathofexile.com/trade/about",
            "ru": "https://ru.pathofexile.com/trade/about"}
    langs = ["en", "ru"]
    result_dic = {"League": "Sanctum"}

    def __init__(self):
        os.environ['WDM_LOCAL'] = '1'
        options = webdriver.EdgeOptions()
        options.use_chromium = True
        options.add_argument("headless")
        options.add_argument("disable-gpu")
        self.driver = webdriver.Edge(
            executable_path=EdgeChromiumDriverManager(version=BrowserUpdater().browser_version).install(),
            options=options)

    def parse(self):
        """
        Parsing about page on PoE trade site
        """

        for lang in self.langs:
            self.result_dic[lang] = {}
            self.driver.get(url=self.urls[lang])
            self.driver.add_cookie(
                {"name": "POESESSID",
                 "path": "/",
                 "domain": ".pathofexile.com",
                 "value": "ENTER POESESSID"})
            self.driver.get(url=self.urls[lang])
            time.sleep(5)
            start_point = self.driver.find_element("class name", "search-bar.about")
            second_point = start_point.find_elements("class name", "filter-group")
            for category in second_point:
                if ("Item Tags" in category.text and
                    "Maps" not in category.text and
                    "Cards" not in category.text) or (
                        "Тэги предмета - " in category.text and
                        "Карты" not in category.text and
                        "Гадальные карты" not in category.text):
                    category_name = category.text.replace("Item Tags - ", "").replace("Тэги предмета - ", "")
                    self.result_dic[lang][category_name] = {}
                    item_list = category.find_element("class name", "filter-group-body")
                    items = item_list.find_elements("class name", "filter")
                    for item in items:
                        item_name = item.find_element("class name", "filter-title").get_attribute("textContent").strip()
                        item_alt_name = item.find_element("class name", "form-control").get_attribute("value")
                        blocked_words = ["whispering", "muttering", "weeping", "wailing", "screaming"]
                        if any(word in blocked_words for word in item_alt_name):
                            continue
                        self.result_dic[lang][category_name].update({item_name: item_alt_name})
        self.driver.close()
        self.driver.quit()
        with open("items.json", "w", encoding="utf-8") as jsonFile:
            json.dump(self.result_dic, jsonFile, indent=4)


class FileUpdater:
    file_url = "https://raw.githubusercontent.com/proDreams/PoETRY/main/app/parser/items.json"
    current_league = "Sanctum"

    def check_version(self) -> str:
        response = requests.get(self.file_url)
        if response.json()["League"] == self.current_league:
            return "Обновление не требуется"
        else:
            return "Требуется обновление"

    def update_file(self):
        response = requests.get(self.file_url)
        with open("items.json", "w", encoding="utf-8") as jsonFile:
            json.dump(response.json(), jsonFile, indent=4)


class BrowserUpdater:
    webdriver_version = EdgeChromiumDriverManager().driver.get_browser_version()
    browser_version = os.popen(
        "powershell.exe "
        "(Get-ItemProperty -Path HKCU:\\Software\\Microsoft\\Edge\\BLBeacon "
        "-Name version).version").read().strip()[:-3]

    def check_version(self) -> str:
        if self.webdriver_version == self.browser_version:
            return "Обновление не требуется"
        else:
            return "Требуется обновление"


# Parse().parse()
# FileUpdater().check_version()
# print(BrowserUpdater().check_version())
# print(BrowserUpdater().webdriver_version)
# print(BrowserUpdater().driver_binary)
