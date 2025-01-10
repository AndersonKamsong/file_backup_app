import flet as ft
import views
from backend.controllers.homeController import * 
import time

add_folder_msg = ft.Text("",size=14, weight=ft.FontWeight.BOLD, color="black")

def show_login(page):
    page.clean()
    views.login.signin_page(page)
    page.update()

def add_folder(page,user):
    folder_path = "/home/anderson/Desktop/python/file_backup_app/storage2"
    result = create_branch_from_folder(user,folder_path)
    print(result)
    if "error" in result:
        add_folder_msg.value = result['error']
        add_folder_msg.color = "red"
        page.update()
    else:
        add_folder_msg.value = result['message']
        add_folder_msg.color = "green"
        page.update()
        

def start_backup_to_branch(page,user,branch_name):
    add_folder_msg.value = ""
    page.update()
    result_backup = backup_to_branch(user,branch_name)
    time.sleep(1)
    if "error" in result_backup:
        add_folder_msg.value = result_backup['error']
        add_folder_msg.color = "red"
        page.update()
    else:
        add_folder_msg.value = result_backup['message']
        add_folder_msg.color = "green"
        page.update()
        
def home_page(page,user):
    page.add(
        ft.Column([
            ft.Text(f"Welcome {user[0][1]} ", size=24),
            add_folder_msg,
            ft.ElevatedButton("add folder", on_click=lambda e: add_folder(page,user)),
            ft.ElevatedButton("back up", on_click=lambda e: start_backup_to_branch(page,user,"storage")),
            ft.ElevatedButton("Logout", on_click=lambda e: show_login(page))
        ])
    )
