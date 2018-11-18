# this is made by lne
import ggSearch
import bdSearch
import tszSearch
import bingSearch
import useChrom
import anlsPage
import configparser
import dealUrl

class lneS:
    def __init__(self):
        self.resultss = None
        self.outcomes = None
        self.configLocation = 'spider.conf'
        pass

    def isIntelligentSort(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(self.configLocation)
        if self.cf.get('normalsetting', 'intelligentsort') == 'True':
            print('使用智能排序')
            return True
        else:
            print('不使用智能排序')
            return False

    def analysisEveryPage(self,isGetPic, picCount, interval, slideTime,
                            downloadLoc, isGetText, isGetLink):
        print('开始分析每一页面')
        du = dealUrl.durl()
        for ot in self.outcomes:
            du.start(ot.link, isGetPic, picCount, interval, slideTime,
                     downloadLoc, isGetText, isGetLink)

    def search(self, *params, **sparams):
        self.resultss = []
        names = ['keys', 'webdriver', 'isUseGoogle', 'isUseBaiDu', 'isUseBing', 'isUseTsz',
                 'outcomeCount', 'weightLike']
        param = {'keys': None, 'webdriver': None,
                'isUseGoogle': None, 'isUseBaiDu': None, 'isUseBing': None, 'isUseTsz': None,
                 'outcomeCount': None, 'weightLike': None}

        self.searchCount = 0

        for i in range(0, len(params)):
            param[names[i]] = params[i]
            if i > 1 and params[i] is True:
                self.searchCount += 1

        for name, value in sparams.items():
            param[name] = value

        self.averageCount = param['outcomeCount'] / self.searchCount
        self.allCount = param['outcomeCount']

        driver = None
        keys = param['keys']
        print(keys)
        if param['webdriver'] is None:
            driver = useChrom.defaultUse()
        else:
            driver = param['webdriver']

        if param['isUseGoogle'] is True:
            print('google:')
            self.resultss.append(ggSearch.search(keys, driver))

        if param['isUseBaiDu'] is True:
            print('baidu:')
            self.resultss.append(bdSearch.search(keys, driver))

        if param['isUseBing'] is True:
            print('Bing:')
            self.resultss.append(bingSearch.search(keys, driver))

        if param['isUseTsz'] is True:
            print('360:')
            self.resultss.append(tszSearch.search(keys, driver))

        driver.quit()

        # 先按照结果的要求排序并数量要求
        return self.resultss

    def wipe(self, resultss):
        self.outcomes = []
        links = set()
        if self.isIntelligentSort() is False:
            for results in resultss:
                count = self.averageCount
                # 每种引擎的平均条数
                for result in results:
                    link = result.link
                    if link not in links and count > 0:
                        links.add(link)
                        self.outcomes.append(result)
                        count -= 1
        else:
            # 智能排序处理一下
            current = 0
            i = 0
            while i < self.allCount:
                for results in resultss:
                    # 如果当前大于结果数量，则跳过
                    if current >= len(results):
                        i += 1
                        continue
                    link = results[current].link
                    if link not in links:
                        i += 1
                        links.add(link)
                        self.outcomes.append(results[current])
                current += 1
        return self.outcomes


def lneSearch(keys, webdriver = None):
    resultss = []
    driver = None
    if webdriver is None:
        driver = useChrom.defaultUse()
    else:
        driver = webdriver
    print('google:')
    # resultss.append(ggSearch.search(keys, driver))
    print('baidu:')
    resultss.append(bdSearch.search(keys, driver))
    print('360:')
    resultss.append(tszSearch.search(keys, driver))
    print('Bing:')
    resultss.append(bingSearch.search(keys, driver))
    # driver.quit()
    return resultss

# 去除重复的链接
def wipe(resultss):
    outcomes = []
    links = set()
    for results in resultss:
        for result in results:
            link = result.link
            if link not in links:
                links.add(link)
                outcomes.append(result)
    return outcomes


if __name__ == '__main__':
    keys = {'水稻': '1'}
    driver = useChrom.defaultUse()
    resultss = lneSearch(keys, driver)
    outcomes = wipe(resultss)
    address = 'D:\\Computer\\Desk\\test\\20180908'
    # 清洗效果似乎不太好，因为搜索出来的网站会在后面提交很多参数，导至无法去重
    i = 0
    for outcome in outcomes:
        loc = address + '\\' + str(i)
        link = outcome.link
        anlsPage.analysisDefault(link, loc, driver)
        i += 1