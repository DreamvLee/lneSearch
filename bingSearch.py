from bs4 import BeautifulSoup
import ggSearch as ggs
from ggSearch import outcome
# 结果集拿出来


# three six zero
class bSearch(ggs.GoogleSearch):
    originUrl = 'https://cn.bing.com/search?q='
    # &ensearch=1   结尾加上则为国际版，将1->2则为国内版

    def __init__(self, location, key, driver=None):
        ggs.GoogleSearch.__init__(self,location, key, driver)

    def search(self, names):
        '''
                    bing搜索的结果(国际版,去除了大部分广告):
                      li   class: b_algo

                    link:
                       li h2  a -> href
                    title:
                      li h2 -> a get_text()
                    describetion:
                        li  p   内为描述
                '''
        results = []
        url = self.originUrl
        cur = 1
        for name in names:
            url += name
            if cur < len(names):
                cur += 1
                url += '+'
        url += '&ensearch=1'
        # 将关键字键入链接内搜索
        driver = self.driver
        driver.get(url)
        html = BeautifulSoup(driver.page_source, 'html.parser')
        gs = html.findAll('li', {'class': 'b_algo'})
        print('共计： ', len(gs), '条搜索结果...')
        # 在google的搜索中，每条结果都是以class='g'来装饰
        # 但是在wikeBike 和图片链接中没有文字描述，因此在下面需要判断文字描述None
        for g in gs:
            # print(g)
            # print('-----------------------------------------')
            # h3 = g.find('h3', {'class': 'res-title'})
            h3 = g.find('h2')
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
            # span = g.find('p', {'class': 'res-desc'})
            span = g.find('p')
            if span is not None:
                description = span.get_text()
            else:
                description = None
            result = outcome(title, link, description)
            results.append(result)
        return results

def search(keys, driver):
    loc = 'Chrome所在的位置'
    bing = bSearch('a', keys, driver)
    res = bing.search(bing.names)
    # bing.close()
    for r in res:
        r.printItself()
    return res

if __name__ == '__main__':
    keys = {'手机': 1}
    bing = bSearch('a', keys)
    res = bing.search(bing.names)
    for r in res:
        r.printItself()