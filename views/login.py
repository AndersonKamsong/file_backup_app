import flet as ft
from views.register import register_page

 # Navigation function to switch between login and registration
def show_registration(page):
    page.clean()
    register_page(page)
    page.update()

login_msg = ft.Text("",size=14, weight=ft.FontWeight.BOLD, color="black")

def login(page):
    # Add your login logic here
    print(f"Logging in with email: {login_email.value} and password: {login_password.value}")
    page.snack_bar = ft.SnackBar(ft.Text("Login successful!"))
    login_msg.value = "Login successful!"
    login_msg.color = "red"
    # page.snack_bar.open()
    page.update()

login_email = ft.TextField(label="Email", width=300)
login_password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)

def signin_page(page):
    page.add(
        ft.Column(
            [
                ft.Text("Login", size=24, weight=ft.FontWeight.BOLD, color="black"),
                login_msg,
                login_email,
                login_password,
                ft.ElevatedButton("Login", on_click=lambda e: login(page), width=300),
                ft.TextButton("Don't have an account? Register",on_click=lambda e: show_registration(page)),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            visible=True,
        )
    )
