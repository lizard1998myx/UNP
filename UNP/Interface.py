from UNP.IO import SearcherIO, LoginerIO
# from Core import Account


class Interface:
    def __init__(self):
        pass

    @staticmethod
    def info():
        info = "\n[University Network Project Interface]"
        return info

    @staticmethod
    def version():
        version = "V5.2.3 - 20190926"
        return version

    @staticmethod
    def history():
        history = """[Version history]
V0.1.0 (20181230) Searcher 1.0
V0.5.0 (20190103) Loginer  1.0
V0.6.0 (20190624) account data update
V1.0.0 (20190625) Combine Searcher and Loginer
V1.1.0 (20190625) Network tester
                  progression logger
                  visualized progression
V1.1.1 (20190625) Searcher 2.0 (traditional-mode)
V1.2.0 (20190625) Automode
V1.3.0 (20190626) CSV editor
V1.3.4 (20190626) command line interface
V2.0.0 (20190626) stable version
V2.1.0 (20190626) Searcher 2.2 (better search)
V2.2.2 (20190626) Automode update
V3.0.0 (20190626) Loginer  2.0 (new accounts)
                  silent and developer modes
V3.1.0 (20190626) Loginer  2.1 (customization)
V4.0.0 (20190627) Searcher 3.0 (password mode)
V4.0.3 (20190701) tester debug and icon
V4.1.0 (20190802) Loginer  3.0 (timer)
V5.0.0 (20190808) Object Oriented update
V5.2.0 (20190809) Searcher 5.0 (special modes)
                  error fix Core
V5.2.2 (20190828) bug fix
V5.2.3 (20190926) packed in package

[Incoming]
V5.3.0 (201909+) Manual control, multi-threading
"""
        return history

    def commandline(self):
        pass

    def keyboard(self):
        print(self.info())
        print(self.history())
        print(self.version())
        # Account.test()
        command = input("Chose mode (Login/Search)[default:L]: ")
        if command == "" or command.lower()[0] == 'l':
            LoginerIO.example()
        elif command.lower()[0] == 's':
            SearcherIO.example()
        input("exit!")


if __name__ == '__main__':
    Interface().keyboard()
