from bs4 import BeautifulSoup
import ggSearch as ggs
from ggSearch import outcome
# 结果集拿出来


# three six zero
class threeSixZeroSearch(ggs.GoogleSearch):
    originUrl = 'https://www.so.com/s?q='

    def __init__(self, location, key, driver=None):
        ggs.GoogleSearch.__init__(self,location, key, driver)

    def search(self, names):
        '''
                    360搜索的结果(非广告):
                      li   class: res-list

                    link:
                       li h3 class: res-title -> a -> href
                    title:
                      li h3 -> a get_text()
                    describetion:
                        li  p class: res-desc  内为描述
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
        gs = html.findAll('li', {'class': 'res-list'})
        print('共计： ', len(gs), '条搜索结果...')
        # 在google的搜索中，每条结果都是以class='g'来装饰
        # 但是在wikeBike 和图片链接中没有文字描述，因此在下面需要判断文字描述None
        for g in gs:
            # print(g)
            # print('-----------------------------------------')
            # h3 = g.find('h3', {'class': 'res-title'})
            h3 = g.find('h3')
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
    tsx = threeSixZeroSearch(loc, keys, driver)
    res = tsx.search(tsx.names)
    # tsx.close()
    for r in res:
        r.printItself()
    return res

if __name__ == '__main__':
    keys = {'360好不好用': 1}
    tsx = threeSixZeroSearch('a', keys)
    res = tsx.search(tsx.names)
    for r in res:
        r.printItself()