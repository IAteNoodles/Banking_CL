import csv
def create_account():
    uid = input("Enter Unique ID: ")
    if len(uid) != 16:
        print("Invalid Unique ID")
        return 0
def login():
    uid = input("Enter Unique ID: ")
    password = input("Enter Password: ")
if __name__ == '__main__':
    print("User: 1\n"
          "Admin: 2")
    choice = int(input("Enter Choice:"))
    if choice == 1:
        #User Panel
        print("Login: 1\n"
              "Create a new account: 2\n"
              "Forget password: 3\n"
              "Check application status: 4\n"
              "Check transaction status: 5")
        choice = int(input("Enter Choice:"))
        if choice == 1:
            token = login()
    elif choice == 2:
        #Admin Panel
        print("Login: 1\n")