#! python3
import argparse
import models.hasher
import time
import datetime
from models import Message, User
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
                        help="Takes and sends a message to specified user.")

    options = parser.parse_args()
    return options


def solution(options):
    """
    Checks which parameters have been provided by the user and perform respective action.
    :param options: parameters provided by users via set_options function.
    :return:
    """

    # -u -p -l parameters (List all messages for this user)
    if options.username and options.password and options.list and not options.send and not options.to:

        # Check login and pass
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
                if models.hasher.check_password(options.password, user_data.hashed_password) is False:
                    return "Wrong password."

                # Collect all messages
                message_collection = Message.load_all_messages_for_user(cnx_cursor[1], item.id)

                # Display
                print("### Messages for you:")
                for element in message_collection:
                    print("From:", element.from_user, "\nDate:",
                          element.creation_date,
                          "\nMessage:", element.message_content, "\n")
                return "###"

        return "No such user found."

    # -u -p -s -t parameters (Send message to specified user)
    elif options.username and options.password and options.send and not options.list:

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
                if models.hasher.check_password(options.password, user_data.hashed_password) is False:
                    return "Wrong password."

                # See if options.to is provided; if not, display no recipient. Likely to be redundant since parameters
                # are checked by the parser.
                if options.to is False:
                    return "No recipient provided in argument -t"

                # See if recipient is in database
                for member in user_collection:
                    if options.to == member.username:
                        recipient_id = member.id

                        # Check message length <= 255
                        if len(options.send) > 255:
                            return "Message too long. Maximum is 255 characters."

                        if len(options.send) < 1:
                            return "Nothing to send. Please type message after parameter -s"

                        # Send message
                        new_mssg = Message()
                        new_mssg.from_id = item.id
                        new_mssg.to_id = recipient_id
                        new_mssg.message_content = options.send
                        new_mssg.creation_date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                        new_mssg.save_to_db(cnx_cursor[1])
                        return "Message sent."
                return "No recipient found in database."

        return "No such user found."

    else:
        return "No function for those parameters found. Try -u -p -s -t for sending or -u -p -l for listing messages."


if __name__ == "__main__":

    # Set up connection and download class data
    cnx_cursor = ["", ""]
    establish_connection(cnx_cursor)

    print(solution(set_options()))

    # End connection
    end_connection(cnx_cursor)
