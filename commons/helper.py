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
        os.system('cls')
        print("\n=====ORDERING FORM======\nPlease Enter Your Choice")
        print("\nEnter 1 to start ordering")
        print("\nEnter 2 to to print statistic")
        print("\nEnter 3 to to LogOut\n")
        choice = input("Please select an option: ")

        if choice == "1":
            os.system('cls')
            choice = input("\nEnter 1 for Dine in\nEnter 2 for Order Online\nEnter 3 for Login Page\nEnter Your Choice: ")
            if choice == "1":
                menu_choice,price = self.get_menu_choice()
                if not menu_choice:
                    self.ordering(user=user)
                number_of_person = input("Please Enter Number Of Person: ")
                date_of_visit = input("Enter Date Of Visit[yy-mm-dd]: ")
                time_of_visit = input("Enter Time Of Visit[h:m]: ")
                
                order_data = OrderData()
                order_data.objects().create(
                    name = menu_choice,
                    user_id = user.get("id"),
                    type = choice,
                    price = price,
                    no_of_person=number_of_person,
                    date_of_visit=date_of_visit,
                    time_of_visit=time_of_visit
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
                date_of_pickup=""
                time_of_pickup=""
                date_of_delivery=""
                time_of_delivery=""
                name_of_person_picking_up=""
                if delivery_choice == "1":
                    delivery_option ="Self PickUP"
                    date_of_pickup = input("Please Enter Date Of Pickup[yy-mm-dd]: ")
                    time_of_pickup = input("Please Enter Time Of Pickup[h:m]: ")
                    name_of_person_picking_up = input("Please Enter Name Of Person Picking Up: ")
                elif delivery_choice == "2":
                    date_of_delivery=input("Please Enter Date Of Delivery[yy-mm-dd]: ")
                    time_of_delivery=input("Please Enter Time Of Delivery[h:m]: ")
                    delivery_option ="Home Delivery"
                elif delivery_choice == "3":
                    self.ordering(user=user)
                else:
                    return False
                menu_choice,price = self.get_menu_choice()
                if not menu_choice:
                    self.ordering(user=user)
                order_data = OrderData()
                order_data.objects().create(
                    name = menu_choice,
                    user_id = user.get("id"),
                    type = choice,
                    price = price,
                    delivery = delivery_option,
                    date_of_pickup=date_of_pickup,
                    time_of_pickup=time_of_pickup,
                    name_of_person_picking_up=name_of_person_picking_up,
                    date_of_delivery=date_of_delivery,
                    time_of_delivery=time_of_delivery,
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
            statistic_choice = input("Please Enter Option to Print The Statistics.\n1.All Dine in Orders\n2.All Pick up Order\n3.All Deliveries\n4.All Orders\n5.Total Amount Spent on All Orders\n6.Go to Previous Menu\n : ")
            order_data = OrderData()
            if statistic_choice == "1":
                user_orders = order_data.objects().filter(type="1")
                data_frames = pd.DataFrame.from_records(user_orders)
            elif statistic_choice =="2":
                user_orders = order_data.objects().filter(delivery="Self PickUP")
                data_frames = pd.DataFrame.from_records(user_orders)
            elif statistic_choice =="3":
                user_orders_pickup = order_data.objects().filter(delivery="Self PickUP")
                user_orders_home = order_data.objects().filter(delivery="Home Delivery")
                all = user_orders_pickup+user_orders_home
                data_frames = pd.DataFrame.from_records(all)
            elif statistic_choice =="4":
                user_orders= order_data.objects().all()
                data_frames = pd.DataFrame.from_records(user_orders)
            elif statistic_choice =="5":
                user_orders= order_data.objects().all()
                total_price = 0
                for order in user_orders:
                    price = order.get("price")
                    total_price = total_price +int(price)

                print("=====================================================")
                print(f"Total Price Spend is : {total_price} USD")
                print("=====================================================")
                return False
            else:
                return False
            print(data_frames)
            time.sleep(5)
            return self.ordering(user=user)
        elif choice == "3":
            return False

    def get_menu_choice(self):
        os.system('cls')
        print("===============MENU===================")
        print('\n=====normal====')
        print("\nEnter 1 for Noodles    Price AUD 2")
        print("\nEnter 2 for Sandwitch  Price AUD 4")
        print("\nEnter 3 for Dumpling   Price AUD 6")
        print("\nEnter 4 for Muffins    Price AUD 8")
        print("\nEnter 5 for Pasta      Price AUD 10")
        print("\nEnter 6 for Pizza      Price AUD 20")
        print('\n=====liquairs====')
        print("\nEnter 7 for Coffee      Price AUD 2")
        print("\nEnter 8 for Cold Drink  Price AUD 4")
        print("\nEnter 9 for Shake       Price AUD 6\n")
        choice = input("Place Your Order: ")
        if choice == "1":
            choice =  "Noodles",2
        elif choice == "2":
           choice = "Sandwich",4
        elif choice == "3":
            choice = "Dumpling",6
        elif choice == "4":
           choice = "Muffins",8
        elif choice == "5":
            choice = "Pasta",10
        elif choice == "6":
            choice = "Pizza",20
        elif choice == "7":
            choice = "Coffee",2
        elif choice == "8":
            choice = "Cold Drink",4
        elif choice == "9":
            choice = "Shake",6
        else:
            return False,None

        cnfrm = input("Please Enter Y to proceed to checkout or N to cancel: ")
        if cnfrm == "Y" or cnfrm == "y":
            return choice
        else:
            return False,None