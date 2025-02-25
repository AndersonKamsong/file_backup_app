from backend.config.DataSource import DataSource

class Branch:
    TABLE_NAME = "branches"

    def __init__(self, branch_id=None, user_id=None, branch_name=None, folder_path=None):
        self.branch_id = branch_id
        self.user_id = user_id
        self.branch_name = branch_name
        self.folder_path = folder_path
        self.ds = DataSource()

    def save(self):
        """
        Save or update a branch in the database.
        """
        if self.branch_id:
            # Update the branch if it exists
            query = f"UPDATE {self.__class__.TABLE_NAME} SET user_id=?, branch_name=?, folder_path=? WHERE branch_id=?"
            self.ds.execute(query, (self.user_id, self.branch_name, self.folder_path, self.branch_id))
        else:
            # Create a new branch
            query = f"INSERT INTO {self.__class__.TABLE_NAME} (user_id, branch_name, folder_path) VALUES (?, ?, ?)"
            self.ds.execute(query, (self.user_id, self.branch_name, self.folder_path))
            results = self.ds.execute(f"SELECT MAX(branch_id) FROM {self.__class__.TABLE_NAME}")
            for result in results:
                new_instance_id = result[0]
            self.branch_id = new_instance_id

    def read(self, branch_id=None):
        """
        Retrieve branch details. If no branch_id is provided, fetch all branches.
        """
        if branch_id:
            query = f"SELECT * FROM {self.__class__.TABLE_NAME} WHERE branch_id=?"
            result = self.ds.execute(query, (branch_id,))
            return result
        else:
            query = f"SELECT * FROM {self.__class__.TABLE_NAME}"
            results = self.ds.execute(query)
            branches = []
            for result in results:
                branches.append(result)
            return branches

    def findByUser(self, user_id=None):
        """
        Retrieve all branches associated with a specific user.
        """
        if user_id:
            query = f"SELECT * FROM {self.__class__.TABLE_NAME} WHERE user_id=?"
            results = self.ds.execute(query, (user_id,))
            return results
        else:
            return None

    def findByUserAndName(self,user_id=None,branch_name=None):
        """
        Retrieve a branch by its name.
        """
        if branch_name and user_id:
            query = f"SELECT * FROM {self.__class__.TABLE_NAME} WHERE branch_name=? and user_id=?"
            result = self.ds.execute(query, (branch_name,user_id,))
            return result
        else:
            return None

    def delete(self, branch_id=None):
        """
        Delete a branch by its ID or all branches if no ID is provided.
        """
        if branch_id:
            query = f"DELETE FROM {self.__class__.TABLE_NAME} WHERE branch_id=?"
            self.ds.execute(query, (branch_id,))
            print("Branch deleted successfully")
        else:
            self.ds.execute(f"DELETE FROM {self.__class__.TABLE_NAME}")

# Example Usage:
# branch = Branch(user_id=1, branch_name="feature-xyz", folder_path="/path/to/folder")
# branch.save()
# print(branch.read())
