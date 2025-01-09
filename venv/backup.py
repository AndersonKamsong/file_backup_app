import flet as ft
import os
import requests
import base64

# Replace with your GitHub OAuth credentials
GITHUB_CLIENT_ID = "your_client_id"
GITHUB_CLIENT_SECRET = "your_client_secret"

# Function to get access token (placeholder)
def get_access_token():
    # Implement logic to retrieve and return the access token
    return "your_access_token"

def main(page: ft.Page):
    page.title = "File Backup Application"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Display for input and output
    repo_display = ft.TextField(
        label="Repository Name",
        width=300,
        text_align=ft.TextAlign.LEFT,
    )
    
    file_picker = ft.FilePicker()

    # Function to authenticate with GitHub
    def authenticate(e):
        oauth_url = f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&scope=repo"
        page.launch_url(oauth_url)

    # Function to create a repository
    def create_repository(e):
        repo_name = repo_display.value.strip()
        if repo_name:
            response = requests.post(
                f"https://api.github.com/user/repos",
                json={"name": repo_name},
                headers={"Authorization": f"token {get_access_token()}"}
            )
            if response.status_code == 201:
                page.add(ft.Text(f"Repository '{repo_name}' created successfully!"))
            else:
                page.add(ft.Text("Failed to create repository."))

    # Function to handle file selection
    def file_selected(e):
        if e.files:
            upload_file(e.files[0])

    # Function to upload file
    def upload_file(selected_file):
        file_path = selected_file.path
        
        # Check if the file exists (for safety)
        if not os.path.exists(file_path):
            page.add(ft.Text("File does not exist!"))
            return

        file_size = os.path.getsize(file_path)

        # Split file into chunks if larger than 100MB
        chunk_size = 100 * 1024 * 1024  # 100MB
        with open(file_path, 'rb') as f:
            chunk_number = 0
            while True:
                chunk_data = f.read(chunk_size)
                if not chunk_data:
                    break
                
                chunk_number += 1
                chunk_filename = f"{os.path.basename(file_path)}.part{chunk_number}"
                status_code = upload_chunk_to_github(chunk_filename, chunk_data)

                if status_code != 201:
                    page.add(ft.Text(f"Failed to upload chunk {chunk_number}."))
                    return

        page.add(ft.Text("File uploaded successfully!"))

    def upload_chunk_to_github(filename, data):
        # Encode data in Base64 for GitHub API
        encoded_data = base64.b64encode(data).decode('utf-8')
        
        # Placeholder for your GitHub repository details
        repo_name = repo_display.value.strip()
        
        url = f"https://api.github.com/repos/your_username/{repo_name}/contents/{filename}"
        
        response = requests.put(
            url,
            json={
                "message": f"Upload {filename}",
                "content": encoded_data,
                "branch": "main"  # Specify the branch if needed
            },
            headers={"Authorization": f"token {get_access_token()}"}
        )
        
        return response.status_code

    # Button to authenticate
    auth_button = ft.ElevatedButton("Authenticate with GitHub", on_click=authenticate)
    
    # Button to create repository
    create_button = ft.ElevatedButton("Create Repository", on_click=create_repository)
    
    # Button to select file
    select_file_button = ft.ElevatedButton("Select File", on_click=lambda e: file_picker.pick_files())
    
    # Set up file picker event handler
    file_picker.on_change = file_selected

    # Add components to the page
    page.add(repo_display, auth_button, create_button, select_file_button, file_picker)

# Run the app
ft.app(target=main)