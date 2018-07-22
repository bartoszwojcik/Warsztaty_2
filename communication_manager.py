#! python3
import argparse
import models.hasher
from models import User
from psycopg2 import connect, OperationalError, IntegrityError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def establish_connection(cnx_cursor):
    """
    Simplified function for establishing connection. Provides data for connection, uses tuple as a set of cnx and cursor
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


def end_connection(cnx_cursor_pair):
    """
    Ends connection previously set up by establish_connection.
    :param cnx_cursor:
    :return:
    """
    cnx_cursor_pair[0].close()
    cnx_cursor_pair[1].close()
    print("Connection closed.")
    return


def set_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username",
                        dest="username", default=False,
                        help="Takes user login.")
    parser.add_argument("-p", "--password",
                        dest="password", default=False,
                        help="Takes user password for identification.")
    parser.add_argument("-l", "--list",
                        action="store_true", dest="list", default=False,
                        help="Lists all messages.")
    parser.add_argument("-t", "--to",
                        dest="to", default=False,
                        help="Specifies user to which a message is to be sent.")
    parser.add_argument("-s", "--send",
                        dest="send", default=False,
                        help="Sends a message to a user.")

    options = parser.parse_args()
    return options


def solution(options):
    raise NotImplementedError("To be implemented.")


if __name__ == "__main__":
    cnx_cursor = ["", ""]
    establish_connection(cnx_cursor)



    end_connection(cnx_cursor)
