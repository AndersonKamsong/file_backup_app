import flet as ft
from flet import TextField, Checkbox, ElevatedButton, Text, Row, Column
from flet_core.control_event import ControlEvent


def main(page: ft.Page) -> None:
    page.title = 'Sinup'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 500
    page.window_height = 600
    page.window_resizable = False


    #setting our fields
    text_username: TextField = TextField(label='Username', text_align=ft.TextAlign.LEFT, width=300)