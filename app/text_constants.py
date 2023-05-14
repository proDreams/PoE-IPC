import yaml
import json
import requests


def get_current_lang():
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
    return config["current_language"]


def get_leagues():
    url_leagues = "https://api.pathofexile.com/leagues"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212",
        "From": "youremail@domain.com"
    }

    leagues_response = requests.get(url_leagues, headers=headers)
    leagues = json.loads(leagues_response.text)
    leagues_list = [i.get('id') for i in leagues if 'SSF' not in i.get('id') and 'Solo' not in i.get('id')]
    return leagues_list


def get_local_base():
    with open("items.json", "r") as jsonFile:
        items = json.load(jsonFile)
    return items["League"]


def get_server_base():
    items_url = "https://raw.githubusercontent.com/proDreams/PoETRY/main/items.json"
    response = requests.get(items_url)
    return response.json()["League"]


def check_required():
    if local_base != server_base:
        return settings_version_text[current_lang]["required"]
    return settings_version_text[current_lang]["not_required"]


def get_current_mode():
    with open('config.yaml') as f:
        conf = yaml.safe_load(f)
    return conf["trade_mode"]


def get_selected_league():
    with open('config.yaml') as f:
        conf = yaml.safe_load(f)
    return conf["selected_league"]


def get_version():
    with open('config.yaml') as f:
        conf = yaml.safe_load(f)
    return conf["version"]


settings_language_text = {"ru": {"label": "Язык/Language:",
                                 "ru": "Русский/Russian",
                                 "en": "Английский/English",
                                 "current": "Текущий язык:",
                                 "change": "Сменить язык/Change language:"},
                          "en": {"label": "Language/Язык",
                                 "ru": "Russian/Русский",
                                 "en": "English/Английский",
                                 "current": "Current language:",
                                 "change": "Change language/Сменить язык:"}
                          }
settings_league_text = {"ru": {"label": "Лига:",
                               "actual": "Актуальная лига:",
                               "change": "Выбрать лигу:",
                               "selected": "Выбранная лига:"},
                        "en": {"label": "League:",
                               "actual": "Actual league:",
                               "change": "Choose league:",
                               "selected": "Selected league:"}
                        }
settings_version_text = {"ru": {"label": "Состояние базы предметов:",
                                "server": "База предметов на сервере:",
                                "local": "Локальная база предметов:",
                                "need_update": "Обновление:",
                                "required": "Требуется",
                                "not_required": "Не требуется",
                                "local_btn": "Обновить локально",
                                "server_btn": "Обновить с сервера",
                                "update_complete": "База обновлена успешно",
                                "poesessid_input": "Введите ваш POESESSID",
                                "submit": "Применить"},
                         "en": {"label": "Item base status:",
                                "server": "Items base on server:",
                                "local": "Local items base:",
                                "need_update": "Update:",
                                "required": "Required",
                                "not_required": "Not required",
                                "local_btn": "Update locally",
                                "server_btn": "Update from server",
                                "update_complete": "Base update successful",
                                "poesessid_input": "Enter your POESESSID",
                                "submit": "Submit"}
                         }
settings_dialog_text = {"ru": {"restart_app": "Пожалуйста, перезапустите приложение, для применения изменений.",
                               "update_not_required": "Обновление базы не требуется!"},
                        "en": {"restart_app": "Please restart the application to apply the changes.",
                               "update_not_required": "Base update not required!"}
                        }
settings_mode_text = {"ru": {"label": "Режим торговли:",
                             "current": "Текущий режим торговли:",
                             "bulk": "Оптовый",
                             "retail": "Штучный",
                             "change": "Выберите режим:"},
                      "en": {"label": "Trade mode:",
                             "current": "Current trade mode:",
                             "bulk": "Bulk",
                             "retail": "Retail",
                             "change": "Choice trade mode:"}
                      }

about_text = {"ru": {"label": "О программе",
                     "description": "Приложение для расчёта оптимального соотношения цены предмета к сферам хаоса",
                     "version": "Версия приложения:",
                     "author": "Автор:",
                     "author_name": "Иван Ашихмин",
                     "github": "Страница проекта:"},
              "en": {"label": "About",
                     "description":
                         "Application for calculating the optimal ratio of the price of an item to chaos orbs",
                     "version": "Application version:",
                     "author": "Author:",
                     "author_name": "Ivan Ashikhmin",
                     "github": "Project page:"}
              }

app_bar_text = {"ru": {"title": "PoETRY",
                       "about": "О программе",
                       "settings": "Настройки"},
                "en": {"title": "PoETRY",
                       "about": "About",
                       "settings": "Settings"}
                }

main_text = {"ru": {"select_category": "Выберите категорию:", },
             "en": {"select_category": "Select category:", }
             }

pricer_text = {"ru": {"selected_item": "Выбранный предмет:",
                      "selected_category": "Выбранная категория:",
                      "quantity": "Введите количество",
                      "receive": "Вы получите сфер хаоса:",
                      "for": "За:",
                      "game_string": "Строка для вставки в игре:",
                      "copy_to_clipboard": "Копировать"},
               "en": {"selected_item": "Selected item:",
                      "selected_category": "Selected category:",
                      "quantity": "Enter quantity",
                      "receive": "You receive chaos orbs:",
                      "for": "For:",
                      "game_string": "String for input in game:",
                      "copy_to_clipboard": "Copy"}
               }

current_lang = get_current_lang()
list_leagues = get_leagues()
local_base = get_local_base()
server_base = get_server_base()
required = check_required()
current_mode = get_current_mode()
selected_league = get_selected_league()
version = get_version()
selected_category = None
selected_item = None
