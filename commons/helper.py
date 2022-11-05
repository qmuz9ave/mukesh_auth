import os
from getpass import getpass
from commons.db import UserData

class AuthHelper():
    def __init__(self) -> None:
        self.error_count = 0

    def handle_choice(self,choice_name=None):
        if choice_name:
            if choice_name == '1':
                self.sign_up()
            elif choice_name == '2':
                self.sign_in()
            elif choice_name == '3':
                print("....Exiting the application....")
                exit(0)
            else:
                return False
        else:
            return False

    def check_error_count(self):
        if self.error_count >=3:
            print("Error count exceeds the limit")
            raise Exception("Error count exceeds the limit")

    @staticmethod
    def validate_mobile_number(mobile_number):
        return mobile_number

    @staticmethod
    def validate_password(password,confirm_password):
        if password == confirm_password:
            return password
        else:
            print("\n....Password Does Not Match....\n")
            return False

    @staticmethod        
    def get_password():
        password = getpass("Enter Password: ")
        confirm_password = getpass("Re Enter Password: ")
        return password,confirm_password

    def sign_up(self):
        os.system('cls')
        print("======SIGN UP======\n")

        # mobile_number
        mobile_number = input("Enter Your Mobile Number: ")
        mobile_number = self.validate_mobile_number(mobile_number)

        #password
        password,confirm_password = self.get_password()
        valid_password = self.validate_password(password,confirm_password)

        while not valid_password:
            self.error_count+=1
            # self.check_error_count()
            if self.error_count >=3:
                os.system('cls')
                print("....You have exceeded your error limit\nPlease continue with the options")
                break
            self.get_password()
            valid_password = self.validate_password(password,confirm_password)

        user = UserData().objects().create(
            mobile_number=mobile_number,
            dob='11',
            password=password
        )

        print("User Registration Successful")
        

    def sign_in(self):
        os.system('cls')
        print("======SIGN IN======\n")
        mobile_number = input("Enter Your Mobile Number: ")
        password = input("Enter Your Password: ")

        user = UserData().objects().get(
            mobile_number=mobile_number,
            password=password
        )

        if user.instance:
            os.system('cls')
            print("======Login Successful======\n")
            print(f"WELCOME {user.instance.get('mobile_number')}")
            print("\nChoose the following options\n")
            choice = input("\nChange Password: 1\nLog Out: 2\n")

            if choice == "1":
                print("change password form")
            elif choice == "2":
                pass

        else:
            print("User Not Found")
            return False
       
