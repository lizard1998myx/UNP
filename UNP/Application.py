import random, time
from UNP.Core import Account, ActTable


class Loginer:
    def __init__(self):
        self.mode = "001"
        self.timer = -1
        self.file = ""

    def __str__(self):
        string = "mode-" + self.mode + "_timer-" + str(self.timer)
        if self.file != "":
            string = string + "_filename-" + self.file
        return string

    def _iterator(self):
        userlist_201901 = []
        userlist_201906 = []
        userlist_201907 = []

        userlist = []
        if self.mode[0] == '1':
            userlist = userlist + userlist_201901
        if self.mode[1] == '1':
            userlist = userlist + userlist_201906
        if self.mode[2] == '1':
            userlist = userlist + userlist_201907
        random.shuffle(userlist)
        for user in userlist:
            yield Account(username=user[0], name=user[1])

    def active(self):
        if self.mode[0].lower() in ['f', 't']:
            for account in ActTable(input("Enter filename:")).iterator():
                account.load()
                if account.accessibility:
                    print("Welcome! " + account.name)
                    if self.timer == -1:
                        if input("Enter Y to stop:").lower() == 'y':
                            return
                    else:
                        print("refresh in " + str(self.timer) + " seconds...")
                        time.sleep(self.timer)
        elif self.mode[0].lower() in ['p', 'c']:
            for account in ActTable("customize.csv").iterator():
                account.load()
                if account.accessibility:
                    print("Welcome! " + account.name)
                    if self.timer == -1:
                        if input("Enter Y to stop:").lower() == 'y':
                            return
                    else:
                        print("refresh in " + str(self.timer) + " seconds...")
                        time.sleep(self.timer)
        else:
            for account in self._iterator():
                account.load()
                if account.accessibility:
                    print("Welcome! " + account.name)
                    if self.timer == -1:
                        if input("Enter Y to stop:").lower() == 'y':
                            return
                    else:
                        print("refresh in " + str(self.timer) + " seconds...")
                        time.sleep(self.timer)
        if self.timer == -1:
            input("accounts out")
        else:
            print("...another run...")
            self.active()

    def passive(self):
        for account in self._iterator():
            account.load()
            if account.accessibility:
                return
