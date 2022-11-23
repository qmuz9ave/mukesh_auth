import os
from getpass import getpass
from commons.db import UserData,OrderData
from datetime import datetime
import time
import pandas as pd

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
        if not mobile_number.startswith("0"):
            print("\n....Mobile number must starts with zero....\n")
            return False

        if len(mobile_number) != 10:
            print("\n....Length of mobile number must be 10....\n")
            return False

        return mobile_number

    @staticmethod
    def validate_password(password,confirm_password):
        if password == confirm_password:
            return password
        else:
            print("\n....Password Does Not Match....\n")
            return False

    @staticmethod
    def validate_dob(dob):
        try:
            dob = datetime.strptime(dob,"%Y-%m-%d")
            today = datetime.now()
            age = today-dob
        except Exception as e:
            print(str(e))
            return False
        
        age = age.days/365
        if age < 21:
            print(f"\n....You age is {int(age)} So you are not eligible....\n")
            return False

        return dob

    @staticmethod        
    def get_password():
        password = getpass("Enter Password: ")
        confirm_password = getpass("Re Enter Password: ")
        return password,confirm_password

    def sign_up(self):
        os.system('cls')
        print("======SIGN UP======\n")
        #name
        full_name = input("Enter Your Name: ")
        address = input("Enter Your Address: ")
        #dob
        dob = input("Enter Your DOB [yy-mm-dd]: ")
        valid_dob = self.validate_dob(dob)

        if not valid_dob:
            return False
        # mobile_number
        mobile_number = input("Enter Your Mobile Number: ")
        mobile_number = self.validate_mobile_number(mobile_number)
        if not mobile_number:
            return False
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
            name=full_name,
            mobile_number=mobile_number,
            dob=dob,
            address=address,
            password=password
        )

        print("\n....User Registration Successful\nNow You Can Sign In...\n")
        

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
            print(f"WELCOME {user.instance.get('name')}")
            print("\nChoose the following options\n")
            choice = input("\nChange Password: 1\nOrdering: 2\nLog Out: 3\n")

            if choice == "1":
                print("\n....change password form....\nPlease Enter Your New Password")
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

                user.objects().update(password=password)
                print("\n....Password Changed Successfully....\n")
                return True
            elif choice == "2":
                self.ordering(user=user.instance)  
            elif choice == "3":
                pass

        else:
            print("User Not Found")
            return False
       
    def ordering(self,user):
        print("\n....Ordering form....\nPlease Enter Your Choice")
        print("\nEnter 1 to start ordering")
        print("\nEnter 2 to to print statistic")
        print("\nEnter 3 to to LogOut\n")
        choice = input("Please select an option: ")

        if choice == "1":
            os.system('cls')
            choice = input("\nEnter 1 for Dine in\nEnter 2 for Order Online\nEnter 3 for Login Page\nEnter Your Choice: ")
            if choice == "1":
                menu_choice,price = self.get_menu_choice()
                print(menu_choice)
                
                order_data = OrderData()
                order_data.objects().create(
                    name = menu_choice,
                    user_id = user.get("id"),
                    type = choice,
                    price = price
                )
                print("\n....Your Order has been placed successfully....\n wait for a whie")
                print("-------------------------------------------------------------------\n")
                print(f"Your Total Paybale is {price} AUD including 7.5 for service charge")
                print("-------------------------------------------------------------------\n")
                time.sleep(3)
                return self.ordering(user=user)
                
            elif choice == "2":
                os.system('cls')
                delivery_choice = input("\nEnter 1 for Self Pickup\nEnter 2 for Home Delivery\nEnter 3 for Previous Menu\nEnter Your Choice: ")
                if delivery_choice == "1":
                    delivery_option ="Self PickUP"
                elif delivery_choice == "2":
                    delivery_option =" Home Delivery"
                elif delivery_choice == "3":
                    self.ordering(user=user)
                menu_choice,price = self.get_menu_choice()
                order_data = OrderData()
                order_data.objects().create(
                    name = menu_choice,
                    user_id = user.get("id"),
                    type = choice,
                    price = price,
                    delivery = delivery_option
                )
                print("\n....Your Order has been placed successfully....\n wait for a whie")
                print("-------------------------------------------------------------------\n")
                print(f"Your Total Paybale is {price} AUD")
                print("-------------------------------------------------------------------\n")
                time.sleep(3)
                return self.ordering(user=user)
            elif choice == "3":
                return False
            else: return False

        elif choice == "2":
            order_data = OrderData()
            user_orders = order_data.objects().filter(user_id=user.get("id"))
            data_frames = pd.DataFrame.from_records(user_orders)
            print(data_frames)
            return self.ordering(user=user)
        elif choice == "3":
            return False

    def get_menu_choice(self):
        os.system('cls')
        print("\nEnter 1 for Noodles    Price AUD 2\n")
        print("\nEnter 2 for Sandwitch  Price AUD 4\n")
        print("\nEnter 3 for Dumpling   Price AUD 6\n")
        print("\nEnter 4 for Muffins    Price AUD 8\n")
        print("\nEnter 5 for Checkout\n")
        choice = input("Place Your Order: ")
        if choice == "1":
            choice =  "Noodles",2
        elif choice == "2":
           choice = "Sandwich",4
        elif choice == "3":
            choice = "Dumpling",6
        elif choice == "4":
           choice = "Muffins",8
        cnfrm = input("Please Enter Y to proceed to checkout or N to cancel: ")
        if cnfrm == "Y" or cnfrm == "y":
            return choice
        else:
            return False