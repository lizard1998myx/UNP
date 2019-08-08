import random, time
from Core import Account, ActTable


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
        userlist_201901 = [['ri', '李成日'], ['wsb', '留学生信息管理系'], ['wle', '魏兰娥'],
                           ['ybf', '严驳非'], ['czg', '崔志刚'], ['chl', '李长海'],
                           ['hjl', '胡珏'], ['zhn', '张宁'], ['qjp', '齐敬平'],
                           ['dsp', '杜少鹏'], ['zjq', '郑建全'], ['bbs', '学校BBS'],
                           ['jhs', '金树衡'], ['tzs', '田宗漱'], ['cjt', '唐翠菊'],
                           ['wdw', '王大伟'], ['gjx', '耿继秀'], ['huxa', '胡新爱'],
                           ['yqhe', '何亚庆'], ['zhgf', '周桂芳'], ['lvxf', '吕小凤'],
                           ['yuxg', '俞孝光'], ['wuzg', '武贞光'], ['hedh', '何东华'],
                           ['xudj', '徐德举'], ['lilj', '黎柳君'], ['guhm', '古怀民'],
                           ['gaom', '高明'], ['jcao', '曹洁'], ['xutr', '许庭瑞'],
                           ['xxjs', '王燕芳'], ['xyhu', '胡晓予'], ['jzhu', '朱剑'],
                           ['xkfw', '选课服务器'], ['lisw', '李纾维'], ['suhy', '苏洪玉'],
                           ['zpwy', '刘伟'], ['smxy', '生命学院'], ['wuzz', '吴宗舟'],
                           ['smhua', '华士鸣'], ['sunwb', '孙文博'], ['liujc', '刘建成'],
                           ['renlc', '任鲁川'], ['hanrc', '韩瑞财']]  # 最初筛选的安全账号，已经泄漏
        userlist_201906 = [['yy', '杨扬'], ['lee', '李竞瑜'], ['soe', 'Dr.SintSoe'],
                           ['lyh', '李永华'], ['rxj', '任希娟'], ['fyl', '费银玲'],
                           ['lgm', '刘功明'], ['tom', 'tom'], ['hzm', '侯贞梅'],
                           ['zwp', '赵卫平'], ['wrs', '李剑峰'], ['xut', '徐涛'],
                           ['jzx', '吉祖雄'], ['sgy', '四公寓'], ['bpma', '马丙鹏'],
                           ['maoj', '毛剑'], ['herj', '贺荣绵'], ['chun', 'CHUNJIANHO'],
                           ['zzqq', '周琴'], ['lxxy', '联想学院'], ['wuyy', '吴英毅'],
                           ['seema', 'SeemaMishira'], ['fanjb', '范静波'], ['guowb', '郭文兵'],
                           ['morse', 'Cameron']]  # 补充了一些账号，可能比较危险
        userlist_201907 = [["baixy", "白湘云"], ["chengdh", "程东华"], ["chenxl", "陈相龙"],
                           ["crzhang", "张串绒"], ["cxliu", "刘纯熙"], ["dbzheng", "郑大彬"],
                           ["dengzg", "邓祖淦"], ["dongcy", "董传仪"], ["dongyf", "董佑发"],
                           ["dongzg", "董志刚"], ["fmzhou", "周飞艨"], ["gaojs", "高建生"],
                           ["gengjy", "耿江元"], ["gfwei", "魏国锋"], ["ghxiong", "熊国华"],
                           ["ghzhou", "周国慧"], ["gnzhao", "赵歌喃"], ["goting", "龚婷"],
                           ["guanxh", "管旭红"], ["hines", "hines"], ["hliang", "梁华"],
                           ["hscong", "黄思聪"], ["huangye", "黄野"], ["jhong", "姜红"],
                           ["jhyang", "杨建华"], ["jiangrj", "姜汝俊"], ["jnpan", "潘结南"],
                           ["jstian", "田建生"], ["kqding", "丁克诠"], ["langyy", "郎蕴瑛"],
                           ["lcyang", "李朝阳"], ["liugt", "刘功田"], ["liuxh", "刘小惠"],
                           ["lszhou", "周连生"], ["lxgui", "李新贵"], ["lxliu", "刘利新"],
                           ["maojw", "毛建文"], ["maosp", "毛士鹏"], ["mengyx", "孟艳霞"],
                           ["panjl", "潘建林"], ["panxp", "潘辛平"], ["qianxb", "钱秀斌"],
                           ["rwzhang", "张仁武"], ["tjhuang", "黄铁军"], ["twchen", "twchen"],
                           ["twchiang", "twchiang"], ["twchou", "twchou"], ["twlin", "twlin"],
                           ["wangwx", "王文新"], ["xfang", "方锡生"], ["xfwang", "王小芬"],
                           ["xfzhao", "赵险峰"], ["xiangnz", "向南宗"], ["xlzhang", "张兴兰"],
                           ["xyliu", "刘新彦"], ["yaoym", "姚英明"], ["yhzhang", "张亚红"],
                           ["yinxz", "尹新征"], ["yjzhou", "周玉洁"], ["ylhou", "侯彦林"],
                           ["yqzhao", "赵亚群"], ["yschen", "陈一帅"], ["yzzhao", "赵袆喆"],
                           ["zbsun", "孙正滨"], ["zddai", "戴宗铎"], ["zdzhang", "张正东"],
                           ["zengxq", "曾小青"], ["zhanglp", "章丽萍"], ["zhangyc", "张彦春"],
                           ["zhangyk", "张钰坤"], ["zhouwy", "周文源"], ["zhuxq", "朱兴全"]]  # 新版更新的账号

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