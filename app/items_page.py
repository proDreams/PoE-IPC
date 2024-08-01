import pyperclip
from flet import (
    UserControl,
    Text,
    ElevatedButton,
    Row,
    Image,
    ScrollMode,
    BottomSheet,
    Container,
    Column,
    TextField,
    ProgressRing,
)

from app import text_constants, utils


class Items(UserControl):
    def __init__(self):
        super().__init__()
        self.not_enough_offers = Text(
            text_constants.error_text[text_constants.current_lang]["not_enough_offers"],
            size=18,
            visible=False,
        )
        self.bs = BottomSheet(content=self)
        self.quantity_input = TextField(
            label=text_constants.pricer_text[text_constants.current_lang]["quantity"],
            height=60,
            autofocus=True,
            on_submit=self.check_price,
        )
        self.quantity_submit = ElevatedButton(
            text=text_constants.settings_version_text[text_constants.current_lang][
                "submit"
            ],
            on_click=self.check_price,
        )
        self.input_row = Row([self.quantity_input, self.quantity_submit])
        self.quantity = Text(
            text_constants.pricer_text[text_constants.current_lang]["quantity"]
        )
        self.receive_label = Text("", width=200)
        self.receive_content = Text("")
        self.receive_row = Row(
            [self.receive_label, self.receive_content], visible=False
        )
        self.for_label = Text("", width=200)
        self.for_content = Text("")
        self.for_row = Row([self.for_label, self.for_content], visible=False)
        self.game_string = Text(
            text_constants.pricer_text[text_constants.current_lang]["game_string"],
            visible=False,
        )
        self.raw_game_string = Text("", width=200, selectable=True)
        self.copy_game_string = ElevatedButton(
            text_constants.pricer_text[text_constants.current_lang][
                "copy_to_clipboard"
            ],
            visible=False,
            on_click=self.copy_string,
        )
        self.game_string_row = Row(
            [self.raw_game_string, self.copy_game_string], visible=False
        )

        self.pricing_ring = ProgressRing(visible=False)
        self.items_list = utils.get_items(
            text_constants.current_lang, text_constants.selected_category
        )
        self.containers = Row(wrap=True)
        self.lang = text_constants.current_lang
        self.category = text_constants.selected_category
        max_size = max([len(i[0]) for i in self.items_list]) * 10
        for item in self.items_list:
            if item[1] == "None":
                row_elements = Row(
                    [
                        Image(
                            src="img/img.png",
                            width=48,
                            height=48,
                        ),
                        Text(item[0], size=14),
                    ],
                    scroll=ScrollMode.AUTO,
                )
            else:
                row_elements = Row(
                    [
                        Image(
                            src=item[1],
                            width=48,
                            height=48,
                        ),
                        Text(item[0], size=14),
                    ],
                    scroll=ScrollMode.AUTO,
                )

            btn = ElevatedButton(
                content=Container(
                    row_elements,
                    width=max_size,
                    height=60,
                ),
                on_click=self.open_item_pricer,
            )
            self.containers.controls.append(btn)

    def build(self):
        return self.containers

    def open_item_pricer(self, e):
        text_constants.selected_item = e.control.content.content.controls[1].value
        selected_category = Row(
            [
                Text(
                    text_constants.pricer_text[text_constants.current_lang][
                        "selected_category"
                    ],
                    width=200,
                ),
                Text(text_constants.selected_category),
            ]
        )
        selected_item = Row(
            [
                Text(
                    text_constants.pricer_text[text_constants.current_lang][
                        "selected_item"
                    ],
                    width=200,
                ),
                Text(text_constants.selected_item),
            ]
        )
        self.bs = BottomSheet(
            Container(
                Column(
                    [
                        selected_category,
                        selected_item,
                        self.quantity,
                        self.input_row,
                        self.pricing_ring,
                        self.not_enough_offers,
                        self.receive_row,
                        self.for_row,
                        self.game_string,
                        self.game_string_row,
                    ],
                    tight=True,
                    width=500,
                ),
                padding=30,
            ),
            open=True,
            on_dismiss=self.change_visible,
        )
        self.page.overlay.append(self.bs)
        self.page.update()

    def check_price(self, e):
        self.quantity.visible = False
        self.input_row.visible = False
        self.pricing_ring.visible = True
        self.page.update()
        result = utils.check_price(
            want=utils.get_alt_name(
                text_constants.current_lang,
                text_constants.selected_category,
                text_constants.selected_item,
            ),
            league=text_constants.selected_league,
            quant=int(self.quantity_input.value),
        )
        if result:
            self.pricing_ring.visible = False
            self.receive_label.value = text_constants.pricer_text[
                text_constants.current_lang
            ]["receive"]
            self.receive_content.value = result[0]
            self.for_label.value = text_constants.pricer_text[
                text_constants.current_lang
            ]["for"]
            self.for_content.value = result[1]
            self.raw_game_string.value = f"~price {result[0]}/{result[1]} chaos"

            self.copy_game_string.visible = True
            self.receive_row.visible = True
            self.for_row.visible = True
            self.game_string.visible = True
            self.game_string_row.visible = True
            self.page.update()
        else:
            self.pricing_ring.visible = False
            self.not_enough_offers.visible = True
            self.page.update()

    def copy_string(self, e):
        pyperclip.copy(self.raw_game_string.value)

    def change_visible(self, e):
        self.copy_game_string.visible = False
        self.receive_row.visible = False
        self.for_row.visible = False
        self.game_string.visible = False
        self.game_string_row.visible = False
        self.quantity.visible = True
        self.quantity_input.value = ""
        self.input_row.visible = True
        self.not_enough_offers.visible = False
        self.page.update()
