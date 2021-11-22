import csv



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
    print("Unique ID:%s, Name:%s, Address:%s, Date of Birth:%s, Phone Number:%s, Email Address:%s" % (data[0],
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
    account_type = int(input("Account Type: "))
    if account_type not in account_types.keys():
        print("Invalid Account Type")


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
