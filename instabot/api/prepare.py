#!/usr/bin/env python
import os
import sys
import getpass

SECRET_FILE = "secret.txt"


def get_credentials():
    "Returns login and password stored in SECRET_FILE"
    while not check_secret():
        pass
    with open(SECRET_FILE, "r") as f:
        login = f.readline().strip()
        password = f.readline().strip()
    return login, password


def check_secret():
    while True:
        if os.path.exists(SECRET_FILE):
            with open(SECRET_FILE, "r") as f:
                try:
                    login = f.readline().strip()
                    password = f.readline().strip()
                    if len(login) < 4 or len(password) < 6:

                        print("Data in 'secret.txt' file is invalid. "
                              "We will delete it and try again.")

                        os.remove(SECRET_FILE)
                    else:
                        return True
                except IOError:
                    print("Your file is broken. We will delete it "
                          "and try again.")
                    os.remove(SECRET_FILE)
        else:
            with open(SECRET_FILE, "w") as f:
                print("We need to create a text file 'secret.txt' where "
                      "we will store your login and password from Instagram.")
                print("Don't worry. It will be stored locally.")
                print("Enter your login: ")
                f.write(str(sys.stdin.readline()))
                print("Enter your password: ")
                f.write(getpass.getpass())


def delete_credentials():
    if os.path.exists(SECRET_FILE):
        os.remove(SECRET_FILE)


if __name__ == "__main__":
    check_secret()
