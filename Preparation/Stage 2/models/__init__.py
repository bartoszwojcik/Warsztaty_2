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
        if self.__id == -1:
            sql = """INSERT INTO Users(username, email, hashed_password)
                      VALUES(%s, %s, %s) RETURNING id"""
            values = (self.username, self.email, self.hashed_password)
            cursor.execute(sql, values)
            self.__id = cursor.fetchone()[0]
            return True
        return False

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
            return None

        return None
