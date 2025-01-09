import flet as ft
import views

def show_login(page):
    page.clean()
    views.login.signin_page(page)
    page.update()
    
def home_page(page,user):
    page.add(
        ft.Column([
            ft.Text(f"Welcome {user[0][1]} ", size=24),
            ft.ElevatedButton("Logout", on_click=lambda e: show_login(page))
        ])
    )
