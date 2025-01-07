import os
import shutil
import subprocess
import time
from threading import Thread
import flet as ft

def backup_to_git(backup_dir, tracked_files, output_text):
    if not tracked_files:
        output_text.value += "No files to backup.\n"
        return
    
    print("here1 int")
    # Initialize Git repository if not already
    if not os.path.exists(os.path.join(backup_dir, ".git")):
        subprocess.run(["git", "init"], cwd=backup_dir)
        subprocess.run(["git", "lfs", "install"], cwd=backup_dir)

    # Add and commit files
    for file in tracked_files:
        subprocess.run(["git", "lfs", "track", file], cwd=backup_dir)
        subprocess.run(["git", "add", file], cwd=backup_dir)
    print("here1")
    subprocess.run(["git", "add", "*"], cwd=backup_dir)
    subprocess.run(["git", "commit", "-m", "Automated Backup"], cwd=backup_dir)
    print("here1 push")
    # Push to GitHub
    try:
        subprocess.run(["git", "push", "-u", "origin", "master"], cwd=backup_dir, check=True)
        output_text.value += "Backup completed and pushed to GitHub.\n"
    except subprocess.CalledProcessError:
        output_text.value += "Failed to push to GitHub. Check your remote repository settings.\n"


def main(page: ft.Page):
    page.title = "File Backup Application"
    page.scroll = ft.ScrollMode.AUTO

    backup_dir = "backup_folder"
    os.makedirs(backup_dir, exist_ok=True)
    tracked_files = []

    def add_file(e):
        file_path = file_input.value
        if os.path.exists(file_path) and os.path.isfile(file_path):
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # Size in MB
            # if file_size > 100:
            dest_path = os.path.join(backup_dir, os.path.basename(file_path))
            shutil.copy(file_path, dest_path)
            tracked_files.append(dest_path)
            output_text.value += f"Added: {dest_path} ({file_size:.2f} MB)\n"
            file_input.value = ""
            # else:
            #     output_text.value += f"File {file_path} is smaller than 100MB.\n"
        else:
            output_text.value += f"File {file_path} does not exist.\n"

    def start_backup(e):
        interval = int(backup_interval.value)
        output_text.value += f"Starting backup every {interval} minutes...\n"
        Thread(target=schedule_backup, args=(interval,), daemon=True).start()

    def schedule_backup(interval):
        while True:
            output_text.value += "Backing up files...\n"
            page.update()
            backup_to_git(backup_dir, tracked_files, output_text)
            time.sleep(interval * 60)

    # UI Elements
    file_input = ft.TextField(label="File Path", width=400)
    backup_interval = ft.Slider(min=1, max=60, divisions=59, label="Backup Interval: {value} mins", value=10)
    output_text = ft.Text(value="")

    page.add(
        ft.Row([file_input, ft.ElevatedButton("Add File", on_click=add_file)]),
        backup_interval,
        ft.ElevatedButton("Start Backup", on_click=start_backup),
        ft.Text("Logs:"),
        output_text,
    )

# Run the Flet app
if __name__ == "__main__":
    ft.app(target=main)
