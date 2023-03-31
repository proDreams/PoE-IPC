import requests as requests
from selenium import webdriver
import time
import json


class Parser:
    options = webdriver.EdgeOptions()
    options.use_chromium = True
    options.add_argument("headless")
    options.add_argument("disable-gpu")
    urls = {"en": "https://www.pathofexile.com/trade/about",
            "ru": "https://ru.pathofexile.com/trade/about"}
    driver = webdriver.Edge(executable_path="msedgedriver.exe", options=options)
    langs = ["en", "ru"]
    result_dic = {"League": "Sanctum"}

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

    def check_version(self):
        response = requests.get(self.file_url)
        if response.json()["League"] == self.current_league:
            print("Same")
        else:
            print("Not same")

    def update_file(self):
        response = requests.get(self.file_url)
        with open("items.json", "w", encoding="utf-8") as jsonFile:
            json.dump(response.json(), jsonFile, indent=4)

# Parser().parse()
# FileUpdater().check_version()
