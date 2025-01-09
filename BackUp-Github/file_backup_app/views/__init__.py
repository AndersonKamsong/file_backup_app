import flet as ft
from views.login import signin_page
from views.register import register_page

# from home import home_page

def main(page: ft.Page):
    page.title = "File Backup App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    signin_page(page)
    # register_page(page)
    page.update()
   

    # # Add a container to wrap the entire page with a gradient background
    # gradient_background = ft.Container(
    #     content=None,  # Content will be added later
    #     gradient=ft.LinearGradient(
    #         begin=ft.alignment.Alignment(0.5, -1),  # Top center
    #         end=ft.alignment.Alignment(0.5, 1),    # Bottom center
    #         colors=["#6A0DAD", "#FFFFFF"],         # Purple to White gradient
    #     ),
    #     expand=True,
    # )

    # # Place both views in a stack, wrapped inside a container
    # container_content = ft.Container(
    #     # content=ft.Stack([login_view, registration_view]),
    #     alignment=ft.alignment.center,
    #     padding=20,
    #     border_radius=ft.border_radius.all(15),
    #     bgcolor=ft.Colors.TRANSPARENT,  # Keep transparency to preserve gradient
    #     # expand=False,
    #     width=400,
    #     height= 600,
    # )

    # # Set the gradient container's content
    # gradient_background.content = container_content

    # Add the gradient background to the page
    # page.add(gradient_background)
   

