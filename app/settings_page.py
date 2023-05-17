import yaml
from flet import (UserControl,
                  Text,
                  Dropdown,
                  dropdown,
                  Column,
                  Divider,
                  CrossAxisAlignment,
                  ElevatedButton,
                  AlertDialog,
                  ProgressRing,
                  TextField,
                  Row,
                  MainAxisAlignment)

from app import text_constants, utils


class Settings(UserControl):
    def __init__(self):
        super().__init__()
        self.lang_label = Text(text_constants.settings_language_text[text_constants.current_lang]["label"],
                               size=18,
                               weight="bold")

        self.lang_change = Text(text_constants.settings_language_text[text_constants.current_lang]["change"])
        self.lang_dd = Dropdown(
            width=250,
            options=[
                dropdown.Option(key="ru",
                                text=text_constants.settings_language_text[text_constants.current_lang]["ru"]),
                dropdown.Option(key="en",
                                text=text_constants.settings_language_text[text_constants.current_lang]["en"]),
            ],
            label=text_constants.settings_language_text[text_constants.current_lang][text_constants.current_lang],
            border_radius=5,
            on_change=self.change_lang
        )
        self.mode_label = Text(text_constants.settings_mode_text[text_constants.current_lang]["label"],
                               size=18,
                               weight="bold")

        self.mode_change = Text(text_constants.settings_mode_text[text_constants.current_lang]["change"])
        self.mode_dd = Dropdown(
            width=200,
            options=[
                dropdown.Option(key="bulk",
                                text=text_constants.settings_mode_text[text_constants.current_lang]["bulk"]),
                dropdown.Option(key="retail",
                                text=text_constants.settings_mode_text[text_constants.current_lang]["retail"]),
            ],
            label=text_constants.settings_mode_text[text_constants.current_lang][text_constants.current_mode],
            border_radius=5,
            on_change=self.change_mode
        )
        self.leagues_list = text_constants.list_leagues
        self.league_label = Text(text_constants.settings_league_text[text_constants.current_lang]["label"],
                                 size=18,
                                 weight="bold")

        self.actual_label = Text(text_constants.settings_league_text[text_constants.current_lang]["actual"],
                                 width=200)
        self.actual_content = Text(self.leagues_list[4])
        self.actual_row = Row(
            [
                self.actual_label,
                self.actual_content
            ],
            alignment=MainAxisAlignment.CENTER
        )

        self.selected_content = Text(text_constants.selected_league)

        self.league_change = Text(text_constants.settings_league_text[text_constants.current_lang]["change"])
        self.leagues_dd = Dropdown(
            width=250,
            options=[dropdown.Option(league) for league in self.leagues_list],
            border_radius=5,
            on_change=self.change_league,
            label=text_constants.selected_league
        )

    def change_mode(self, e):
        if text_constants.current_mode != self.mode_dd.value:
            with open('config.yaml') as f:
                conf = yaml.safe_load(f)

            conf['trade_mode'] = self.mode_dd.value
            text_constants.current_mode = self.mode_dd.value

            with open('config.yaml', 'w') as f:
                yaml.safe_dump(conf, f)
            self.update()

    def change_lang(self, e):
        if text_constants.current_lang != self.lang_dd.value:
            with open('config.yaml') as f:
                conf = yaml.safe_load(f)

            conf['current_language'] = self.lang_dd.value

            with open('config.yaml', 'w') as f:
                yaml.safe_dump(conf, f)

            dlg = AlertDialog(title=Text(text_constants.settings_dialog_text[self.lang_dd.value]["restart_app"]))
            self.page.dialog = dlg
            self.page.dialog.open = True
            self.page.update()

    def change_league(self, e):
        if text_constants.selected_league != self.leagues_dd.value:
            with open('config.yaml') as f:
                conf = yaml.safe_load(f)

            conf['selected_league'] = self.leagues_dd.value
            text_constants.selected_league = self.leagues_dd.value

            with open('config.yaml', 'w') as f:
                yaml.safe_dump(conf, f)
            self.selected_content.value = text_constants.selected_league
            self.update()

    def build(self):
        return Column(
            [self.lang_label,
             self.lang_change,
             self.lang_dd,
             Divider(),
             self.mode_label,
             self.mode_change,
             self.mode_dd,
             Divider(),
             self.league_label,
             self.actual_row,
             self.league_change,
             self.leagues_dd,
             ],
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )


class SettingsVersion(UserControl):
    def __init__(self):
        super().__init__()
        self.label = Text(text_constants.settings_version_text[text_constants.current_lang]["label"],
                          size=18,
                          weight="bold")

        self.server_base_label = Text(text_constants.settings_version_text[text_constants.current_lang]["server"],
                                      width=250)
        self.server_base_content = Text(text_constants.server_base)
        self.server_base_row = Row(
            [
                self.server_base_label,
                self.server_base_content
            ],
            alignment=MainAxisAlignment.CENTER
        )

        self.local_base_label = Text(text_constants.settings_version_text[text_constants.current_lang]["local"],
                                     width=250)
        self.local_base_content = Text(text_constants.local_base)
        self.local_base_row = Row(
            [
                self.local_base_label,
                self.local_base_content
            ],
            alignment=MainAxisAlignment.CENTER
        )

        self.update_required_label = Text(
            text_constants.settings_version_text[text_constants.current_lang]["need_update"],
            width=220)
        self.update_required_content = Text(text_constants.required)
        self.update_required_row = Row(
            [
                self.update_required_label,
                self.update_required_content
            ],
            alignment=MainAxisAlignment.CENTER
        )

        self.server_update_btn = ElevatedButton(
            text_constants.settings_version_text[text_constants.current_lang]["server_btn"],
            on_click=self.server_update)
        self.local_update_btn = ElevatedButton(
            text_constants.settings_version_text[text_constants.current_lang]["local_btn"],
            on_click=self.enter_poesessid)
        self.local_updating_ring = ProgressRing(visible=False)
        self.local_update_complete = Text(
            text_constants.settings_version_text[text_constants.current_lang]["update_complete"],
            visible=False)
        self.server_updating_ring = ProgressRing(visible=False)
        self.server_update_complete = Text(
            text_constants.settings_version_text[text_constants.current_lang]["update_complete"],
            visible=False)
        self.poesessid_input = TextField(
            label=text_constants.settings_version_text[text_constants.current_lang]["poesessid_input"], height=60)
        self.poesessid_submit = ElevatedButton(
            text=text_constants.settings_version_text[text_constants.current_lang]["submit"],
            on_click=self.local_update)
        self.input_row = Row([self.poesessid_input,
                              self.poesessid_submit],
                             visible=False)

    def build(self):
        return Column([self.label,
                       Divider(),
                       self.server_base_row,
                       self.local_base_row,
                       self.update_required_row,
                       Divider(),
                       self.server_update_btn,
                       self.server_updating_ring,
                       self.server_update_complete,
                       self.local_update_btn,
                       self.local_updating_ring,
                       self.local_update_complete,
                       self.input_row,
                       ],
                      horizontal_alignment=CrossAxisAlignment.CENTER,
                      )

    def server_update(self, e):
        if text_constants.server_base == text_constants.local_base:
            dlg = AlertDialog(title=Text(
                text_constants.settings_dialog_text[text_constants.current_lang]["update_not_required"]))
            self.page.dialog = dlg
            self.page.dialog.open = True
            self.page.update()
        else:
            self.server_update_btn.visible = False
            self.server_updating_ring.visible = True
            self.update()
            utils.update_from_server()
            self.server_updating_ring.visible = False
            self.server_update_complete.visible = True
            text_constants.local_base = text_constants.get_local_base()
            self.local_base_content.value = text_constants.local_base
            text_constants.required = text_constants.check_required()
            self.update_required_content.value = text_constants.required
            self.update()

    def enter_poesessid(self, e):
        if text_constants.server_base == text_constants.local_base:
            dlg = AlertDialog(title=Text(
                text_constants.settings_dialog_text[text_constants.current_lang]["update_not_required"]))
            self.page.dialog = dlg
            self.page.dialog.open = True
            self.page.update()
        else:
            self.local_update_btn.visible = False
            self.input_row.visible = True
            self.update()

    def local_update(self, e):
        self.input_row.visible = False
        self.server_updating_ring.visible = True
        self.update()
        utils.Parse().parse(actual_league=text_constants.list_leagues[4],
                            poesessid=self.poesessid_input.value)
        self.server_updating_ring.visible = False
        self.server_update_complete.visible = True
        self.update()
        text_constants.local_base = text_constants.get_local_base()
        self.local_base_content.value = text_constants.local_base
        text_constants.required = text_constants.check_required()
        self.update_required_content.value = text_constants.required
        self.update()
