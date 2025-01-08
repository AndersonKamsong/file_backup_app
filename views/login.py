import flet as ft
from views.register import registration_view

 # Navigation function to switch between login and registration
def show_registration(e):
    login_view.visible = False
    registration_view.visible = True
    # page.update()

login_email = ft.TextField(label="Email", width=300)
login_password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)

def login(e):
    # Add your login logic here
    print(f"Logging in with email: {login_email.value} and password: {login_password.value}")
    # page.snack_bar = ft.SnackBar(ft.Text("Login successful!"))
    # page.snack_bar.open()
    # page.update()

login_view = ft.Column(
    [
        ft.Text("Login", size=24, weight=ft.FontWeight.BOLD, color="white"),
        login_email,
        login_password,
        ft.ElevatedButton("Login", on_click=login, width=300),
        ft.TextButton("Don't have an account? Register", on_click=show_registration),
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    visible=True,
)
