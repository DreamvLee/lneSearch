import configparser


class wrtcfg:
    def __init__(self):
        self.configLocation = 'spider.conf'
        pass

    def doWrite(self, cf):
        with open(self.configLocation, 'w+') as f:
            cf.write(f)
        print('修改config配置成功！')

    def getConfig(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(self.configLocation)
        return self.cf

    def writeAbout(self):
        people = {'team': '鸣谢', 'teamname': ' @103',
                  'teacher': '指导', 'teachername': '谭云兰',
                  'developer': '工程', 'developername': '姜璐聪',
                  'designer': '设计', 'designername': '钟雨',
                  'teller': '说明', 'tellername': '娄欢',
                  'tester': '测试', 'testername': '李跃洪',
                  'king': '酱油哥', 'kingname': 'lne',
                  'queue': '酱油姐', 'queuename': 'terri',
                  'massage': ' ', 'massagename': '感谢每一位大佬的辛勤付出'}

        cf = self.getConfig()
        for name, value in people.items():
            cf.set('about', name, value)
        self.doWrite(cf)

    def getAbout(self):
        cf = self.getConfig()
        opts = cf.options('about')
        for opt in opts:
            info = opt + ' : ' + cf.get('about', opt)
            print(info)

    def getAboutn(self):
        cf = self.getConfig()
        opts = cf.options('aboutn')
        for opt in opts:
            name = cf.get('aboutn', opt)
            info = cf.get('about', name) + ':' + cf.get('about', name + 'name')
            print(info)

if __name__ == '__main__':
    wc = wrtcfg()
    wc.writeAbout()
    # wc.getAbout()
    wc.getAboutn()