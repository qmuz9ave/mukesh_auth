import os
from commons.helper import AuthHelper
from commons.db import sqlite

def main():
    print("Sign Up:  1\nSign In:  2\nQuit:     3")
    main_choice = input("Enter Your Choice: ")
    sqlite().create_table()
    auth = AuthHelper()
    resp = auth.handle_choice(main_choice)
    if not resp:
        main()

if __name__ == '__main__':
    main()
