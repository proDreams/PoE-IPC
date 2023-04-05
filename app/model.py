import os
import requests as requests
import yaml
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import json
import statistics as stat


class Parse:
    urls = {"en": "https://www.pathofexile.com/trade/about",
            "ru": "https://ru.pathofexile.com/trade/about"}
    langs = ["en", "ru"]

    def __init__(self):

        os.environ['WDM_LOCAL'] = '1'
        options = webdriver.EdgeOptions()
        options.use_chromium = True
        options.add_argument("headless")
        options.add_argument("disable-gpu")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver_path = EdgeChromiumDriverManager().install()
        self.driver = webdriver.Edge(executable_path=driver_path, options=options)

    def parse(self, actual_league=None, poesessid=None):
        """
        Parsing about page on PoE trade site
        """
        result_dic = {"League": actual_league}
        for lang in self.langs:
            result_dic[lang] = {}
            self.driver.get(url=self.urls[lang])
            self.driver.add_cookie(
                {"name": "POESESSID",
                 "path": "/",
                 "domain": ".pathofexile.com",
                 "value": poesessid})
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
                    result_dic[lang][category_name] = {}
                    item_list = category.find_element("class name", "filter-group-body")
                    items = item_list.find_elements("class name", "filter")
                    for item in items:
                        item_name = item.find_element("class name", "filter-title").get_attribute("textContent").strip()
                        item_alt_name = item.find_element("class name", "form-control").get_attribute("value")
                        blocked_words = ["whispering", "muttering", "weeping", "wailing", "screaming"]
                        if any(word in blocked_words for word in item_alt_name):
                            continue
                        result_dic[lang][category_name].update({item_name: item_alt_name})
        self.driver.close()
        self.driver.quit()
        with open("items.json", "w", encoding="utf-8") as jsonFile:
            json.dump(result_dic, jsonFile, indent=4)


class Data:
    items_url = "https://raw.githubusercontent.com/proDreams/PoETRY/main/items.json"
    config_url = "https://raw.githubusercontent.com/proDreams/PoETRY/main/config.yaml"

    def get_server_version(self):
        response = requests.get(self.items_url)
        return response.json()["League"]

    @staticmethod
    def get_local_version():
        with open("items.json", "r") as jsonFile:
            items = json.load(jsonFile)
            return items["League"]

    def update_file(self):
        response = requests.get(self.items_url)
        with open("items.json", "w", encoding="utf-8") as jsonFile:
            json.dump(response.json(), jsonFile, indent=4)

    @staticmethod
    def get_items(current_language):
        with open("items.json", "r") as jsonFile:
            items = json.load(jsonFile)
            return items[current_language]

    def get_version(self):
        response = requests.get(self.config_url)
        return yaml.safe_load(response.content)["version"]


class GetFromApi:
    url_leagues = "https://api.pathofexile.com/leagues"
    url_currency = "https://www.pathofexile.com/api/trade/exchange/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212",
        "From": "youremail@domain.com"
    }

    def get_leagues(self):
        leagues_response = requests.get(self.url_leagues, headers=self.headers)
        leagues = json.loads(leagues_response.text)
        leagues_list = [i.get('id') for i in leagues if 'SSF' not in i.get('id')]
        return leagues_list

    def get_currency_price(self, want, cl, quant=1, have='chaos'):
        price_catalog = []
        data = {
            "exchange": {
                "want": [want],
                "have": [have],
                "minimum": quant,
                "status": "online"
            },
            "engine": "new"
        }
        respond = requests.post(self.url_currency + cl, json=data, headers=self.headers)
        respond = respond.json()
        for dd in respond["result"]:
            chaos = (respond['result'][dd]['listing']['offers'][0]['exchange']['amount'])
            curr = (respond['result'][dd]['listing']['offers'][0]['item']['amount'])
            price_catalog.append(chaos / curr)
        price_catalog = price_catalog[:20]
        total_price = round((stat.mean(price_catalog[2:]) + stat.median(price_catalog[2:])) / 2, 4)
        return total_price

    @staticmethod
    def calculate_result(count, price):
        total = float(count) * price
        total_x = int(total)
        total_y = total % 1
        return total_x, int(count - (total_y // price))
