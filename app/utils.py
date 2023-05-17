import json
import requests
from selenium import webdriver
from selenium.common import NoSuchElementException
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import os
import time
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

    def parse(self, actual_league, poesessid):
        """
        Parsing about page on PoE trade site
        """
        result_dic = {"League": actual_league}
        for lang in self.langs:
            print(lang)
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
                        if any(blocked_word in item_alt_name for blocked_word in blocked_words):
                            continue
                        try:
                            img = item.find_element("tag name", "img")
                        except NoSuchElementException:
                            img = None
                        if img:
                            img = img.get_attribute("src")
                            response = requests.get(img)
                            directory = f"assets/img/{lang}/{category_name}"
                            if not os.path.exists(directory):
                                os.makedirs(directory)
                            with open(f"{directory}/{item_alt_name}.png", "wb") as image:
                                image.write(response.content)
                            result_dic[lang][category_name].update(
                                {item_name: {"item_alt_name": item_alt_name,
                                             "img": f"assets/img/{lang}/{category_name}/{item_alt_name}.png"}})
                        else:
                            result_dic[lang][category_name].update(
                                {item_name: {"item_alt_name": item_alt_name,
                                             "img": "None"}})
                    print(category_name)
        self.driver.close()
        self.driver.quit()
        print("done")
        with open("items.json", "w", encoding="utf-8") as jsonFile:
            json.dump(result_dic, jsonFile, indent=4)


def update_from_server():
    items_url = "https://raw.githubusercontent.com/proDreams/PoETRY/main/items.json"
    response = requests.get(items_url)
    with open("items.json", "w", encoding="utf-8") as jsonFile:
        json.dump(response.json(), jsonFile, indent=4)


def get_categories(lang):
    with open("items.json", "r") as jsonFile:
        items = json.load(jsonFile)
        return [key for key in items[lang].keys()]


def get_items(lang, category):
    with open("items.json", "r") as jsonFile:
        items = json.load(jsonFile)
        return [[key, items[lang][category][key]["img"]] for key in
                items[lang][category].keys()]


def get_alt_name(lang, category, item):
    with open("items.json", "r") as jsonFile:
        items = json.load(jsonFile)
    return items[lang][category][item]["item_alt_name"]


def check_price(want, league, quant=1, have='chaos'):
    url_currency = "https://www.pathofexile.com/api/trade/exchange/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212",
        "From": "youremail@domain.com"
    }
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
    respond = requests.post(url_currency + league, json=data, headers=headers)
    respond = respond.json()
    for dd in respond["result"]:
        chaos = (respond['result'][dd]['listing']['offers'][0]['exchange']['amount'])
        curr = (respond['result'][dd]['listing']['offers'][0]['item']['amount'])
        price_catalog.append(chaos / curr)
    price_catalog = price_catalog[:20]
    try:
        total_price = round((stat.mean(price_catalog[2:]) + stat.median(price_catalog[2:])) / 2, 4)
    except stat.StatisticsError:
        return None
    total = float(quant) * total_price
    total_x = int(total)
    total_y = total % 1
    return total_x, int(quant - (total_y // total_price))
