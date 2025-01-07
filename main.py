import flet as ft
from flet import FilePicker, TextField, Column, ElevatedButton, ListView, Text, Checkbox, Row

def main(page: ft.Page):
    page.title = "File Backup Application"
    page.vertical_alignment = "center"
    page.padding = 20

    # Global variables to hold user data and state
    authenticated_user = {"username": None}
    selected_folder = None
    repositories = []

    # Authentication function
    def authenticate_user(e):
        # Placeholder for GitHub OAuth2 authentication logic
        username = username_field.value
        if username:
            authenticated_user["username"] = username
            status_text.value = f"Authenticated as {username}"
            repositories_view.controls.clear()
            repositories_view.controls.append(
                ft.Text(f"Repositories for {username} will appear here.")
            )
            page.update()
        else:
            status_text.value = "Authentication failed. Please try again."
            page.update()

    # Folder selection callback
    def on_folder_selected(e):
        nonlocal selected_folder
        if folder_picker.result:
            selected_folder = folder_picker.result.path
            selected_folder_text.value = f"Selected folder: {selected_folder}"
        page.update()

    # Add folder for backup
    def add_folder(e):
        if selected_folder:
            repository_name = repo_name_field.value or selected_folder.split("/")[-1]
            repositories.append({"folder": selected_folder, "repository": repository_name})
            repositories_view.controls.append(ft.Text(f"{repository_name} - {selected_folder}"))
            selected_folder_text.value = "Folder added for backup."
        else:
            selected_folder_text.value = "No folder selected."
        page.update()

    # Upload files (placeholder for actual upload logic)
    def upload_files(e):
        if not authenticated_user["username"]:
            upload_status.value = "Please authenticate first."
        elif not repositories:
            upload_status.value = "No folders added for backup."
        else:
            upload_status.value = "Uploading files to GitHub repositories..."
            # Add your upload logic here
            # Example: push files from each folder to the respective repository
            upload_status.value = "Upload completed successfully!"
        page.update()

    # UI components
    username_field = TextField(label="GitHub Username", width=300)
    authenticate_button = ElevatedButton("Authenticate", on_click=authenticate_user)
    status_text = Text("Not authenticated.")

    folder_picker = FilePicker(on_result=on_folder_selected)
    page.overlay.append(folder_picker)
    select_folder_button = ElevatedButton("Select Folder", on_click=lambda _: folder_picker.get_directory_path())
    selected_folder_text = Text("No folder selected.")

    repo_name_field = TextField(label="Repository Name (optional)", width=300)
    add_folder_button = ElevatedButton("Add Folder for Backup", on_click=add_folder)
    repositories_view = ListView(expand=True)

    upload_button = ElevatedButton("Upload Files", on_click=upload_files)
    upload_status = Text("")

    # Layout
    page.add(
        Column([
            Text("File Backup Application", size=24, weight="bold"),
            Row([username_field, authenticate_button]),
            status_text,
            Row([select_folder_button, selected_folder_text]),
            Row([repo_name_field, add_folder_button]),
            Text("Repositories and Folders:"),
            repositories_view,
            upload_button,
            upload_status
        ])
    )

# Run the app
ft.app(target=main)
