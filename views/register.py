import flet as ft
# from views.login import signin_page
import views
from backend.controllers.userController import * 
# Registration View
def show_login(page):
    page.clean()
    views.login.signin_page(page)
    page.update()
     
register_name = ft.TextField(label="USername", width=300)
register_email = ft.TextField(label="Email", width=300)
register_password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
register_confirm_password = ft.TextField(label="Confirm Password", password=True, can_reveal_password=True, width=300)
register_msg = ft.Text("",size=14, weight=ft.FontWeight.BOLD, color="black")
   
def register(page):
    register_msg.value = ""
    page.update()
    if register_password.value != register_confirm_password.value:
        register_msg.value = "Password donot match!"
        register_msg.color = "red"
    else:
        result = register_user(username=register_name.value, email=register_email.value, password=register_password.value)
        print(result)
        if "error" in result:
            register_msg.value = result['error']
            register_msg.color = "red"
        else:
            register_msg.value = result['message']
            register_msg.color = "green"
    page.update()


def register_page(page):
    page.add(
        ft.Column(
            [
                ft.Text("Login", size=24, weight=ft.FontWeight.BOLD, color="black"),
                register_msg,
                register_name,
                register_email,
                register_password,
                register_confirm_password,
                ft.ElevatedButton("Register", on_click=lambda e:register(page), width=300),
                ft.TextButton("Already have an account? Login",on_click=lambda e: show_login(page)),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            visible=True,
        )
    )