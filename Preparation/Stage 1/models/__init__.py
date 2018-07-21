class User:
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
