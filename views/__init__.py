import flet as ft
from backend.models.Users import User

def main(page: ft.Page):
    page.title = "File Backup App"
    page.padding = 20
    page.scroll = "adaptive"
    user = User()
    # Input field
    input_field = ft.TextField(value="HELLO WORLD", width=500, text_align="center", read_only=True)
   
    # Add components to the page
    page.add(
        ft.Column(
            [
                input_field,
            ],
            alignment="center"
        )
    )
