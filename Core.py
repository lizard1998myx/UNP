import requests, sys, csv


class Account:
    def __init__(self, username, password="ucas", name=None):
        self.username = str(username)
        self.password = str(password)
        self.accessibility = False
        self.situation = False
        self.description = "Initialized"
        self._resp = None
        if name is None:
            self.name = self.username
        else:
            self.name = str(name)

    def __str__(self):
        return self.name + " " + self.description

    def set(self, username, password="ucas", name=None):
        self.__init__(username, password, name)

    def _getresp(self):
        sys.setrecursionlimit(1000000000)
        ReqHead = {
            'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.8, ja; q=0.7, en-US; q=0.5, en; q=0.3, ru; q=0.2',
            'Cache-Control': 'max-age=0',
            'Connection': 'Keep-Alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': '210.77.16.21',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763'
        }
        ChkUrl = 'http://210.77.16.21/eportal/InterFace.do?method=login'  # 登录表单提交
        CisUrl = 'http://210.77.16.21:8080/eportal/interface/index_files/pc/portal.png'  # 用于获取Cookies
        ReqData = {
            'password': self.password,
            'passwordEncrypt': 'false',
            'userId': self.username,
            'queryString': 'wlanuserip%253D0bc386d9e643d188b011a0d00c9b5c40%2526wlanacname%253D5fcbc245a7ffdfa4%2526ssid%253D%2526nasip%253D2c0716b583c8ac3cbd7567a84cfde5a8%2526mac%253D53ba540bde596b811a6d5617a86fa028%2526t%253Dwireless-v2%2526url%253D2c0328164651e2b4f13b933ddf36628bea622dedcc302b30',
        }
        Cis = requests.get(CisUrl)
        Resp = requests.post(ChkUrl, headers=ReqHead, cookies=requests.utils.dict_from_cookiejar(Cis.cookies),
                             data=ReqData)  # 提交登陆表单，并获取返回值
        self._resp = Resp

    @staticmethod
    def quit():
        sys.setrecursionlimit(1000000000)
        ReqHead = {
            'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.8, ja; q=0.7, en-US; q=0.5, en; q=0.3, ru; q=0.2',
            'Cache-Control': 'max-age=0',
            'Connection': 'Keep-Alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': '210.77.16.21',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763'
        }
        ChkUrl = 'http://210.77.16.21/eportal/InterFace.do?method=login'  # 登录表单提交
        CisUrl = 'http://210.77.16.21:8080/eportal/interface/index_files/pc/portal.png'  # 用于获取Cookies
        OutUrl = 'http://210.77.16.21/eportal/InterFace.do?method=logout'  # 成功后登出以便下一次尝试
        ReqData = {
            'password': 'password',
            'passwordEncrypt': 'false',
            'userId': 'username',
            'queryString': 'wlanuserip%253D0bc386d9e643d188b011a0d00c9b5c40%2526wlanacname%253D5fcbc245a7ffdfa4%2526ssid%253D%2526nasip%253D2c0716b583c8ac3cbd7567a84cfde5a8%2526mac%253D53ba540bde596b811a6d5617a86fa028%2526t%253Dwireless-v2%2526url%253D2c0328164651e2b4f13b933ddf36628bea622dedcc302b30',
        }
        Cis = requests.get(CisUrl)
        Resp = requests.post(ChkUrl, headers=ReqHead, cookies=requests.utils.dict_from_cookiejar(Cis.cookies),
                             data=ReqData)  # 提交登陆表单，并获取返回值
        End = Resp.text.find('\",\"result')
        ReqData = {
            'userIndex': str(Resp.text)[14:End],  # 将用户ID填入表单
        }
        requests.post(OutUrl, headers=ReqHead, cookies=requests.utils.dict_from_cookiejar(Cis.cookies),
                      data=ReqData)  # 提交登出表单

    @staticmethod
    def test():
        ac1 = Account("sb")
        ac1.load()
        ac2 = Account("gl")
        ac2.load()
        if ac1.description == "Not Exist" and ac2.description == "Pwd Wrong":
            return True
        else:
            return False

    def load(self):
        try:
            self._getresp()
        except ConnectionError:
            self.load()
        if self._resp.text.find('success') != -1:  # 如果登录成功
            if self._resp.text.find('å½åå·²ç¨(') != -1:  # 如果已有账号登录
                Account.quit()
                self.load()
            else: # 真的成功
                self.accessibility=True
                self.situation=True
                self.description='OK'
        elif self._resp.text.find('fail') != -1:  # 如果登录失败
            if self._resp.text.find('æ å¯ç¨å©ä½æµé!') != -1:  # 如果没有流量剩余
                self.situation=True
                self.description="Data Out"
            elif self._resp.text.find('ç¨æ·ä¸å­å¨,è¯·è¾å¥æ­£ç¡®çç¨æ·å!') != -1:  # 如果账号不存在
                self.situation=False
                self.description="Not Exist"
            elif self._resp.text.find('å¯ç ä¸å¹é,è¯·è¾å¥æ­£ç¡®çå¯ç !') != -1:  # 如果密码错误
                self.situation=True
                self.description="Pwd Wrong"
            else:
                self.situation=False
                self.description="Unknown" # + str(self._resp.text)


class ActTable:
    def __init__(self, filename):
        self.filename = str(filename)
        try:
            with open(self.filename, 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['username', 'password', 'note'])
        except IOError:
            pass # 文件已存在时，不进行初始化

    def record(self, account):
        if account is Account:
            username = account.username
            password = account.password
            note = account.description
        elif account is list:
            username = account[0]
            password = account[1]
            note = account[2]
        with open(self.filename, 'a') as csvfile:
            filenames = ['username', 'password', 'note']
            writer = csv.DictWriter(csvfile, fieldnames=filenames)
            writer.writerow({'username': username,
                             'password': password,
                             'note': note})

    @staticmethod
    def combine(inputlist, outputname):
        if outputname == "":
            outputname = "output.csv"
        output = ActTable(outputname)
        for inputfile in inputlist:
            print("LOADING...")
            with open(inputfile, 'r') as csvfile:
                reader = csv.reader(csvfile)  # 获得输入表数据
                for data in reader:  # 逐行读取载入数据
                    if len(data) >= 3:
                        print(data)
                        if data[2] in ['OK', 'Data Out']:
                            output.record(data)
            print("LOADED (" + inputfile + ")")
        input("Combine DONE!")

    def iterator(self):
        with open(self.filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for data in reader:
                if len(data) >= 3:
                    if data[0] != 'username':  # 跳过第一行
                        yield Account(username=data[0], password=data[1])

    @staticmethod
    def example():
        outputname = input("Enter output filename:")
        inputlist = []
        while True:
            inputname = input("Enter input/Stop:")
            if inputname != "":
                inputlist.append(inputname)
            else:
                ActTable.combine(inputlist, outputname)