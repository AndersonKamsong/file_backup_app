import flet as ft
from views.login import login_view

# Registration View
reg_email = ft.TextField(label="Email", width=300)
reg_password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
reg_confirm_password = ft.TextField(label="Confirm Password", password=True, can_reveal_password=True, width=300)

def show_login(e):
    registration_view.visible = False
    login_view.visible = True
    # home_page(page)
    # page.update()
        
def register(e):
    if reg_password.value != reg_confirm_password.value:
        pass
        # page.snack_bar = ft.SnackBar(ft.Text("Passwords do not match!"), bgcolor=ft.colors.RED)
    else:
        # Add your registration logic here
        print(f"Registering with email: {reg_email.value} and password: {reg_password.value}")
        # page.snack_bar = ft.SnackBar(ft.Text("Registration successful!"))
    # page.snack_bar.open()
    # page.update()

registration_view = ft.Column(
    [
        ft.Text("Register", size=24, weight=ft.FontWeight.BOLD, color="white"),
        reg_email,
        reg_password,
        reg_confirm_password,
        ft.ElevatedButton("Register", on_click=register, width=300),
        ft.TextButton("Already have an account? Login", on_click=show_login),
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    visible=False,
)
