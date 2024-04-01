from flet import UserControl, Text, ElevatedButton, Row, Container

from app import text_constants, utils


class Categories(UserControl):
    def __init__(self):
        super().__init__()
        self.categories_list = utils.get_categories(text_constants.current_lang)
        self.containers = Row(wrap=True)
        for number, category in enumerate(self.categories_list, start=1):
            temp = ElevatedButton(
                content=Container(
                    Row(
                        [
                            Text(f"{number}. ", size=16),
                            Text(category, size=16),
                        ]
                    ),
                    width=250,
                    height=70,
                ),
                on_click=self.open_category,
            )
            self.containers.controls.append(temp)

    def build(self):
        return self.containers

    def open_category(self, e):
        text_constants.selected_category = e.control.content.content.controls[1].value
        self.page.go("/category")
