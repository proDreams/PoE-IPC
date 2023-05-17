import flet as ft

from app import text_constants
from app.about_page import About
from app.catefories_page import Categories
from app.items_page import Items
from app.settings_page import Settings, SettingsVersion


def main(page: ft.Page):
    def app_bar(title: str = text_constants.app_bar_text[text_constants.current_lang]["title"]):
        return ft.AppBar(
            title=ft.Text(title),
            center_title=True,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                Settings().selected_content,
                ft.IconButton(ft.icons.INFO, on_click=lambda _: page.go("/about")),
                ft.IconButton(ft.icons.SETTINGS, on_click=lambda _: page.go("/settings")),
            ],
        )

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    app_bar(),
                    ft.Text(text_constants.main_text[text_constants.current_lang]["select_category"],
                            size=18,
                            weight="bold"),
                    Categories(),
                ],
                padding=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        if page.route == "/category":
            page.views.append(
                ft.View(
                    "/category",
                    [
                        app_bar(text_constants.selected_category),
                        Items(),
                    ],
                    padding=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO
                )
            )
        if page.route == "/about":
            page.views.append(
                ft.View(
                    "/about",
                    [
                        app_bar(text_constants.app_bar_text[text_constants.current_lang]["about"]),
                        ft.Row(
                            [
                                ft.Container(
                                    About(),
                                    bgcolor=ft.colors.SURFACE_VARIANT,
                                    height=300,
                                    width=800,
                                    border_radius=10,
                                    padding=30
                                ),
                            ],
                            alignment="center"
                        ),
                    ],
                )
            )
        if page.route == "/settings":
            page.views.append(
                ft.View(
                    "/settings",
                    [
                        app_bar(text_constants.app_bar_text[text_constants.current_lang]["settings"]),
                        ft.Row(
                            [
                                ft.Container(
                                    SettingsVersion(),
                                    bgcolor=ft.colors.SURFACE_VARIANT,
                                    height=300,
                                    width=450,
                                    border_radius=10,
                                    padding=10
                                ),
                                ft.Container(
                                    Settings(),
                                    bgcolor=ft.colors.SURFACE_VARIANT,
                                    height=500,
                                    width=450,
                                    border_radius=10,
                                    padding=10
                                ),
                            ],
                            alignment="center"
                        ),
                    ],
                )
            )
        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.title = "Path of Exile Items Price Converter " + text_constants.version
    page.window_width = 1200
    page.window_height = 650
    # page.window_resizable = False
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
