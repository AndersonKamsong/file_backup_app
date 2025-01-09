import flet as ft

def main(page: ft.Page):
    page.title = "Calculator"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    display = ft.TextField(
        label="?",
        width=300,
        text_align=ft.TextAlign.RIGHT,
        read_only=True,
        border_color=ft.colors.BLACK, 
    )

    def update_display(value):
        display.value += str(value)
        display.update()

    def calculate_result(e):
        try:
            result = eval(display.value) 
            display.value = str(result)
            display.update()
        except Exception:
            display.value = "Error"
            display.update()

    def clear_display(e):
        display.value = ""
        display.update()

    buttons = [
        ft.Row([
            ft.ElevatedButton("7", on_click=lambda e: update_display(7)),
            ft.ElevatedButton("8", on_click=lambda e: update_display(8)),
            ft.ElevatedButton("9", on_click=lambda e: update_display(9)),
            ft.ElevatedButton("/", on_click=lambda e: update_display("/")),
        ]),
        ft.Row([
            ft.ElevatedButton("4", on_click=lambda e: update_display(4)),
            ft.ElevatedButton("5", on_click=lambda e: update_display(5)),
            ft.ElevatedButton("6", on_click=lambda e: update_display(6)),
            ft.ElevatedButton("*", on_click=lambda e: update_display("*")),
        ]),
        ft.Row([
            ft.ElevatedButton("1", on_click=lambda e: update_display(1)),
            ft.ElevatedButton("2", on_click=lambda e: update_display(2)),
            ft.ElevatedButton("3", on_click=lambda e: update_display(3)),
            ft.ElevatedButton("-", on_click=lambda e: update_display("-")),
        ]),
        ft.Row([
            ft.ElevatedButton("0", on_click=lambda e: update_display(0)),
            ft.ElevatedButton("C", on_click=clear_display),
            ft.ElevatedButton("=", on_click=calculate_result),
            ft.ElevatedButton("+", on_click=lambda e: update_display("+")),
        ]),
    ]

    page.add(display)
    for row in buttons:
        page.add(row)

ft.app(target=main)