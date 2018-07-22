#! python3
import argparse
import models.hasher
from models import User
from psycopg2 import connect, OperationalError, IntegrityError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Possibilities for improvement:
# ToDo: usernames and passwords should forbid spaces
# ToDo: usernames only in lowercase
# ToDo: could add message_read if a particular message has been displayed
# ToDo: could make functions out of some repeatable elements, e.g. username and password checking


def establish_connection(cnx_cursor):
    """
    Simplified function for establishing connection with a database. Provides login data for connection, uses tuple
     as a set of cnx and cursor
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
                        help="Takes input as user's login.")
    parser.add_argument("-p", "--password",
                        dest="password", default=False,
                        help="Takes input as user's password. Checks if there are at least 8 characters.")
    # Changed new-pass into newpass
    parser.add_argument("-n", "--newpass",
                        dest="newpass", default=False,
                        help="Accepts new password for a user.")
    parser.add_argument("-l", "--list",
                        action="store_true", dest="list", default=False,
                        help="Lists all users.")
    parser.add_argument("-d", "--delete",
                        action="store_true", dest="delete", default=False,
                        help="Deletes provided user login.")
    # The following requested parameter seems unnecessary. Could be used for changing username though.
    # parser.add_argument("-e", "--edit",
    #                     dest="edit", default=False,
    #                     help="Modifies provided user login.")

    options = parser.parse_args()

    return options


def solution(options):
    """
    Checks which parameters have been provided by the user and perform respective action.
    :param options: parameters provided by users via set_options function.
    :return:
    """

    # -u and -p parameters only (Create user)
    if options.username and options.password and not options.newpass and not options.delete and not options.list:

        user_collection = []
        try:
            user_collection = User.load_all_ids_usernames(cnx_cursor[1])
        except:
            print("Failed to load user data.")

        if len(options.password) < 8:
            return "Password too short. Provide at least 8 characters."
        else:
            for item in user_collection:
                if options.username == item.username:
                    return "Error: User already exists."

            # Perform operation
            new_user = User()
            new_user.username = options.username
            new_user.email = options.username + "@test.com"
            new_user.set_password(options.password, models.hasher.generate_salt())
            new_user.save_to_db(cnx_cursor[1])
            return "User created."

    # -u -p and -n parameters (Modify user password)
    elif options.username and options.password and options.newpass and not options.delete and not options.list:

        user_collection = []
        try:
            user_collection = User.load_all_ids_usernames(cnx_cursor[1])
        except:
            print("Failed to load user data.")

        # Check login
        for item in user_collection:
            if options.username == item.username:

                # Load one user
                user_data = User.load_user_by_id(cnx_cursor[1], item.id)

                # Check if password is correct
                if models.hasher.check_password(options.password, user_data.hashed_password) is True:
                    if len(options.newpass) < 8:
                        return "New password too short. Provide at least 8 characters."
                    # Perform operation
                    user_data.set_password(options.newpass, models.hasher.generate_salt())
                    user_data.save_to_db(cnx_cursor[1])
                    return "Password changed."
                else:
                    return "Wrong password."
        return "No such user found. Create new user using parameters: --username and --password"

    # -u -p and -d parameters (Delete user)
    elif options.username and options.password and options.delete and not options.newpass and not options.list:

        user_collection = []
        try:
            user_collection = User.load_all_ids_usernames(cnx_cursor[1])
        except:
            print("Failed to load user data.")

        # Check login
        for item in user_collection:
            if options.username == item.username:

                # Load one user
                user_data = User.load_user_by_id(cnx_cursor[1], item.id)

                # Check if password is correct
                if models.hasher.check_password(options.password, user_data.hashed_password) is True:
                    # Perform operation
                    user_data.delete(cnx_cursor[1])
                    return "User deleted."
                else:
                    return "Wrong password."
        return "No such user found."

    # -l parameter (List all users)
    elif options.list and not options.username and not options.password and not options.delete and not options.newpass:
        user_list = User.list_usernames(cnx_cursor[1])
        user_list.sort()
        print("### List of users ###")
        for username in user_list:
            print(username)
        return "### List ended ###"
    else:
        return "No function for those parameters found."


if __name__ == "__main__":

    # Set up connection and download class data
    cnx_cursor = ["", ""]
    establish_connection(cnx_cursor)

    print(solution(set_options()))

    # End connection
    end_connection(cnx_cursor)
