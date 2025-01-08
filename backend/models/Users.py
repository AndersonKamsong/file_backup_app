from backend.config.DataSource import DataSource

class User:
    TABLE_NAME = "users"

    def __init__(self, id=None, username=None, email=None, role=None, password=None):
        self.id = id
        self.username = username
        self.email = email
        self.role = role
        self.password = password
        self.ds = DataSource()

    def save(self):
        # Update user if it exists
        if self.id:
            query = f"UPDATE {self.__class__.TABLE_NAME} SET username=%s, email=%s, role=%s, password=%s WHERE id=%s"
            self.ds.execute(query, (self.username, self.email, self.role, self.password, self.id))
        else:
            # Save into database
            query = f"INSERT INTO {self.__class__.TABLE_NAME} (username, email, role, password) VALUES(%s, %s, %s, %s)"
            self.ds.execute(query, (self.username, self.email, self.role, self.password))
            results = self.ds.execute(f"SELECT MAX(id) FROM {self.__class__.TABLE_NAME}")
            for result in results:
                new_instance_id = result[0]
            self.id = new_instance_id

    def read(self, id=None):
        if id:
            query = f"SELECT * FROM {self.__class__.TABLE_NAME} WHERE id=%s"
            result = self.ds.execute(query, (id,))
            return result
        else:
            query = f"SELECT * FROM {self.__class__.TABLE_NAME}"
            results = self.ds.execute(query)
            users = []
            for result in results:
                users.append(result)
            return users

    def findByEmail(self, email=None):
        if email:
            query = f"SELECT * FROM {self.__class__.TABLE_NAME} WHERE email=%s"
            result = self.ds.execute(query, (email,))
            return result
        else:
            return None
    
    def findByUsername(self, name=None):
        if name:
            query = f"SELECT * FROM {self.__class__.TABLE_NAME} WHERE username=%s"
            result = self.ds.execute(query, (name,))
            return result
        else:
            return None

    def delete(self, id=None):
        # Delete by id
        if id:
            query = f"DELETE FROM {self.__class__.TABLE_NAME} WHERE id=%s"
            self.ds.execute(query, (id,))
            print("User deleted successfully")
        else:
            self.ds.execute(f"DELETE FROM {self.__class__.TABLE_NAME}")
