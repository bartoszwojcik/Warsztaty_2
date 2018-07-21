#! python3

# CREATE TABLE public.users
# (
#   id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass),
#   email character varying(255),
#   username character varying(255),
#   hased_password character varying(80),
#   CONSTRAINT users_pkey PRIMARY KEY (id)
# )

import models.hasher
from models import User
from psycopg2 import connect, OperationalError, IntegrityError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def establish_connection(cnx_cursor):
    """
    Simplified method for establishing connection. Provides data for connection, uses tuple as a set of cnx and cursor.
    :param cnx_cursor:
    :return:
    """
    username = "postgres"
    passwd = "coderslab"
    hostname = "localhost"
    db_name = "workshop_db"

    try:
        cnx_cursor[0] = connect(user=username, password=passwd, host=hostname, database=db_name)
        cnx_cursor[0].set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cnx_cursor[1] = cnx_cursor[0].cursor()
        print("Connection established.")
        return cnx_cursor

    except OperationalError:
        print("Failed to connect.")
        return


def end_connection(cnx_cursor):
    """
    Ends connection previously set up by establish_connection.
    :param cnx_cursor:
    :return:
    """
    cnx_cursor[0].close()
    cnx_cursor[1].close()
    print("Connection closed.")
    return


if __name__ == "__main__":
    cnx_cursor = ["", ""]
    establish_connection(cnx_cursor)

    # Create test classes
    try:
        test_user_1 = User()
        test_user_1.username = "testmah"
        test_user_1.email = "mah@test.com"
        test_user_1.set_password("admin123", models.hasher.generate_salt())
        test_user_1.save_to_db(cnx_cursor[1])
    except IntegrityError:
        print("User already exists in the database.")

    # Load user
    test_user_2 = User.load_user_by_id(cnx_cursor[1], 2)    # None for removed User
    test_user_3 = User.load_user_by_id(cnx_cursor[1], 3)
    print(test_user_3.username)

    # Load all users and test if correct
    all_user_list = User.load_all_users(cnx_cursor[1])
    print(all_user_list[0].username)

    end_connection(cnx_cursor)
