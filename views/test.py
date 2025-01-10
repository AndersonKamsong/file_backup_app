import flet as ft

# Page 1: Home
def home_page(page):
    page.add(
        ft.Column([
            ft.Text("Welcome to the Home Page", size=24),
            ft.ElevatedButton("Go to Login", on_click=lambda e: go_to_login(page))
        ])
    )

# Page 2: Login
def login_page(page):
    page.add(
        ft.Column([
            ft.Text("Login Page", size=24),
            ft.TextField(label="Email", autofocus=True),
            ft.TextField(label="Password", password=True),
            ft.ElevatedButton("Login", on_click=lambda e: login_action(page))
        ])
    )

# Page 3: Registration
def register_page(page):
    page.add(
        ft.Column([
            ft.Text("Register Page", size=24),
            ft.TextField(label="Username"),
            ft.TextField(label="Email"),
            ft.TextField(label="Password", password=True),
            ft.ElevatedButton("Register", on_click=lambda e: register_action(page))
        ])
    )

# Function to go to the login page
def go_to_login(page):
    page.clean()
    login_page(page)
    page.update()

# Function to go to the home page
def go_to_home(page):
    page.clean()
    home_page(page)
    page.update()

# Function to go to the registration page
def go_to_register(page):
    page.clean()
    register_page(page)
    page.update()

# Actions for Login and Registration (you can expand them)
def login_action(page):
    print("Login successful!")
    go_to_home(page)

def register_action(page):
    print("User registered!")
    go_to_home(page)

# Main function to set up the pages
def main(page):
    # Start with the home page
    home_page(page)
    page.update()

ft.app(target=main)



# login_view = ft.Column(
#     [
#         ft.Text("Login", size=24, weight=ft.FontWeight.BOLD, color="white"),
#         login_email,
#         login_password,
#         ft.ElevatedButton("Login", on_click=login, width=300),
#         ft.TextButton("Don't have an account? Register", on_click=show_registration),
#     ],
#     alignment=ft.MainAxisAlignment.CENTER,
#     visible=True,
# )

# registration_view = ft.Column(
#     [
#         ft.Text("Register", size=24, weight=ft.FontWeight.BOLD, color="white"),
#         reg_email,
#         reg_password,
#         reg_confirm_password,
#         ft.ElevatedButton("Register", on_click=register, width=300),
#         ft.TextButton("Already have an account? Login", on_click=show_login),
#     ],
#     alignment=ft.MainAxisAlignment.CENTER,
#     visible=False,
# )
# login_email = ft.TextField(label="Email", width=300)
# login_password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)

def pick_files(page, user):
    """
    Function to handle file selection and add the selected folder or file.
    """

    def on_files_selected(e):
        if e.files:
            for file in e.files:
                # Process the selected file or folder
                print(f"Selected: {file.path}")  # Example: print the file path
            # Perform additional actions here if needed

    # Check if the FilePicker already exists on the page
    if not hasattr(page, "file_picker"):
        # Create and add FilePicker to the page's overlay
        page.file_picker = ft.FilePicker(on_result=on_files_selected)
        page.overlay.append(page.file_picker)
        page.update()

    # Open the file picker dialog
    page.file_picker.pick_files(allow_multiple=True)  # Allow selecting multiple files


# Main page layout
page.add(
    ft.Column(
        controls=[
            ft.Text(f"Welcome {user[0][1]}", size=24, alignment=ft.TextAlign.CENTER),
            add_folder_msg,
            ft.ElevatedButton("Add Folder", on_click=lambda e: add_folder(page, user)),
            ft.ElevatedButton("Logout", on_click=lambda e: show_login(page)),
            ft.ElevatedButton(
                "Pick Files or Folder",
                on_click=lambda e: pick_files(page, user)
            ),
            ft.ListView(
                controls=[
                    grid
                ],
                expand=1,  # Allow ListView to expand and enable scrolling
            )
        ],
        expand=1  # Allow the column to fill available space
    )
)
