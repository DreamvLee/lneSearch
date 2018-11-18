from bs4 import BeautifulSoup
import useChrom
from urllib.parse import urlparse
import UseSS as ss


class FError(Exception):
    pass


class outcome:
    def __init__(self, title, link, description):
        self.title = title
        self.link = link
        self.description = description

    def printItself(self):
        print('title is : ', self.title)
        print('link is : ', self.link)
        print('description is : ', self.description)
        print()


class GoogleSearch:
    originUrl = 'https://www.google.com/search?q='
    key = []

    def sort(self, names, weights):
        if len(names) < 2:
            return names, weights
        for i in range(0, len(weights)):
            for j in range(i + 1, len(weights)):
                if weights[i] < weights[j]:
                    temp = weights[i]
                    weights[i] = weights[j]
                    weights[j] = temp
                    temp = names[i]
                    names[i] = names[j]
                    names[j] = temp
        for i in names:
            print(i)
        return names, weights

    # 传入键值和权重，默认都为1，权重目前由在网页出现的词频来判断
    def __init__(self, location, key, driver=None):
        self.names = []
        self.weights = []
        for name, weight in key.items():
            self.names.append(name)
            self.weights.append(weight)
        self.names, self.weights = self.sort(self.names, self.weights)
        # 将名和权重排好序
        self.location = location
        chrome = useChrom.UseChrome(self.location)
        # 传入浏览器的路径
        # self.driver = chrome.setDriver()
        # 设置浏览器
        if driver is None:
            self.location = location
            chrome = useChrom.UseChrome(self.location)
            # 传入浏览器的路径
            self.driver = chrome.setDriver()
            # 设置浏览器
        else:
            self.driver = driver


    def prevent(self):
        print('输入任意退出...')
        a = str(input())
        print(a, '退出了...')

    # 将内链和外链全部成外链
    def getLink(self, comeFrom, to):
        if to.startswith('http'):
            link = to
        else:
            comeFrom = urlparse(comeFrom).scheme + '://' + urlparse(comeFrom).netloc
            # 解析内链
            link = comeFrom + to
        return link

    def search(self, names):
        results = []
        url = self.originUrl
        cur = 1
        for name in names:
            url += name
            if cur < len(names):
                cur += 1
                url += '+'
        # 将关键字键入链接内搜索
        driver = self.driver
        driver.get(url)
        html = BeautifulSoup(driver.page_source, 'html.parser')
        gs = html.findAll('div', {'class': 'g'})
        print('共计： ', len(gs), '条搜索结果...')
        # 在google的搜索中，每条结果都是以class='g'来装饰
        # 但是在wikeBike 和图片链接中没有文字描述，因此在下面需要判断文字描述None
        for g in gs:
            try:
                h3 = g.find('h3')
                if h3 is None:
                    continue
                title = h3.get_text()
                # print('title is : ', title.get_text())
                a = h3.find('a')
                if a is not None:
                    if 'href' in a.attrs:
                        link = self.getLink(url, a.attrs['href'])
                        # print(a.attrs['href'])
                    else:
                        link = None
                else:
                    link = None
                span = g.find('span', {'class': 'st'})
                if span is not None:
                    description = span.get_text()
                else:
                    description = None
                result = outcome(title, link, description)
                results.append(result)
            except FError as e:
                print('啊偶，出错了')
        return results


    def close(self):
        self.driver.quit()


# 返回的是结果的链接---title link description
def search(keys, driver):
    # ss.UseDefaultShadowsock()
    loc = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    # 目前调用的是环境变量的Chrome，届时还需调整
    # driver = useChrom.defaultUse()
    googleSearch = GoogleSearch(loc, keys, driver)
    results = googleSearch.search(googleSearch.names)
    # googleSearch.close()
    for result in results:
        result.printItself()
    # ss.closeShadowsocks()
    return results


if __name__ == '__main__':
    keys = {'女朋友很瘦是一种什么体验': 1}
    loc = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    # 记住,需要传入Chrome的路径,目前一切默认
    results = search(keys)
    # googleSearch = GoogleSearch(loc, key)
    # results = googleSearch.search(googleSearch.names)
    # googleSearch.close()
    # for result in results:
    #     result.printItself()

# url = 'https://www.google.com/search?q='
# loc = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
# keyOne = str(input())
# keyTwo = str(input())
# keyThree = str(input())
# url = url + keyOne + '+' + keyTwo + '+' + keyThree
