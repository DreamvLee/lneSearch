from bs4 import BeautifulSoup
import ggSearch as ggs
from ggSearch import outcome
# 结果集拿出来


class BaiduSearch(ggs.GoogleSearch):
    # 根据google来改变,主要改变的是search找链接那一部分
    originUrl = 'https://www.baidu.com/s?wd='

    def __init__(self, location, key, driver=None):
        ggs.GoogleSearch.__init__(self,location, key, driver)

    def search(self, names):
        '''
                    百度搜索的结果(非广告):
                        class: c-container

                    link:
                        h3 -> a -> href
                        get_text 为title

                    describetion:
                        div class: c-abstract  内为描述
                '''
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
        gs = html.findAll('div', {'class': 'c-container'})
        print('共计： ', len(gs), '条搜索结果...')
        # 在google的搜索中，每条结果都是以class='g'来装饰
        # 但是在wikeBike 和图片链接中没有文字描述，因此在下面需要判断文字描述None
        for g in gs:
            # print(g)
            # print('-----------------------------------------')
            h3 = g.find('h3', {'class': 't'})
            if h3 is None:
                continue
            a = h3.find('a')
            title = a.get_text()
            # title = str(title).replace('\n', '')
            # print('title is : ', title.get_text())
            if a is not None:
                if 'href' in a.attrs:
                    link = self.getLink(url, a.attrs['href'])
                    # print(a.attrs['href'])
                else:
                    link = None
            else:
                link = None
            #####################找到title和link
            span = g.find('div', {'class': 'c-abstract'})
            if span is not None:
                description = span.get_text()
            else:
                description = None
            result = outcome(title, link, description)
            results.append(result)
        return results


def search(keys, driver):
    loc = 'Chrome所在的位置'
    baidu = BaiduSearch(loc, keys, driver)
    res = baidu.search(baidu.names)
    # baidu.close()
    for r in res:
        r.printItself()
    return res

if __name__ == '__main__':
    keys = {'女朋友很瘦是一种什么体验': 1}
    baidu = BaiduSearch('a', keys)
    res = baidu.search(baidu.names)
    for r in res:
        r.printItself()