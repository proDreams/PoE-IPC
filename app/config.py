import yaml


class Configuration:
    current_league = 'None'
    current_language = 'None'
    poesessid = 'None'
    local_item_version = 'None2'
    server_item_version = 'None'
    browser_version = 'None'
    webdriver_version = 'None'
    browser_version_status = 'None'

    def __init__(self):
        with open("config.yaml") as f:
            config = yaml.safe_load(f)
        self.current_league = config["current_league"]
        self.current_language = config["current_language"]
        self.poesessid = config["poesessid"]

    @staticmethod
    def set_versions(local_item_version, server_item_version, browser_version, webdriver_version,
                     browser_version_status):
        Configuration.local_item_version = local_item_version
        Configuration.server_item_version = server_item_version
        Configuration.browser_version = browser_version
        Configuration.webdriver_version = webdriver_version
        Configuration.browser_version_status = browser_version_status
