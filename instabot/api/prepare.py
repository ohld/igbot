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
        lines = [line.strip().split(":") for line in f.readlines()] # '\n'
        if len(lines) == 1:
            return lines[0]
        else:
            print("Which account do you want to use? (Type number)")
            for ind, (login, password) in enumerate(lines):
                print(ind, login)
            while True:
                try:
                    ind = int(sys.stdin.readline())
                    if ind in list(range(len(lines))):
                        return lines[ind]
                except:
                    print("Wrong input. I need the number of account to use.")


def check_secret():
    while True:
        if os.path.exists(SECRET_FILE):
            with open(SECRET_FILE, "r") as f:
                try:
                    login, password = f.readline().strip().split(":")
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
                while True:
                    print("Enter your login: ")
                    f.write(str(sys.stdin.readline().strip()) + ":")
                    print("Enter your password: ")
                    f.write(getpass.getpass() + "\n")
                    print("Do you want to add another account? (y/n)")
                    if "y" not in sys.stdin.readline():
                        break


def delete_credentials():
    if os.path.exists(SECRET_FILE):
        os.remove(SECRET_FILE)


if __name__ == "__main__":
    check_secret()
