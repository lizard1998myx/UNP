import datetime
from Core import Account, ActTable
from Engineering import Searcher
from Application import Loginer


class SearcherIO(Searcher):
    @staticmethod
    def info():
        return "[SearcherIO]"

    @staticmethod
    def version():
        version = "V1.0 - 20190808"
        return version

    def echo(self):
        print("[Current setting]")
        print("mode: " + self.mode)
        print("start: " + str(self.start))
        print("end: " + str(self.end))
        print("string: " + self.string)
        print("list: " + str(self.list))

    def chmod(self):
        mode = input("Enter mode[" + self.mode + "]:")
        if mode != "":
            if mode[0].lower() == "p":
                self.mode = "password"
            if mode[0].lower() == "u":
                self.mode = "username"

    def chrange(self):
        start = input("Enter start[" + str(self.start) + "]:")
        end = input("Enter end[" + str(self.end) + "]:")
        if start != "":
            self.start = start
        if end != "":
            self.end = end

    def chstr(self):
        command = input("Enter string setting[" + self.string + "]:")
        if command == "":
            return
        elif command[0].lower() == "c": # 清空
            self.string = ""
            self.chstr()
        elif command[0].lower() == "r": # 重写
            self.string = input("Reset string :")
        elif command[0].lower() == "w": # 附上
            self.string = self.string + input("Append string:")
        else:
            self.string = ""
            if command[0] == '1': # 如果数字打开
                self.string = self.string + "0123456789"
            if command[1] == '1': # 如果小写打开
                self.string = self.string + "abcdefghijklmnopqrstuvwxyz"
            if command[2] == '1': # 如果大写打开
                self.string = self.string + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            if command[3] == '1': # 如果符号打开
                self.string = self.string + "`~!@#$%^&*()-=_+[]{}|;:,./<>?"
                # 去除了三个字符\\ ' "

    def chlist(self):
        command = input("Enter list setting"+ str(self.list) + ":")
        if command == "":
            return
        elif command[0] == "c": # 清空
            self.list = []
            self.chlist()
        else:
            while True:
                element = input("Append list element/Stop:")
                if element == "":
                    return
                else:
                    self.list.append(element)

    @staticmethod
    def example():
        searcher = SearcherIO()
        print(searcher.info())
        while True:
            searcher.chmod()
            searcher.chrange()
            searcher.chstr()
            searcher.chlist()
            searcher.echo()
            if input("Continue? (enter to go)") == '':
                searcher.search()
                print("Search complete!")
                return


class LoginerIO(Loginer):
    @staticmethod
    def info():
        info = "[Loginer]"
        return info

    @staticmethod
    def version():
        version = "V1.0 - 20190808"
        return version

    def echo(self):
        print("[Current setting]")
        print("mode: " + self.mode)
        print("timer: " + str(self.timer))
        print("file: " + self.file)

    def chmod(self):
        mode = input("Enter mode[" + self.mode + "]:")
        if mode != "":
            self.mode = mode

    def chtim(self):
        timer = input("Enter timer[" + str(self.timer) + "]:")
        if timer != "":
            timer = int(timer)
            if timer > 0:
                self.timer = timer

    @staticmethod
    def customizer():
        actt = ActTable("customize.csv")
        while True:
            username = input("Enter username/Stop:")
            password = input("Enter password/Stop:")
            if username == "" or password == "":
                return
            else:
                actt.record([username, password,
                             "Saved " + datetime.datetime.now().strftime('%Y-%m-%d')])

    @staticmethod
    def example():
        Account.test() # 使用account类进行网络测试
        loginer = LoginerIO()
        loginer.passive() # 使用被动模式进行一次登录
        print(loginer.info()) # 显示说明
        while True:
            loginer.chmod() # 设置模式
            loginer.chtim() # 设置循环时间
            loginer.echo()
            if input("Continue? (enter to go)") == '':
                if loginer.mode[0].lower in ['i', 's']:
                    loginer.customizer()
                else:
                    loginer.active()
                return


