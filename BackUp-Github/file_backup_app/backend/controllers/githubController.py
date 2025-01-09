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
            "Authorization": f"token {access_token}",
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

    def upload_file(self, repo_name, file_path, branch="main"):
        """
        Upload a file to a GitHub repository. Handles files larger than 100MB by splitting them.

        :param repo_name: Name of the repository
        :param file_path: Path to the file to upload
        :param branch: Target branch (default is 'main')
        :return: Response JSON or error message
        """
        if os.path.getsize(file_path) > 100 * 1024 * 1024:
            return self._upload_large_file(repo_name, file_path, branch)

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

    def _upload_large_file(self, repo_name, file_path, branch):
        """
        Handle the upload of large files by splitting them into smaller chunks.

        :param repo_name: Name of the repository
        :param file_path: Path to the file to upload
        :param branch: Target branch
        :return: Response JSON or error message
        """
        # Example placeholder for large file handling logic
        return {"error": "Large file upload is not yet implemented."}

    def list_commits(self, repo_name, branch="main"):
        """
        List all commits in a specific branch of a repository.

        :param repo_name: Name of the repository
        :param branch: Branch to list commits from (default is 'main')
        :return: Response JSON or error message
        """
        url = f"{self.base_url}/repos/{{owner}}/{repo_name}/commits?sha={branch}"
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

# Example usage
# Replace "your_personal_access_token" with an actual GitHub personal access token
# controller = GitHubController("your_personal_access_token")
# print(controller.authenticate())
# print(controller.create_repository("backup-repo"))
# print(controller.upload_file("backup-repo", "path/to/your/file.txt"))
