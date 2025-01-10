import os
import subprocess
import requests
import flet as ft
import time
from typing import Optional, Dict, Any

def create_github_repository(repo_name: str, token: str) -> Optional[str]:
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    payload = {
        "name": repo_name,
        "private": False,
    }
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        return response.json()["html_url"]
    return None

def get_github_repository_data(repo_name: str, token: str) -> Optional[Dict[str, Any]]:
    url = f"https://api.github.com/repos/{repo_name}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    return None

def ensure_git_repository(file_path: str, repo_name: str, github_token: str) -> tuple[bool, str, Optional[Dict[str, Any]]]:
    try:
        repo_dir = os.path.dirname(file_path)
        os.chdir(repo_dir)

        if not os.path.exists(os.path.join(repo_dir, ".git")):
            subprocess.run(["git", "init"], check=True)

        # Create unique repository name
        unique_repo_name = f"{repo_name}_{int(time.time())}"
        
        remote_url = create_github_repository(unique_repo_name, github_token)
        if not remote_url:
            return False, "Failed to create GitHub repository", None

        # Handle existing remote
        result = subprocess.run(["git", "remote", "get-url", "origin"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            subprocess.run(["git", "remote", "set-url", "origin", remote_url], check=True)
        else:
            subprocess.run(["git", "remote", "add", "origin", remote_url], check=True)
        
        file_name = os.path.basename(file_path)
        subprocess.run(["git", "add", file_name], check=True)
        subprocess.run(["git", "commit", "-m", f"Add {file_name}"], check=True)
        subprocess.run(["git", "push", "-u", "origin", "master"], check=True)
        
        # Get repository data
        repo_data = get_github_repository_data(unique_repo_name, github_token)
        return True, remote_url, repo_data

    except subprocess.CalledProcessError as e:
        return False, f"Git operation failed: {str(e)}", None
    except Exception as e:
        return False, f"An error occurred: {str(e)}", None

def main(page: ft.Page):
    page.title = "GitHub File Uploader"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 800
    page.window_height = 600
    
    github_token = "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"

    # Components
    progress_ring = ft.ProgressRing(visible=False)
    status_text = ft.Text(size=16)
    file_path_text = ft.Text(
        size=14,
        color=ft.colors.GREY_700,
        overflow=ft.TextOverflow.ELLIPSIS,
        max_lines=1
    )
    
    # Repository info card (initially hidden)
    repo_info_card = ft.Card(
        visible=False,
        content=ft.Container(
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text("Repository Information", size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Column(spacing=10, controls=[
                        ft.Text("", weight=ft.FontWeight.BOLD, size=16),  # Repository name
                        ft.Text(""),  # Description
                        ft.Text(""),  # Owner
                        ft.Text(""),  # Created at
                        ft.Text(""),  # Clone URL
                    ])
                ],
                spacing=10,
            )
        )
    )
    
    def show_snackbar(message: str, color: str = "error"):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=color,
        )
        page.snack_bar.open = True
        page.update()

    def set_status(message: str, is_error: bool = False):
        status_text.value = message
        status_text.color = ft.colors.RED_600 if is_error else ft.colors.GREEN_600
        status_text.update()

    def update_repo_info(repo_data: Dict[str, Any]):
        info_column = repo_info_card.content.content.controls[2]
        info_column.controls[0].value = f"Repository: {repo_data['name']}"
        info_column.controls[1].value = f"Description: {repo_data['description'] or 'No description'}"
        info_column.controls[2].value = f"Owner: {repo_data['owner']['login']}"
        info_column.controls[3].value = f"Created at: {repo_data['created_at']}"
        info_column.controls[4].value = f"Clone URL: {repo_data['clone_url']}"
        repo_info_card.visible = True
        repo_info_card.update()

    def on_file_selected(e: ft.FilePickerResultEvent):
        if not e.files:
            show_snackbar("No file selected")
            return

        file_path = e.files[0].path
        file_name = os.path.basename(file_path)
        repo_name = os.path.splitext(file_name)[0]
        
        # Update UI to show selected file
        file_path_text.value = f"Selected file: {file_name}"
        file_path_text.update()
        
        # Show progress indicator
        progress_ring.visible = True
        progress_ring.update()
        
        # Process the file
        success, result, repo_data = ensure_git_repository(file_path, repo_name, github_token)
        
        # Hide progress indicator
        progress_ring.visible = False
        progress_ring.update()
        
        if success:
            set_status("✓ File successfully uploaded to GitHub!")
            show_snackbar(
                "Repository created successfully!",
                color=ft.colors.GREEN_600
            )
            # Update repository information
            if repo_data:
                update_repo_info(repo_data)
            # Add link to repository
            page.add(
                ft.TextButton(
                    text="Open repository",
                    url=result,
                    tooltip="Click to open repository in browser",
                    icon=ft.icons.OPEN_IN_NEW
                )
            )
        else:
            set_status(f"✗ {result}", is_error=True)
            show_snackbar(result)

    file_picker = ft.FilePicker(on_result=on_file_selected)
    page.overlay.append(file_picker)

    # Main content
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "GitHub File Uploader",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLUE_900
                    ),
                    ft.Text(
                        "Select a file to create a GitHub repository and upload it automatically.",
                        size=16,
                        color=ft.colors.GREY_700
                    ),
                    ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                "Select File",
                                icon=ft.icons.UPLOAD_FILE,
                                on_click=lambda _: file_picker.pick_files(),
                                style=ft.ButtonStyle(
                                    color=ft.colors.WHITE,
                                    bgcolor=ft.colors.BLUE_600,
                                )
                            ),
                            progress_ring,
                        ],
                        alignment=ft.MainAxisAlignment.START
                    ),
                    file_path_text,
                    status_text,
                    repo_info_card,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=20,
            ),
            padding=ft.padding.all(20),
            border_radius=10,
            bgcolor=ft.colors.WHITE,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.with_opacity(0.2, ft.colors.GREY_800),
            )
        )
    )

if __name__ == "__main__":
    ft.app(target=main)