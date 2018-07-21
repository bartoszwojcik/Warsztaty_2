#! python3
import argparse


def set_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username",
                        action="store_true", dest="movies", default=False,
                        help="Display all movies")
    parser.add_argument("-p", "--password",
                        action="store_true", dest="cinemas", default=False,
                        help="Display all cinemas")
    parser.add_argument("-n", "--new-pass",
                        action="store_true", dest="payments", default=False,
                        help="Display all payments")
    parser.add_argument("-l", "--list",
                        action="store_true", dest="tickets", default=False,
                        help="Display all tickets")
    parser.add_argument("-d", "--delete",
                        action="store_true", dest="tickets", default=False,
                        help="Display all tickets")
    parser.add_argument("-e", "--edit",
                        action="store_true", dest="tickets", default=False,
                        help="Display all tickets")

    options = parser.parse_args()
    return options


def solution(options):
    raise NotImplementedError("To be implemented.")


if __name__ == "__main__":

