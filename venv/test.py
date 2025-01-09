import flet as ft

def main(page):
    def pick_file(e):
        page.dialog = ft.FilePicker(on_result=upload_file)
        page.dialog.show()

    page.add(ft.ElevatedButton("Pick File", on_click=pick_file))

ft.app(target=main)
import os

def split_file(file_path, chunk_size=100 * 1024 * 1024): # 100 MB
    with open(file_path, 'rb') as f:
        chunk_number = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            with open(f"{file_path}.part{chunk_number}", 'wb') as chunk_file:
                chunk_file.write(chunk)
            chunk_number += 1
import subprocess

def upload_chunk(chunk_path):
    subprocess.run(["git", "add", chunk_path])
    subprocess.run(["git", "commit", "-m", f"Add {chunk_path}"])
    subprocess.run(["git", "push"])
def reassemble_file(original_file_name, number_of_chunks):
    with open(original_file_name, 'wb') as output_file:
        for i in range(number_of_chunks):
            with open(f"{original_file_name}.part{i}", 'rb') as chunk_file:
                output_file.write(chunk_file.read())
