import os
import base64
import zipfile
import requests
from datetime import datetime


class GitHubController:
    def __init__(self, access_token):
        """
        Initialize the GitHubController with the user's personal access token.

        :param access_token: Personal access token for GitHub API authentication
        """
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github.v3+json",
        }
        self.owner = self.get_authenticated_user()  # Set the owner to the authenticated user

    def get_authenticated_user(self):
        # Send a request to GitHub API to get the authenticated user's information
        response = requests.get('https://api.github.com/user', headers=self.headers)
        if response.status_code == 200:
            return response.json().get('login')  # 'login' is the username
        else:
            print(f"Error getting authenticated user: {response.status_code}")
            return None

    def create_repository(self, repo_name, private=True):
        """
        Create a new GitHub repository.

        :param repo_name: Name of the repository to create
        :param private: Boolean to set the repository as private or public
        :return: Response JSON or error message
        """
        url = f"{self.base_url}/user/repos"
        payload = {"name": repo_name, "private": private}
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

    def upload_file(self, repo_name, file_path, branch="main"):
        """
        Upload a file to a GitHub repository.

        :param repo_name: Name of the repository
        :param file_path: Path to the file to upload
        :param branch: Target branch (default is 'main')
        :return: Response JSON or error message
        """
        url = f"{self.base_url}/repos/{{owner}}/{repo_name}/contents/{os.path.basename(file_path)}"
        with open(file_path, "rb") as file:
            content = base64.b64encode(file.read()).decode("utf-8")
        payload = {
            "message": f"Add {os.path.basename(file_path)}",
            "content": content,
            "branch": branch,
        }
        response = requests.put(url, json=payload, headers=self.headers)
        return response.json()

    def backup_folder(self, folder_path, repo_name):
        import zipfile
        import os

        # Log repository name and folder path
        print(f"Backing up to repository: {repo_name}")
        print(f"Folder path: {folder_path}")

        # Create a zip file of the folder
        zip_file_name = os.path.basename(folder_path) + "_backup.zip"
        zip_file_path = os.path.join(os.path.dirname(folder_path), zip_file_name)
        try:
            with zipfile.ZipFile(zip_file_path, "w") as zipf:
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        relative_path = os.path.relpath(full_path, folder_path)
                        zipf.write(full_path, arcname=relative_path)
        except PermissionError as e:
            print(f"Error creating zip file: {e}")
            return {"message": "Failed to create zip file", "error": str(e)}

        # Log zip file details
        print(f"Created zip file: {zip_file_path}")

        # Upload the zip file to GitHub
        with open(zip_file_path, "rb") as file_content:
            content = file_content.read()
            encoded_content = base64.b64encode(content).decode()

        api_url = f"https://api.github.com/repos/{self.owner}/{repo_name}/contents/{zip_file_name}"
        response = requests.put(
            api_url,
            headers=self.headers,
            json={"message": "Backup folder", "content": encoded_content},
        )

        # Log API response
        print("GitHub API Response:", response.json())

        return response.json()

        """
        Backup a folder by zipping it and pushing to a GitHub repository.

        :param folder_path: Path of the folder to back up
        :param repo_name: Name of the repository to store the backup
        :param branch: Branch to upload the backup file (default is 'main')
        :return: Status of the backup
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_file_path = f"{folder_path}_{timestamp}.zip"

        # Zip the folder
        with zipfile.ZipFile(zip_file_path, "w") as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, start=folder_path)
                    zipf.write(full_path, arcname)

        # Push the zip file to GitHub
        upload_response = self.upload_file(repo_name, zip_file_path, branch)

        # Clean up the zip file after upload
        os.remove(zip_file_path)

        return upload_response

    def restore_backup(self, repo_name, file_name, output_folder, branch="main"):
        """
        Restore a backup by downloading and extracting a zip file from GitHub.

        :param repo_name: Name of the repository
        :param file_name: Name of the backup zip file
        :param output_folder: Directory to extract the backup
        :param branch: Branch to fetch the backup file from (default is 'main')
        :return: Status of the restoration
        """
        url = f"{self.base_url}/repos/{{owner}}/{repo_name}/contents/{file_name}?ref={branch}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            file_content = base64.b64decode(response.json()["content"])
            zip_file_path = os.path.join(output_folder, file_name)

            # Save the zip file locally
            with open(zip_file_path, "wb") as file:
                file.write(file_content)

            # Extract the zip file
            with zipfile.ZipFile(zip_file_path, "r") as zipf:
                zipf.extractall(output_folder)

            # Clean up the downloaded zip file
            os.remove(zip_file_path)

            return {"status": "success", "message": f"Backup restored to {output_folder}"}
        else:
            return {"status": "failure", "message": response.json().get("message", "Unknown error")}
    
    def authenticate(self):
        """
        Authenticate with GitHub using the provided personal access token.

        :return: Response JSON or error message
        """
        url = f"{self.base_url}/user"
        response = requests.get(url, headers=self.headers)
        return response.json()



