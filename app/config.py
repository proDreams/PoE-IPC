import yaml


class Configuration:
    def __init__(self):
        with open("config.yaml") as f:
            config = yaml.safe_load(f)
        self._selected_league = config["selected_league"]
        self._current_language = config["current_language"]
        self._poesessid = config["poesessid"]
        self._actual_league = 2
        self._browser_version_status = 2
        self._local_item_version = 2
        self._server_item_version = 2
        self._browser_version = 2
        self._webdriver_version = 2

    @property
    def selected_league(self):
        return self._selected_league

    @property
    def actual_league(self):
        return self._actual_league

    @property
    def current_language(self):
        return self._current_language

    @property
    def poesessid(self):
        return self._poesessid

    @property
    def browser_version_status(self):
        return self._browser_version_status

    @property
    def local_item_version(self):
        return self._local_item_version

    @property
    def server_item_version(self):
        return self._server_item_version

    @property
    def browser_version(self):
        return self._browser_version

    @property
    def webdriver_version(self):
        return self._webdriver_version

    @selected_league.setter
    def selected_league(self, value):
        self._selected_league = value

    @actual_league.setter
    def actual_league(self, value):
        self._actual_league = value

    @current_language.setter
    def current_language(self, value):
        self._current_language = value

    @webdriver_version.setter
    def webdriver_version(self, value):
        self._webdriver_version = value

    @browser_version.setter
    def browser_version(self, value):
        self._browser_version = value

    @server_item_version.setter
    def server_item_version(self, value):
        self._server_item_version = value

    @local_item_version.setter
    def local_item_version(self, value):
        self._local_item_version = value

    @browser_version_status.setter
    def browser_version_status(self, value):
        self._browser_version_status = value

    @poesessid.setter
    def poesessid(self, value):
        self._poesessid = value

    def set_league(self, league):
        with open('config.yaml') as f:
            conf = yaml.safe_load(f)

        conf['selected_league'] = league

        with open('config.yaml', 'w') as f:
            yaml.safe_dump(conf, f)
        self._selected_league = league
