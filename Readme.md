# File Backup App

This is a Python backup application built using the Flet framework and SQLite database. The app allows users to back up files to a GitHub repository. When a user registers, a GitHub repository is created using their username. Users can select a folder, and a branch is created with the folder name. Branch switching functionality is currently under development.

## Features
- User registration (creates a GitHub repository automatically)
- Select a folder for backup (creates a branch with the folder name) (in development)
- SQLite database for storing user data
- GitHub integration for file backups
- Branch switching (in development)

## Installation
### Prerequisites
Ensure you have the following installed on your system:
- Python (>=3.7)
- Virtual environment (`venv`)

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/AndersonKamsong/file_backup_app
   cd file_backup_app
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory and add the following:
   ```sh
   FILE_BACKUP_TOKEN=<your_github_personal_access_token>
   ```

## Usage
1. Run the application:
   ```sh
   flet app.py --web
   ```
2. Register in the app (this will create a GitHub repository in your name).
3. Select a folder to back up (a branch will be created with the folder name).
4. Future updates will include the ability to switch between branches.

## Directory Structure
```
file_backup_app/
│── app.py                # Main application entry point
│── auth/                 # Authentication module
│── backend/              # Backend logic and database handling
│── backup_folder/        # Folder where local backups are stored
│── .env                  # Environment variables
│── file_backup.db        # SQLite database
│── .git                  # Git repository
│── .gitignore            # Files to ignore in Git
│── Readme.md             # Project documentation
│── requirements.txt      # Dependencies
│── venv/                 # Virtual environment
│── views/                # UI components
```

## Development
- To contribute, ensure you have a GitHub account and a personal access token.
- Future updates will include improved UI/UX with Flet, branch management, and automation.

## License
This project is licensed under the MIT License.

## Contact
For any issues or suggestions, feel free to open an issue on GitHub.

