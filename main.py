import flet as ft

def main(page: ft.Page):
    page.title = "Login and Registration"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Add a container to wrap the entire page with a gradient background
    gradient_background = ft.Container(
        content=None,  # Content will be added later
        gradient=ft.LinearGradient(
            begin=ft.alignment.Alignment(0.5, -1),  # Top center
            end=ft.alignment.Alignment(0.5, 1),    # Bottom center
            colors=["#6A0DAD", "#FFFFFF"],         # Purple to White gradient
        ),
        expand=True,
    )

    # Navigation function to switch between login and registration
    def show_registration(e):
        login_view.visible = False
        registration_view.visible = True
        page.update()

    def show_login(e):
        registration_view.visible = False
        login_view.visible = True
        page.update()

    # Login View
    login_email = ft.TextField(label="Email", width=300)
    login_password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)

    def login(e):
        # Add your login logic here
        print(f"Logging in with email: {login_email.value} and password: {login_password.value}")
        page.snack_bar = ft.SnackBar(ft.Text("Login successful!"))
        page.snack_bar.open()
        page.update()

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

    # Registration View
    reg_email = ft.TextField(label="Email", width=300)
    reg_password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
    reg_confirm_password = ft.TextField(label="Confirm Password", password=True, can_reveal_password=True, width=300)

    def register(e):
        if reg_password.value != reg_confirm_password.value:
            page.snack_bar = ft.SnackBar(ft.Text("Passwords do not match!"), bgcolor=ft.colors.RED)
        else:
            # Add your registration logic here
            print(f"Registering with email: {reg_email.value} and password: {reg_password.value}")
            page.snack_bar = ft.SnackBar(ft.Text("Registration successful!"))
        page.snack_bar.open()
        page.update()

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

    # Place both views in a stack, wrapped inside a container
    container_content = ft.Container(
        content=ft.Stack([login_view, registration_view]),
        alignment=ft.alignment.center,
        padding=20,
        border_radius=ft.border_radius.all(15),
        bgcolor=ft.colors.TRANSPARENT,  # Keep transparency to preserve gradient
        # expand=False,
        width=400,
        height= 600,
    )

    # Set the gradient container's content
    gradient_background.content = container_content

    # Add the gradient background to the page
    page.add(gradient_background)

ft.app(target=main)