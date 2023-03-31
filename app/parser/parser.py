import json

from selenium import webdriver
import time


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
        print('wait...')
        for lang in self.langs:
            self.result_dic[lang] = {}
            self.driver.get(url=self.urls[lang])
            self.driver.add_cookie(
                {"name": "POESESSID",
                 "path": "/",
                 "domain": ".pathofexile.com",
                 "value": "b45a275ffb32515faf8de1e6f34af182"})
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
        print('done')

    def dict_to_json(self):
        with open("items.json", "w", encoding="utf-8") as file:
            json.dump(self.result_dic, file, indent=4)


print(Parser().result_dic)
Parser().parse()
print(Parser().result_dic)
Parser().dict_to_json()
