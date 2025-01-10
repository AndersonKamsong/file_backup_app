import os
import base64
import requests

class GitHubController:
    def __init__(self, access_token):
        """
        Initialize the GitHubController with the user's personal access token.

        :param access_token: Personal access token for GitHub API authentication
        """
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github.v3+json",
        }

    def create_repository(self, repo_name, private=True):
        """
        Create a new GitHub repository.

        :param repo_name: Name of the repository to create
        :param private: Boolean to set the repository as private or public
        :return: Response JSON or error message
        """
        url = f"{self.base_url}/user/repos"
        payload = {
            "name": repo_name,
            "private": private
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()
    
    def download_branch(self, repo_name, branch, restore_folder):
        """
        Download the entire contents of a specific branch to a given folder in the project directory.

        :param repo_name: Name of the repository
        :param branch: Name of the branch to download
        :param restore_folder: The local folder where the branch contents should be restored
        :return: Response message indicating success or failure
        """
        print("loging")
        owner = self._get_authenticated_user()
        if not owner:
            return {"error": "Authentication failed. Cannot determine user."}

        # Create the restore folder if it doesn't exist
        print("login")
        restore_path = restore_folder
        if not os.path.exists(restore_path):
            os.makedirs(restore_path)
        print("login ok")
        
        # Start downloading the branch contents
        self._download_directory_contents(owner, repo_name, branch, "", restore_path)

        return {"message": f"Branch '{branch}' downloaded successfully to '{restore_path}'."}

    def _download_directory_contents(self, owner, repo_name, branch, path, local_path):
        """
        Download the contents of a directory from the GitHub repository recursively.

        :param owner: GitHub owner (username or organization)
        :param repo_name: Name of the repository
        :param branch: Branch name
        :param path: Path to the current directory in the repository
        :param local_path: Path to the local folder to store files
        """
        print("here")
        url = f"{self.base_url}/repos/{owner}/{repo_name}/contents/{path}?ref={branch}"
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            print(f"Error: {response.json()}")
            return

        contents = response.json()

        # Iterate over the contents (files and subdirectories)
        for item in contents:
            file_path = item["path"]
            local_file_path = os.path.join(local_path, item["name"])

            if item["type"] == "file":
                # It's a file, download it
                self._download_file(owner, repo_name, file_path, local_file_path)
            elif item["type"] == "dir":
                # It's a directory, recurse into it
                if not os.path.exists(local_file_path):
                    os.makedirs(local_file_path)
                self._download_directory_contents(owner, repo_name, branch, file_path, local_file_path)

    def _download_file(self, owner, repo_name, file_path, local_file_path):
        """
        Download a single file from the repository and save it locally.

        :param owner: GitHub owner (username or organization)
        :param repo_name: Name of the repository
        :param file_path: Path of the file in the repository
        :param local_file_path: Local path to save the file
        """
        url = f"{self.base_url}/repos/{owner}/{repo_name}/contents/{file_path}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            file_data = response.json()
            content = base64.b64decode(file_data["content"])

            # Write the file to the local directory
            with open(local_file_path, "wb") as f:
                f.write(content)
        else:
            print(f"Error downloading {file_path}: {response.json()}")

    def create_branch(self, repo_name, folder_path):
        """
        Create a new branch in the repository based on the folder name.

        :param repo_name: Name of the repository
        :param folder_path: Path to the folder; its name will be used as the branch name
        :return: Response JSON or error message
        """
        owner = self._get_authenticated_user()
        if not owner:
            return {"error": "Authentication failed. Cannot determine user."}

        folder_name = os.path.basename(folder_path.rstrip("/"))
        branch_name = folder_name

        # Get the default branch's latest commit SHA
        url = f"{self.base_url}/repos/{owner}/{repo_name}/git/refs/heads/main"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            return response.json()

        default_branch_sha = response.json()["object"]["sha"]

        # Create a new branch
        url = f"{self.base_url}/repos/{owner}/{repo_name}/git/refs"
        payload = {
            "ref": f"refs/heads/{branch_name}",
            "sha": default_branch_sha
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return {'branch_info':response.json(),'branch_name':branch_name}

    def delete_branch(self, repo_name, branch):
        """
        Delete a specific branch in the given repository.

        :param repo_name: Name of the repository
        :param branch: Name of the branch to delete
        :return: Response JSON or error message
        """
        owner = self._get_authenticated_user()
        if not owner:
            return {"error": "Authentication failed. Cannot determine user."}

        # URL for deleting the branch
        url = f"{self.base_url}/repos/{owner}/{repo_name}/git/refs/heads/{branch}"

        # Send DELETE request
        response = requests.delete(url, headers=self.headers)

        if response.status_code == 204:
            return {"success": f"Branch '{branch}' deleted successfully from repository '{repo_name}'."}
        else:
            return {"error": f"Failed to delete branch '{branch}'. Error: {response.json()}"}

    def add_folder_to_branch(self, repo_name, folder_path, branch):
        """
        Add all files and subfolders in a folder to a specific branch in the repository.

        If a file already exists in the branch and has been modified, it will be updated.

        :param repo_name: Name of the repository
        :param folder_path: Path to the folder whose files should be added
        :param branch: Target branch to add or update the files
        :return: Response JSON or error message
        """
        owner = self._get_authenticated_user()
        if not owner:
            return {"error": "Authentication failed. Cannot determine user."}

        results = []

        # Walk through all files and subfolders in the given folder_path
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, folder_path)

                # Construct the API URL for the file
                url = f"{self.base_url}/repos/{owner}/{repo_name}/contents/{relative_path}"

                # Check if the file exists in the repository
                response = requests.get(url, headers=self.headers, params={"ref": branch})
                existing_file = response.json()

                # Read the file content
                with open(file_path, "rb") as f:
                    content = base64.b64encode(f.read()).decode("utf-8")

                # Prepare the payload
                payload = {
                    "message": f"Update {relative_path} from {folder_path}",
                    "content": content,
                    "branch": branch,
                }

                # If the file exists, include the 'sha' to update it
                if response.status_code == 200 and "sha" in existing_file:
                    payload["sha"] = existing_file["sha"]

                # Upload or update the file
                response = requests.put(url, json=payload, headers=self.headers)
                results.append(response.json())

        return results

    def upload_file(self, repo_name, file_path, branch="main"):
        """
        Upload a file to a GitHub repository. Handles files larger than 100MB by splitting them.

        :param repo_name: Name of the repository
        :param file_path: Path to the file to upload
        :param branch: Target branch (default is 'main')
        :return: Response JSON or error message
        """
        owner = self._get_authenticated_user()
        if not owner:
            return {"error": "Authentication failed. Cannot determine user."}

        if os.path.getsize(file_path) > 100 * 1024 * 1024:
            return self._upload_large_file(repo_name, file_path, branch)

        url = f"{self.base_url}/repos/{owner}/{repo_name}/contents/{os.path.basename(file_path)}"
        with open(file_path, "rb") as file:
            content = base64.b64encode(file.read()).decode("utf-8")
        payload = {
            "message": f"Add {os.path.basename(file_path)}",
            "content": content,
            "branch": branch,
        }
        response = requests.put(url, json=payload, headers=self.headers)
        return response.json()

    def _upload_large_file(self, repo_name, file_path, branch):
        """
        Handle the upload of large files by splitting them into smaller chunks.

        :param repo_name: Name of the repository
        :param file_path: Path to the file to upload
        :param branch: Target branch
        :return: Response JSON or error message
        """
        return {"error": "Large file upload is not yet implemented."}

    def list_commits(self, repo_name, branch="main"):
        """
        List all commits in a specific branch of a repository.

        :param repo_name: Name of the repository
        :param branch: Branch to list commits from (default is 'main')
        :return: Response JSON or error message
        """
        owner = self._get_authenticated_user()
        if not owner:
            return {"error": "Authentication failed. Cannot determine user."}

        url = f"{self.base_url}/repos/{owner}/{repo_name}/commits?sha={branch}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def authenticate(self):
        """
        Test authentication and retrieve user details.

        :return: Response JSON or error message
        """
        url = f"{self.base_url}/user"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def _get_authenticated_user(self):
        """
        Retrieve the authenticated user's username.

        :return: Username of the authenticated user or None if authentication fails.
        """
        user_data = self.authenticate()
        if "login" in user_data:
            return user_data["login"]
        return None

# Example usage:
# Replace "your_personal_access_token" with an actual GitHub personal access token
# controller = GitHubController("your_personal_access_token")
# print(controller.authenticate())
# print(controller.create_repository("backup-repo"))
# print(controller.upload_file("backup-repo", "path/to/your/file.txt"))
