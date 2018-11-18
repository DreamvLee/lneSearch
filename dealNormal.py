import lneSearch
import configparser

class dnm:
    def __init__(self):
        self.lne = lneSearch.lneS()
        self.configLocation = 'spider.conf'
        self.dealUrlCf = 'dealurl'
        self.webdriverCf = 'webDriver'
        pass

    def getConfig(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(self.configLocation)
        return self.cf

    def isAnalysisEveryPage(self):
        self.getConfig()
        if self.cf.get('normalsetting', 'analyzeallpage') == 'True':
            print('conf被设置为分析每一页面')
            return True
        else:
            print('conf未被设置为分析每一页面')
            return False

    def start(self, *params, **dparams):
        names = ['isUseGoogle', 'isUseBaiDu', 'isUseBing', 'isUseTsz',
                 'isGetPic', 'isGetTxt', 'isGetLink',
                 'keyWords', 'weights', 'weightLike', 'outcomeCount', 'path']

        param = {'isUseGoogle': False, 'isUseBaiDu': False, 'isUseBing': False, 'isUseTsz': False,
                 'isGetPic': False, 'isGetTxt': False, 'isGetLink': False, 'keyWords': None,
                 'weights': None, 'weightLike': None, 'outcomeCount': None, 'path': None}

        for i in range(0, len(params)):
            param[names[i]] = params[i]

        for name, value in dparams.items():
            param[name] = value

        self.isGetPic = param['isGetPic']
        self.isGetTxt = param['isGetTxt']
        self.isGetLink = param['isGetLink']
        self.downloadLoc = param['path']

        webdriver = None
        keys = {}
        # 将其转变为map
        for i in range(0, len(param['keyWords'])):
            keys[param['keyWords'][i]] = param['weights'][i]
            print(param['keyWords'][i])

        self.lne.search(keys, webdriver, param['isUseGoogle'],
                        param['isUseBaiDu'], param['isUseBing'], param['isUseTsz'],
                        param['outcomeCount'], param['weightLike'])

        self.lne.wipe(self.lne.resultss)
        self.outcomes = self.lne.outcomes
        # 结果，是ggSearch的outcome类
        print('over!')
        return self.outcomes

    # 逐页分析
    def analysisAllPage(self):
        if self.isAnalysisEveryPage() is True:
            interval = int(self.cf.get(self.dealUrlCf, 'interval'))
            slideTime = int(self.cf.get(self.dealUrlCf, 'slidetime'))

            if self.downloadLoc is None:
                downloadLoc = self.cf.get(self.webdriverCf, 'downloadlocation')
            else:
                downloadLoc = self.downloadLoc
            self.lne.analysisEveryPage(self.isGetPic, None, interval, slideTime,
                                       downloadLoc, self.isGetTxt, self.isGetLink)

if __name__ == '__main__':
    d = dnm()