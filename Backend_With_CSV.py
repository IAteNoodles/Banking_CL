import csv
import hashlib
from os import times
import os
import time
from datetime import datetime, date
from cryptography import fernet
from cryptography.fernet import Fernet


def create_account() -> tuple:
    uid = input("Enter Unique ID: ")
    if len(uid) != 16:
        print("Invalid Unique ID")
        return 0
    data = list()
    # Checking if there already is a record with the unique ID in the database (CSV file)
    user_data = csv.reader(open(r"./user.csv"))
    for row in user_data:
        if row[0] == uid:
            for detail in row:
                data.append(detail)
            break
    # If no record with the unique ID in the database exists, asks for the data and adds it to the database.
    if len(data) == 0:
        data.append(uid)
        data.append(input("Name: "))
        data.append(input("Adress: "))
        data.append(input(" Date of Birth: "))
        data.append(int(input("Phone Number: ")))
        data.append(input("Email Address:"))
        csv.writer(open(r"./user.csv", "a")).writerows([data])
    print("Your record already exists in the database")
    print("----------------------------------------------------------------")
    print("Unique ID: %s\nName: %s\nAddress: %s\nDate of Birth: %s\nPhone Number: %s\nEmail Address: %s\n" % (data[0],
                                                                                                      data[1],
                                                                                                      data[2],
                                                                                                      data[3],
                                                                                                      data[4],
                                                                                                      data[5]))
    # Account Signing Form
    account_types = {1: "Savings Account",
                     2: "Current Account",
                     3: "Corporate Account"}
    print(account_types)
    account_type = account_types[int(input("Account Type: "))]
    print(account_type)
    print(account_types.items())
    if account_type not in account_types.values():
        print("Invalid Account Type")
        return
    else:
        print("Enter Amount for Account Initialization. (Minimum first time deposit required is Rs.1000")
        first_amount = int(input("Amount for Account Initialization: "))
        if first_amount < 1000:
            print("Minimum first time deposit required is Rs.1000")
            return
        user_count = open(r"./count.txt").read()
        open(r"./count.txt","w").write(str(int(user_count)+1))
        account_number = account_type.split()[0][0] + account_type.split()[1][0]
        account_number = account_number+(user_count)
        timestamp = time.time()
        with open(r"./account_details.csv","a",encoding="utf-8",newline="\n") as account_database:
            details = [account_number,uid, first_amount]
            csv.writer(account_database).writerow(details)
        print("Account created successfully")
        hash_text = account_number.join(str(timestamp))
        result = hashlib.sha256(hash_text.encode()).hexdigest()
        passbook_name = result+".csv"
        with open(r"./Passbooks/"+passbook_name,"w",newline="\n") as passbook:
            now = datetime.now()
            current_date = date.today().strftime("%d/%m/%Y")
            current_time = now.strftime("%H:%M:%S")
            fields = ["Credit","Deposit","Date","Time","Via"]
            details = ["",first_amount,current_date,current_time,"Initial Deposit"]
            csv.writer(passbook).writerow(fields)
            csv.writer(passbook).writerow(details)
            print("Passbook created successfully")
        password = input("Enter a atleast 8 characters password: ") # Check regex pattern later on.
        password = hashlib.sha256(password.encode()).hexdigest()
        key = Fernet.generate_key()
        with open(r"./Passbooks/"+passbook_name, 'rb') as unencrypted:
            _file = unencrypted.read()
            encrypted = Fernet(key).encrypt(_file)
        with open(r"./Passbooks/"+passbook_name, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
            print("Your key to access your account passbook is\n:",key)
            if input("Do you want to save this key? Enter y for yes:") == 'y':
                directory = os.path.join(account_number+"_key.key")
                open(directory, 'wb').write(key)
                print("Your key is saved at",directory)

                
def login() -> tuple:
    uid = input("Enter Unique ID: ")
    password = input("Enter Password: ")
    

if __name__ == '__main__':
    print("User: 1\n"
          "Admin: 2")
    choice = int(input("Enter Choice:"))
    if choice == 1:
        # User Panel
        print("Login: 1\n"
              "Create a new account: 2\n"
              "Forget password: 3\n"
              "Check application status: 4\n"
              "Check transaction status: 5")
        print("----------------------------------------------------------------")
        choice = int(input("Enter Choice:"))
        if choice == 1:
            token = login()
        elif choice == 2:
            token = create_account()
    elif choice == 2:
        # Admin Panel
        print("Login: 1\n")
