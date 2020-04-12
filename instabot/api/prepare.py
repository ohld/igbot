#!/usr/bin/env python

import getpass
import os
import sys

DEFAULT_SECRET_DIR = os.path.abspath(os.getcwd())


def get_credential_file(base_path=DEFAULT_SECRET_DIR):
    return base_path + "/config/secret.txt"


def add_credentials(base_path):
    SECRET_FILE = get_credential_file(base_path)
    with open(SECRET_FILE, "a") as f:
        print("Enter your login: ")
        f.write(str(sys.stdin.readline().strip()) + ":")
        print(
            "Enter your password: (it will not be shown due to security "
            + "reasons - just start typing and press Enter)"
        )
        f.write(getpass.getpass() + "\n")


def get_credentials(base_path, username=None):
    SECRET_FILE = get_credential_file(base_path)
    """Returns login and password stored in `secret.txt`."""
    while not check_secret():
        pass
    while True:
        try:
            with open(SECRET_FILE, "r") as f:
                lines = [line.strip().split(":", 2) for line in f.readlines()]
        except ValueError:
            msg = "Problem with opening `{}`, will remove the file."
            raise Exception(msg.format(SECRET_FILE))
        if username is not None:
            for login, password in lines:
                if login == username.strip():
                    return login, password
        print("Which account do you want to use? (Type number)")
        for ind, (login, password) in enumerate(lines):
            print("%d: %s" % (ind + 1, login))
        print("%d: %s" % (0, "add another account."))
        print("%d: %s" % (-1, "delete all accounts."))
        try:
            ind = int(sys.stdin.readline())
            if ind == 0:
                add_credentials(base_path)
                continue
            elif ind == -1:
                delete_credentials(base_path)
                check_secret(base_path)
                continue
            elif 0 <= ind - 1 < len(lines):
                return lines[ind - 1]
        except Exception:
            print("Wrong input, enter the number of the account to use.")


def check_secret(base_path):
    SECRET_FILE = get_credential_file(base_path)
    while True:
        if os.path.exists(SECRET_FILE):
            with open(SECRET_FILE, "r") as f:
                try:
                    login, password = f.readline().strip().split(":")
                    if len(login) < 4 or len(password) < 6:

                        print(
                            "Data in `secret.txt` file is invalid. "
                            "We will delete it and try again."
                        )

                        os.remove(SECRET_FILE)
                    else:
                        return True
                except Exception:
                    print("Your file is broken. We will delete it " + "and try again.")
                    os.remove(SECRET_FILE)
        else:
            print(
                "We need to create a text file '%s' where "
                "we will store your login and password from Instagram." % SECRET_FILE
            )
            print("Don't worry. It will be stored locally.")
            while True:
                add_credentials(base_path)
                print("Do you want to add another account? (y/n)")
                if "y" not in sys.stdin.readline():
                    break


def delete_credentials(base_path):
    SECRET_FILE = get_credential_file(base_path)
    if os.path.exists(SECRET_FILE):
        os.remove(SECRET_FILE)


if __name__ == "__main__":
    check_secret()
