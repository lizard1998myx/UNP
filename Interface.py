from IO import SearcherIO, LoginerIO
from Core import Account

class Interface:
    def __init__(self):
        pass

    @staticmethod
    def info():
        info = "[University Network Project Interface]"
        return info

    @staticmethod
    def version():
        version = "V5.1 - 20190808"
        return version

    @staticmethod
    def history():
        history = """[Version history]
V0.10 (20181230) Searcher 1.0
V0.50 (20190103) Loginer  1.0
V0.60 (20190624) account data update
V1.00 (20190625) Combine Searcher and Loginer
V1.10 (20190625) Network tester
                 progression logger
                 visualized progression
V1.11 (20190625) Searcher 2.0 (traditional-mode)
V1.20 (20190625) Automode
V1.30 (20190626) CSV editor
V1.34 (20190626) command line interface
V2.00 (20190626) stable version
V2.10 (20190626) Searcher 2.2 (better search)
V2.22 (20190626) Automode update
V3.00 (20190626) Loginer  2.0 (new accounts)
                 silent and developer modes
V3.10 (20190626) Loginer  2.1 (customization)
V4.00 (20190627) Searcher 3.0 (password mode)
V4.03 (20190701) tester debug and icon
V4.10 (20190802) Loginer  3.0 (timer)
V5.00 (20190808) Object Oriented update
V5.20 (20190809) Searcher 5.0 (special modes)
                 error fix Core
"""
        return history

    def commandline(self):
        pass

    def keyboard(self):
        print(self.info())
        print(self.history())
        print(self.version())
        Account.test()
        if input("into Loginer? (enter to skip):") != "":
            LoginerIO.example()
        if input("into Searcher? (enter to skip):") != "":
            SearcherIO.example()
        input("exit!")


Interface().keyboard()
