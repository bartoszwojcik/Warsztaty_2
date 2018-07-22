class User:
    """
    Requires hasher module.
    """
    __id = None
    email = None
    username = None
    __hashed_password = None

    def __init__(self):
        self.__id = -1
        self.username = ""
        self.email = ""
        self.__hashed_password = ""

    @property
    def id(self):
        return self.__id

    @property
    def hashed_password(self):
        return self.__hashed_password

    def set_password(self, password, salt):
        self.__hashed_password = hasher.password_hash(password, salt)

    def save_to_db(self, cursor):
        """
        Previously this checked if an object is already in the database. Now it updates data if object is present.
        :param cursor:
        :return:
        """
        if self.__id == -1:
            sql = """INSERT INTO Users(username, email, hashed_password)
                      VALUES(%s, %s, %s) RETURNING id"""
            values = (self.username, self.email, self.hashed_password)
            cursor.execute(sql, values)
            self.__id = cursor.fetchone()[0]
            return True
        else:
            sql = """UPDATE Users SET username=%s, email=%s, hashed_password=%s WHERE id=%s"""
            values = (self.username, self.email, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True


    @staticmethod
    def load_user_by_id(cursor, user_id):
        """Creates a new user object based on data from SQL database."""
        sql = "SELECT id, username, email, hashed_password FROM users WHERE id=%s"
        cursor.execute(sql, (user_id, ))
        data = cursor.fetchone()
        if data:
            #This creates a new users
            loaded_user = User()
            loaded_user.__id = data[0]
            loaded_user.username = data[1]
            loaded_user.email = data[2]
            loaded_user.__hashed_password = data[3]
            return loaded_user
        else:
            print("No user with that id found.")
            return None

        return None

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, email, hashed_password FROM Users"
        result = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            loaded_user = User()
            loaded_user.__id = row[0]
            loaded_user.username = row[1]
            loaded_user.email = row[2]
            loaded_user.__hashed_password = row[3]
            result.append(loaded_user)
        return result

    def delete(self, cursor):
        sql = """DELETE FROM Users WHERE id=%s"""
        try:
            cursor.execute(sql, (self.__id, ))
            self.__id = -1
            return True
        except AttributeError:
            print("No user with that id found for deletion.")
            return False


