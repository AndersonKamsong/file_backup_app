import datetime
import githubController

def main():
    access_token = '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'
    if not access_token:
        print("Error: GitHub personal access token is not set.")
        return

    controller = githubController.GitHubController(access_token)

    # Authenticate with GitHub
    print("Authenticating with GitHub...")
    auth_response = controller.authenticate()
    print(auth_response)

    if "login" not in auth_response:
        print("Error: Authentication failed. Check your personal access token.")
        return

    # Create a unique repository name
    repo_name = f"Test-backup-repo-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    print(f"Creating a new repository: {repo_name}...")
    repo_response = controller.create_repository(repo_name, private=True)
    print(repo_response)

    if "id" not in repo_response:
        print(f"Error: Failed to create repository '{repo_name}'. Reason: {repo_response.get('message', 'Unknown error')}")
        return

    # Proceed with backup coordination
    folder_path = r"C:\Users\acer\Desktop\Python\Advanced Python"
    print(f"Backing up the folder: {folder_path}...")
    backup_response = controller.backup_folder(folder_path, repo_name)
    print("Backup response:", backup_response)

if __name__ == "__main__":
    main()
