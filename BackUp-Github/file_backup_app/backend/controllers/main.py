import os
import githubController

# Testing controllers
def main():
    # Replace "your_personal_access_token" with an actual GitHub personal access token
    access_token = os.getenv("GITHUB_TOKEN")
    controller = githubController.GitHubController(access_token)

    # Test authentication
    print("Authenticating with GitHub...")
    auth_response = controller.authenticate()
    print(auth_response)

    # Create a new repository
    print("Creating a new repository...")
    repo_response = controller.create_repository("test-backup-repo", private=True)
    print(repo_response)

    # Upload a file to the repository
    print("Uploading a file to the repository...")
    file_path = r"../../../Composer-Setup.exe"  # Replace with the path to your test file
    upload_response = controller.upload_file("test-backup-repo", file_path)
    print(upload_response)

if __name__ == "__main__":
    main()
