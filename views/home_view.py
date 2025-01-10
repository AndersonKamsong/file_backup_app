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
    folder_path = "/home/anderson/Desktop/python/file_backup_app/storage3"
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
        time.sleep(1)
        page.clean()
        home_page(page,user)
        page.update()
        
def restore_branch_fun(page,user,branch_name,):
    folder_path = "/home/anderson/Desktop/python/file_backup_app/storage_restore2"
    result = restore_branch(user,branch_name,folder_path)
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

def delete_branch_fun(page,user,branch_name):
    add_folder_msg.value = ""
    page.update()
    result_backup = delete_branch(user,branch_name)
    if "error" in result_backup:
        add_folder_msg.value = result_backup['error']
        add_folder_msg.color = "red"
        page.update()
    else:
        add_folder_msg.value = result_backup['message']
        add_folder_msg.color = "green"
        page.update()
        time.sleep(1)
        page.clean()
        home_page(page,user)
        page.update()
        
        
def get_branch_list(user_id):
    result =  get_user_branch(user_id)
    print(result)
    if "error" in result:
        return []
    else:
        return result['branch_found']
    
def on_button_click(name,branch_name):
    print(f"{name} {branch_name}")
def home_page(page,user):
    user_branch = get_branch_list(user[0][0])
    grid = ft.Column(
        controls=[
            ft.Column(
                controls=[
                    ft.Text(f"Branch Name: {row[2]}", size=16, weight=ft.FontWeight.BOLD, color="black"),
                    ft.Text(f"Folder Path: {row[3]}", size=14, weight=ft.FontWeight.BOLD, color="black"),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(text="Backup",on_click=lambda e, branch=row[2]: start_backup_to_branch(page,user,branch),width=70,height=70),
                            ft.ElevatedButton(text="Restore",on_click=lambda e, branch=row[2]: restore_branch_fun(page,user,branch),width=70,height=70),
                            ft.ElevatedButton(text="Delete",on_click=lambda e, branch=row[2]: delete_branch_fun(page,user,branch),width=70,height=70)
                        ],
                        alignment="spaceEvenly"
                    )
                ]
            )
            for row in user_branch
        ]
    )
    
    page.add(
        ft.Column([
            ft.Text(f"Welcome {user[0][1]} ", size=24),
            add_folder_msg,
            ft.ElevatedButton("Add Folder", on_click=lambda e: add_folder(page, user)),
            ft.ElevatedButton("Logout", on_click=lambda e: show_login(page)),
            ft.ListView(  # This makes the column scrollable
                controls=[
                    grid
                ],
                expand=1,  # Allow the ListView to take up available space
                # scroll=ft.ScrollMode.AUTO  # Enable scrolling when content exceeds the screen height
            )
        ], expand=1)  # Allow the column to expand and fill available space
    )

