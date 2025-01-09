import flet as ft
# from views.login import signin_page
import views

# Registration View
def show_login(page):
    page.clean()
    views.login.signin_page(page)
    page.update()
     
register_email = ft.TextField(label="Email", width=300)
register_password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
register_confirm_password = ft.TextField(label="Confirm Password", password=True, can_reveal_password=True, width=300)
register_msg = ft.Text("",size=14, weight=ft.FontWeight.BOLD, color="black")
   
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


def register_page(page):
    page.add(
        ft.Column(
            [
                ft.Text("Login", size=24, weight=ft.FontWeight.BOLD, color="black"),
                register_msg,
                register_email,
                register_password,
                register_confirm_password,
                ft.ElevatedButton("Register", on_click=register, width=300),
                ft.TextButton("Already have an account? Login",on_click=lambda e: show_login(page)),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            visible=True,
        )
    )