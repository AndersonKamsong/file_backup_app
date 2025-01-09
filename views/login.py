import flet as ft
from views.register import register_page
from views.home_view import home_page
from backend.controllers.userController import * 
import time
# import views

 # Navigation function to switch between login and registration
def show_registration(page):
    page.clean()
    register_page(page)
    page.update()

def go_to_home(page,user):
    page.clean()
    home_page(page,user)
    page.update()
    
login_msg = ft.Text("",size=14, weight=ft.FontWeight.BOLD, color="black")

def login(page):
    login_msg.value = ""
    page.update()
    # Add your login logic here
    print(f"Logging in with email: {login_email.value} and password: {login_password.value}")
    result = login_user(email=login_email.value,password=login_password.value)
    print(result)
    if "error" in result:
        login_msg.value = result['error']
        login_msg.color = "red"
        page.update()
    else:
        login_msg.value = result['message']
        login_msg.color = "green"
        page.update()
        time.sleep(1)
        go_to_home(page,result['user'])

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
