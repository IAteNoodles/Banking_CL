import csv
import hashlib
import io
import json
import re
import time
from datetime import date, datetime
from os import times
import pandas as pd
from cryptography.fernet import Fernet
import pickle

def create_account() -> None:
    uid = input("Enter Unique ID: ")
    if len(uid) != 16:
        print("Invalid Unique ID")
        create_account()
    data = list()
    # Checking if there already is a record with the unique ID in the database (CSV file)
    user_data = csv.reader(open(r"./user.csv"))
    for row in user_data:
        if row[0] == uid:
            for detail in row:
                data.append(detail)
            # Exists the loop once data is retrieved.
            break
    # Check:    If no record with the unique ID in the database exists, asks for the data and adds it to the database.
    if len(data) == 0:
        data.append(uid)
        data.append(input("Name: "))
        data.append(input("Adress: "))
        data.append(input(" Date of Birth: "))
        data.append(int(input("Phone Number: ")))
        data.append(input("Email Address:"))
        csv.writer(open(r"./user.csv", "a",newline="\n")).writerows([data])
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
                     3: "Business Account"}
    print("Choose Account Type:")
    formated_account_types = json.dumps(account_types, indent=2).strip("{}")
    for types in formated_account_types.split(","):
        print(types.replace("\"",""))
    try:
        account_type = account_types[int(input("Account Type: "))]
        while(True):
            print("Enter Amount for Account Initialization.")
            print("Minimum first time deposit required is Rs.1000")
            first_amount = int(input("Amount for Account Initialization: "))
            if first_amount >= 1000:
                break
        # Opens up the count.dat file which contains the various counters.
        with open(r"./count.dat","rb+") as count_file:
            counter = pickle.load(count_file)
            user_count = counter[account_type]
            counter[account_type] = user_count+1
            pickle.dump(counter, open("./count.dat","wb"))
        account_number = account_type.split()[0][0] + account_type.split()[1][0]
        account_number = account_number+str(user_count)
        timestamp = time.time()
        with open(r"./account_details.csv","a",encoding="utf-8",newline="\n") as account_database:
            details = [account_number,uid,timestamp,first_amount]
            csv.writer(account_database).writerow(details)
        print("Account created successfully")
        # Salts the account number with the timestamp.
        hash_text = account_number.join(str(timestamp))
        # Hashes the resulting string.
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
        # Encrypt the passbook.
        key = Fernet.generate_key()
        with open(r"./Passbooks/"+passbook_name, 'rb') as unencrypted:
            _file = unencrypted.read()
            encrypted = Fernet(key).encrypt(_file)
        with open(r"./Passbooks/"+passbook_name, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
            print("Your key to access your account passbook is:\n",key)
            if input("Do you want to save this key? Enter y for yes:") == 'y':
                directory = "./Keys/"+account_number+"_key.key"
                open(directory, 'wb').write(key)
                print("Your key is saved at",directory)
    except KeyError:
        print("Wrong Account Type")
                
def login() -> tuple:
    uid = input("Enter Unique ID: ")
    if len(uid) !=16:
        print("Invalid Unique ID")
        return None
    with open(r"./account_details.csv",newline="\n") as database:
        list_of_account = csv.DictReader(database)
        user_accounts = list()
        for details in list_of_account:
            if details['user unique id'] == uid:
                print("--------------------------------------------------------")
                print("Account number:", details['account number'])
                account_type = details["account number"]
                if "SA" in account_type:
                    account_type = "Savings"
                elif "CA" in account_type:
                    account_type = "Current"
                else:
                    account_type = "Bussiness"
                print("Account type:", account_type)
                user_accounts.append(details)
                account_number = input("Enter the account number you want to login in: ")
                for user in user_accounts:
                    if user['account number'] == account_number:
                        timestamp = user['timestamp']
                        # Salts the account number with the timestamp.
                        hash_text = account_number.join(str(timestamp))
                        print(timestamp)
                        # Hashes the resulting string.
                        result = hashlib.sha256(hash_text.encode()).hexdigest()
                        passbook_name = result+".csv"
                        passbook_location = r"./Passbooks/"+passbook_name
                        key = Fernet(input("Enter the account key:"))
                        with open(passbook_location,'rb') as file:
                            encrypted = file.read()
                        decrypted = key.decrypt(encrypted)
                        with open(passbook_location,"wb") as file:
                            file.write(decrypted)
                        def account_actions():
                            print("Welcome")
                            print("Enter 1 to deposit to your account.")
                            def deposit():
                                amount = int(input("Enter amount to be deposit to your account"))
                                via = int(input("Select Payment method.\n1-Cash\n2Cheque\nEnter your method: "))
                                with open(passbook_location,"a",newline="\n") as account:
                                    now = datetime.now()
                                    current_date = date.today().strftime("%d/%m/%Y")
                                    current_time = now.strftime("%H:%M:%S")
                                    csv.writer(account).writerow(["",amount,current_date,current_time,via])
                                    dataframe = pd.read_csv(r"./account_details.csv")
                                    dataframe.loc[0,"current balance"] = dataframe.loc[0,"current balance"]+amount
                                    dataframe.to_csv(r"./account_details.csv",index=False)
                                print("Successful")
                            print("Enter 2 to withdraw from your account.")
                            choice = int(input("Enter Choice: "))
                            if choice == 1:
                                deposit()
                        account_actions()
                        with open(passbook_location,"wb") as file:
                            file.write(encrypted)
                            
                        
        if len(user_accounts) == 0:
            print("No account linked to your unique ID found.")
            if input("Do you want to create an account?\nEnter y for yes:") == 'y':
                create_account()    
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
