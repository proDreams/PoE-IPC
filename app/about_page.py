from flet import (UserControl,
                  Text,
                  Column,
                  Divider,
                  CrossAxisAlignment,
                  Row,
                  TextSpan,
                  TextDecoration,
                  TextStyle,
                  colors)

from app import text_constants


class About(UserControl):
    def __init__(self):
        super().__init__()
        self.label = Text(text_constants.about_text[text_constants.current_lang]["label"],
                          size=18,
                          weight="bold")
        self.description = Text(text_constants.about_text[text_constants.current_lang]["description"],
                                size=16)

        self.version_label = Text(text_constants.about_text[text_constants.current_lang]["version"],
                                  width=250)
        self.version_content = Text(text_constants.version)
        self.version_row = Row(
            [
                self.version_label,
                self.version_content,
            ],
        )

        self.author_label = Text(text_constants.about_text[text_constants.current_lang]["author"],
                                 width=250)
        self.author_content = Text(text_constants.about_text[text_constants.current_lang]["author_name"])
        self.author_row = Row(
            [
                self.author_label,
                self.author_content,
            ],
        )

        self.github_label = Text(text_constants.about_text[text_constants.current_lang]["github"],
                                 width=250)
        self.github_content = Text(
            spans=[
                TextSpan(
                    "https://github.com/proDreams/PoETRY",
                    TextStyle(decoration=TextDecoration.UNDERLINE),
                    url="https://github.com/proDreams/PoETRY",
                    on_enter=self.highlight_link,
                    on_exit=self.unhighlight_link,
                ),
            ],
        )
        self.github_row = Row(
            [
                self.github_label,
                self.github_content,
            ]
        )

    def build(self):
        self.expand = True
        return Column(
            [self.label,
             self.description,
             Divider(),
             self.version_row,
             self.author_row,
             Divider(),
             self.github_row
             ],
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )

    @staticmethod
    def highlight_link(e):
        e.control.style.color = colors.BLUE
        e.control.update()

    @staticmethod
    def unhighlight_link(e):
        e.control.style.color = None
        e.control.update()
