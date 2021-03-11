# database.py
# responsible for loading up the users.txt file

# we want the date and time the account was created
import datetime

class DataBase:
    def __init__(self, filename):
        # initializer - what file are we working with?
        self.filename = filename
        self.users = None
        self.file = None
        self.load()

    # load all data into a dictionary - stored in self.users on line 11
    def load(self):
        self.file = open(self.filename, "r")
        self.users = {}

        for line in self.file:
            # split line up by ; (delimitor)
            phone, password, name, created = line.strip().split(";")
            self.users[phone] = (password, name, created)

        self.file.close()

    # return user's data upon validated login
    def get_user(self, phone):
        if phone in self.users:
            return self.users[phone]
        else:
            # didn't find key
            return -1

    def add_user(self, phone, password, name):
        # strip to get rid of leading whitespaces
        # self.users has already been loaded up by this point, check for duplicate
        if phone.strip() not in self.users:
            # add key to dictionary
            self.users[phone.strip()] = (password.strip(), name.strip(), DataBase.get_date())
            self.save()
            # successful
            return 1
        else:
            print("Phone number already exists in system.")
            return -1

    def validate(self, phone, password):
        # verify user exists and get phone number from db
        if self.get_user(phone) != -1:
            return self.users[phone][0] == password
        else:
            return False

    # write everything into our dictionary ("users.txt")
    def save(self):
        with open(self.filename, "w") as f:
            for user in self.users:
                f.write(user + ";" + self.users[user][0] + ";" + self.users[user][1] + ";" + self.users[user][2] + "\n")

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]