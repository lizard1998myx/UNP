import sys, datetime
from Core import Account, ActTable


class Searcher:
    def __init__(self, mode="username", start=0, end=100,
                 string="abcdefghijklmnopqrstuvwxyz", list=['ucas']):
        self.mode = str(mode)
        self.start = int(start)
        self.end = int(end)
        self.string = str(string)
        self.list = list
        self._username = ""
        self._password = ""

    def __str__(self):
        string = "mode-" + self.mode + "_between-" + str(self.start) + "-" + str(self.end)
        if self.string != "":
            string = string + "_string-" + self.string
        if self.list != ['ucas']:
            string = string + "_list-" + str(self.list)
        return string

    def reset(self, mode="username", start=0, end=100,
              string="abcdefghijklmnopqrstuvwxyz", list=['ucas']):
        self.__init__(self, mode=mode, start=start, end=end, string=string, list=list)

    @staticmethod
    def percentage(now, all, tip="Progress: ", info=" "):
        now = now + 1
        percent = 1.0 * int(now) / int(all)
        sys.stdout.write("\r{0}{1}{2}{3}".format(tip,
                                                 "|" * int(percent // 0.05),
                                                 '%.2f%%' % (percent * 100),
                                                 " (" + info + ")"))
        sys.stdout.flush()

    @staticmethod
    def generator(n, charlist):
        base = len(charlist)
        string = ""
        while n != 0:
            string = charlist[n % base] + string
            n = n // base
        return string

    def search(self):
        if self.mode == "username":
            for password in self.list:
                self._password = password
                self.run()
        if self.mode == "password":
            for username in self.list:
                self._username = username
                self.run()

    def run(self):
        filename = 'Record_' + str(self) + '_' + \
                   datetime.datetime.now().strftime('%Y-%m-%d-%H-%M') + '.csv'
        actt = ActTable(filename)
        for [now, account] in self.iterator():
            account.load()
            Searcher.percentage(now, self.end-self.start, info=str(account))
            if self.mode == "username":
                if account.situation:
                    actt.record(account)
                    print('\nSuccess! '+ account.username + "|" + account.password)
            if self.mode == "password":
                if account.accessibility:
                    actt.record(account)
                    print('\nSuccess! ' + account.username + "|" + account.password)
                    return
            actt.record(account) # 失败记录

    def iterator(self):
        if self.mode == "username":
            password = self._password
            for now in range(self.start, self.end):
                username = self.generator(now, '\n'+self.string)
                if '\n' not in username and username != "":
                    yield [now, Account(username, password=password)]
        elif self.mode == "password":
            username = self._username
            for now in range(self.start, self.end):
                password = self.generator(now, '\n'+self.string)
                if '\n' not in password and password != "":
                    yield [now, Account(username, password=password)]