import os
import requests as requests
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import json

from app.config import Configuration


class Parse:
    urls = {"en": "https://www.pathofexile.com/trade/about",
            "ru": "https://ru.pathofexile.com/trade/about"}
    langs = ["en", "ru"]
    result_dic = {"League": Configuration().current_league}

    def __init__(self):
        os.environ['WDM_LOCAL'] = '1'
        options = webdriver.EdgeOptions()
        options.use_chromium = True
        options.add_argument("headless")
        options.add_argument("disable-gpu")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver_path = EdgeChromiumDriverManager().install()
        self.driver = webdriver.Edge(executable_path=driver_path, options=options)

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
                 "value": Configuration().poesessid})
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

    def update_file(self):
        response = requests.get(self.file_url)
        with open("items.json", "w", encoding="utf-8") as jsonFile:
            json.dump(response.json(), jsonFile, indent=4)


class VersionInfo:
    current_league = "Sanctum"
    webdriver_version = EdgeChromiumDriverManager().driver.get_browser_version()
    browser_version = os.popen(
        "powershell.exe "
        "(Get-ItemProperty -Path HKCU:\\Software\\Microsoft\\Edge\\BLBeacon "
        "-Name version).version").read().strip()[:-3]
    file_url = "https://raw.githubusercontent.com/proDreams/PoETRY/main/app/parser/items.json"

    def check_browser_version(self):
        if self.webdriver_version == self.browser_version:
            return 1
        else:
            return 3

    def check_server_version(self):
        response = requests.get(self.file_url)
        if response.json()["League"] == self.current_league:
            return 1
        else:
            return 2

    def check_local_version(self):
        with open("items.json", "r") as jsonFile:
            items = json.load(jsonFile)
            if items["League"] == self.current_league:
                return 1
            else:
                return 2
