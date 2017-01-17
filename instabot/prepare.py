#!/usr/bin/env python
import os, sys

def get_credentials():
    "Returns login and password stored in secret.txt"
    while not check_secret():
        pass

    with open("secret.txt", "r") as f:
        login = f.readline().strip()
        password = f.readline().strip()

    return login, password

def check_secret():
    while True:
        if os.path.exists("secret.txt"):
            with open("secret.txt", "r") as f:
                try:
                    login = f.readline().strip()
                    password = f.readline().strip()
                    if len(login) < 4 or len(password) < 8:
                        print ("Data in 'secret.txt' file is invalid. We will delete it and try again.")
                        os.remove("secret.txt")
                    else:
                        return True
                except:
                    print ("Your file is broken. We will delete it and try again.")
                    os.remove("secret.txt")
        else:
            with open("secret.txt", "w") as f:
                print ("We need to create a text file 'secret.txt' where we will store your login and password from Instagram.")
                print ("Don't worry. It will be stored locally.")
                print ("Enter your login: ")
                f.write(str(sys.stdin.readline()))
                print ("Enter your password: ")
                f.write(str(sys.stdin.readline()))


if __name__ == "__main__":
    check_secret()
