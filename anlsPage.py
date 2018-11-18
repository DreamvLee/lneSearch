import ggSearch as ggs
import useChrom
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from urllib.parse import urlparse, quote
from urllib import error
import urllib
import os
import time
import re
import base64
import io
import random
import socket
import datetime
from urllib3.exceptions import ReadTimeoutError
from tkinter import messagebox as mBox

class FError(Exception):
    pass

class ParamsError(Exception):
    def __init__(self, name):
        print(name, '--该参数在模块内部没有定义！')


class ParamsNotFilledError(Exception):
    def __init__(self):
        print('存在未填写的参数')
        mBox.showerror('错误', '存在未填写的参数')


class analysisPage:
    # 初始化,webdriver,下载处，初始链接
    # def __init__(self, driver, link, downloadLocation):
    def __init__(self, driver, *params, **aparams):
        self.names = ['url', 'isGetPic', 'piCount', 'interval', 'slideTime',
                'downloadLoc', 'isGetText', 'isGetLink', 'cookie']
        self.param = {'url': None, 'isGetPic': None, 'piCount': None, 'interval': None, 'slideTime': None,
                 'downloadLoc': None, 'isGetText': None, 'isGetLink': None, 'cookie': None}
        self.driver = driver

        for i in range(0, len(params)):
            self.param[self.names[i]] = params[i]

        for name, value in aparams.items():
            if name not in self.names:
                raise ParamsError(name)
            self.param[name] = value
        print(self.param)

        self.link = self.param['url']
        self.isGetPic = self.param['isGetLink']
        self.piCount = self.param['piCount']
        self.interval = self.param['interval']
        self.slideTime = self.param['slideTime']
        self.downloadLocation = self.param['downloadLoc']
        self.isGetText = self.param['isGetText']
        self.isGetLink = self.param['isGetLink']
        self.cookie = self.param['cookie']

        self.bsObj = None
        self.text = None
        self.links = None
        # 分别代表bsObj,文本，链接，如果是相同下原链接，则不用再分析，如果是不同的，则需要再分析
        self.mkDir(self.downloadLocation)
        # 制作该目录

    def showWarning(self, massage, title='警告'):
        mBox.showwarning(title, massage)

    def showError(self, massage, title='错误'):
        mBox.showerror(title, massage)

    def showInof(self, massage, title='通知'):
        mBox.showinfo(title, massage)

    # 默认对一个网页进行操作,获取网页链接，获取文本，获取图片
    def defaultDeal(self):
        print('正在进行默认处理...')
        text = self.getText(self.link)
        if self.bsObj is None:
            massage = '该网页似乎有一些问题我无法处理...'
            print('该网页似乎有一些问题我无法处理...尝试跳过')
            print('网址是：', self.link)
            self.showError(massage=massage)
            return None

        if self.isGetText is True:
            self.writeFile(self.downloadLocation, 'text', text)
            print('文本处理完成...')
            # 写入对应目录，并命名为文本

        if self.isGetLink is True:
            links = self.getLinks(self.link)
            slinks = '\n'.join(links)
            self.writeFile(self.downloadLocation, 'links', slinks)
            print('链接处理完成...')
            # 将链接也写入文本内，命名为链接

        if self.isGetPic is True:
            picLoc = self.downloadLocation + '\\' + 'picture'
            self.mkDir(picLoc)
            self.getPicture(self.link, picLoc)
            print('图片处理完成...该页面已分析完毕')
            # 建立子文件夹存图片

        massage = '已全部处理完成！'
        print(massage)
        self.showInof(massage=massage)


    # 在转一些链接的时候，需要处理一些特殊符号
    def quoteLink(self, link):
        link = quote(link)
        link = link.replace('%3A', ':')
        link = link.replace('%25', '%')
        link = link.replace('%3F', '?')
        link = link.replace('%3D', '=')
        link = link.replace('%2C', ',')
        link = link.replace('%26', '&')
        return link

    # 拖动滑动条，达成滑动该页面，处理哪些定时加载的
    def slideDown(self, count):
        for i in range(0, count):
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(3)
            print('滑动一下...第', i, '次...共计', count, '次')
        # 滑动五次，然后再解析网页，


    # 如果是第一次运行,或者是新链接
    def getBsobj(self, link):
        flag = False
        if self.bsObj is None or self.link != link:
            self.link = link
            try:
                self.driver.get(link)
            except ReadTimeoutError:
                print('该网页无法打开...')
                flag = True
                pass
            if flag is True:
                return None
            # 如果超过预定时间还没有加载完,则默认打不开...此处有一些问题，在挂木弟子的时候
            self.slideDown(self.slideTime)
            time.sleep(2)
            html = self.driver.page_source
            self.bsObj = BeautifulSoup(html, 'html.parser')
        return self.bsObj

    # 获取页面文本，存下到记事本中
    def getText(self, link):
        print('获取文本...')
        # self.driver.get(link)
        # page = self.driver.page_source
        # # print(page)
        # # print('----------------')
        # html = BeautifulSoup(page, 'html.parser')
        html = self.getBsobj(link)
        # 直接获取
        if html is None:
            return None
        for script in html(["script", "style"]):
            script.extract()
            # rip it out
        text = html.get_text()
        # text = text.replace('\n', '')
        text = re.sub(r'[\n]+', r'\n', text, flags=re.S)
        # 使用正则，将多个换行替换成一个
        # print(text)
        self.text = text
        # self.writeFile(location, 'page', text)
        # 将文本存入该路径下，并命名为page
        return text

    def getAbsoluteURL(self, baseUrl, source):
        baseUrl = urlparse(baseUrl).scheme + '://' + urlparse(baseUrl).netloc
        # 先转化为基链
        if source.startswith('http://www.'):
            url = 'http://' + source[11:]
        elif source.startswith('http://') or source.startswith('https://'):
            url = source
        elif source.startswith('www.'):
            url = 'http://' + source[4:]
        elif source.startswith('//'):
            url = 'http:' + source
        elif source.startswith('/'):
            url = baseUrl + source
        elif source.startswith('data:image'):
            return source
        else:
            url = baseUrl + '/' + source
        return url

    # 增加一个判断，
    def getKind(self, link):
        reg = '\.(...?)'
        kinds = re.findall(reg, link)
        # 只取.后面三个字符
        if len(kinds) > 0:
            kind = '.' + kinds[len(kinds) - 1]
            if kind == '.com':
                kind = '.jpg'
            # 如果他只是一个网址，则默认为jpg格式图片
            return kind
        else:
            return False

    # data开头的则需要用bs64进行解码
    def bs64ToPic(self, code, location):
        flag = re.compile('data:.*base64,')
        code = flag.sub('', code)
        # print(code)
        pic = base64.b64decode(code)
        file = open(location, 'wb')
        file.write(pic)
        file.close()

    # 如果是bs64类型的图片，则返回图片类型，否则，False，不是该类型图片
    def getKindBs64(self, link):
        reg = 'data:image/(.*);base64'
        if link.startswith('data:image'):
            kinds = re.findall(reg, link)
            if len(kinds) > 0:
                kind = '.' + kinds[0]
                return kind
        else:
            return False

    def wait(self):
        min = int(self.interval // 2)
        max = int(self.interval * 1.5)
        t = random.randint(min, max)
        print('等待时间为：', t, 'S')
        time.sleep(t)

    # 获取页面所有图片,填入链接，下载地址，以及下拉次数

    def getPicture(self, link, downloadLocation):
        links = set()
        picLinks = []
        linkToId = {}
        # driver = self.driver
        # driver.get(link)
        # # 转到该网页
        # for i in range(0, count):
        #     time.sleep(3)
        #     driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        # # 滑动五次，然后再解析网页
        # page = driver.page_source
        # html = BeautifulSoup(page, 'html.parser')
        socket.setdefaulttimeout(15)
        # 设置超时时长
        bsObj = self.getBsobj(link)
        if bsObj is None:
            return None
        html = bsObj.decode('utf-8')
        html = html.replace('&lt;', '<')
        html = html.replace('&gt;', '>')
        # 解决一些图片被忽略的问题
        # self.writeFile(self.downloadLocation, 'html', html)
        html = BeautifulSoup(html, 'html.parser')
        # print(html, '\n\n\n\n')
        imgTags = html.findAll('img')
        # 找到所有图片
        i = 0
        count = 0
        self.mkDir(downloadLocation)
        # 找到该文件夹，如果不存在则制作一个
        # print('大约有', len(imgTags), '张图...')
        for imgTag in imgTags:
            if 'src' in imgTag.attrs:
                src = imgTag.attrs['src']
                # print('The', count, 'th pic:  ', src)
                src = self.getAbsoluteURL(link, src)
                # 绝对路径还需要再完善一下
                # 此处已经去重
                if src not in links:
                    links.add(src)
                else:
                    continue
                # 判断该链接是否已经下载过，如果已经下载过，则不再下载了
                # print('src: ', src)
                tail = self.getKindBs64(src)
                # 判断是否是bs64编码的图片，不是则返回False
                if tail is not False:
                    print('存在bs64的图---已经解码')
                    loc = downloadLocation + '\\' + str(i) + str(tail)
                    self.bs64ToPic(src, loc)
                    # 通过bs64直接解码，保存图片
                else:
                    src = self.quoteLink(src)
                    picLinks.append(src)
                    linkToId[src] = i
                    # 将id与链接对应
                i += 1
                #   此行以下都改为调用随机下载方法，原为顺序下载
                #     tail = self.getKind(src)
                #     if tail is not False:
                #         address = downloadLocation + '\\' + str(i) + str(tail)
                #         src = self.quoteLink(src)
                #         # 讲此项添加至链接中
                #         print('sra', src)
                #         try:
                #             self.wait()
                #             # 暂停一会儿
                #             urlretrieve(src, address)
                #         # except (urllib.error.HTTPError, socket.timeout, urllib.error.URLError, urllib.error):
                #         except (socket.timeout, urllib.error.HTTPError):
                #             print('这张图似乎下不了...')
                #             pass
                #         i += 1
                # print('正在下载第', i, '张图片...包含重复图片约', len(imgTags), '张')
        self.randomDownloadPic(picLinks, linkToId, downloadLocation)

    def prevent(self):
        print('此次中断，键入一值后继续...')
        a = input()
        return a

    # 传入随机下载的路径
    def randomDownloadPic(self, links, linkToId, location):
        errorFlag = False
        errorTime = 0
        count = 0
        if self.piCount is not None:
            maxCount = min(len(links), self.piCount)
        else:
            maxCount = len(links)
        # 代表下载了多少张图片
        hasDownloaded = set()
        random.seed(datetime.datetime.now())
        # 需要产生真随机数
        # print(links)
        # self.prevent()
        while count < maxCount:
            cur = random.randint(0, len(links) - 1)
            if errorFlag is True:
                print('存在些许问题，该网站不再下载图片...')
                return False
            if cur in hasDownloaded:
                continue
            else:
                hasDownloaded.add(cur)
            src = links[cur]
            tail = self.getKind(src)
            address = location + '\\' + str(linkToId[src]) + str(tail)
            # 虽然随机下载，但也有序排列
            print('sra', src)
            try:
                self.wait()
                # 暂停一会儿
                urlretrieve(src, address)
            # except (urllib.error.HTTPError, socket.timeout, urllib.error.URLError, urllib.error):
            except (socket.timeout, urllib.error.HTTPError, OSError, TypeError):
                print('这张图似乎下不了...将跳过')
                errorTime += 1
                if errorTime > 5:
                    errorFlag = True
            print('正在下载第{0}张图...共计{1}张'.format(count, len(links)))
            count += 1

    # 获取页面所有文件，包含图片
    def getAllFile(self):
        return None

    # 填入关键字，返回每个关键字出现的次,默认权重为1
    def getWordsValue(self, link, word, weight=1):
        text = None
        count = 0
        if self.link == link and self.text is not None:
            text = self.text
        else:
            text = self.getText(link)
        if text is not None:
            count = text.count(word)
        value = count * weight
        return value

    # 获取绝对位置---链接
    def getAbsoluteLink(self, comeFrom, to):
        if to.startswith('http'):
            link = to
        else:
            comeFrom = urlparse(comeFrom).scheme + '://' + urlparse(comeFrom).netloc
            link = comeFrom + to
        return link

    # 获取页面上的所有链接，已经去重,网页排版较乱，可能是a，或者其他，因此暂不做文字处理
    def getLinks(self, baseLink):
        linkSet = set()
        links = []
        # 如果源链接是已经求得的链接，则不再分析该页面
        if baseLink == self.link and self.links is not None:
            return self.links
        html = self.getBsobj(baseLink)
        if html is None:
            return None
        aTags = html.findAll('a')
        # 找到所有链接
        for aTag in aTags:
            # print(aTag)
            if 'href' in aTag.attrs:
                link = self.getAbsoluteLink(baseLink, aTag['href'])
                # print('srb:', link)
                if link not in linkSet:
                    linkSet.add(link)
                    link = self.quoteLink(link)
                    # print('src', link)
                    links.append(link)
        for link in links:
            print(link)
        self.links = links
        # 添加到默认的links
        return links

    # 创建对应路径的文件夹，如果存在则不做
    def mkDir(self, path):
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.replace('/', '\\')
        path = path.rstrip("\\")
        isExists = os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            return False

    # 将文件写入对应文件夹以及文件名
    def writeFile(self, loc, name, text):
        if text is None:
            return None
        self.mkDir(loc)
        location = loc + '\\' + name + '.txt'
        # f = open(location, 'w')
        # f.write(text.encode('utf-8'))
        # f.close()
        # 上面这种方法容易产生编码问题！！！
        with io.open(location, 'w', encoding='utf-8') as file:
            file.write(text)

    # 释放浏览器
    def close(self):
        self.driver.quit()

def analysisDefault(url, downloadLocation, wbdriver = None):
    driver = None
    if wbdriver is None:
        driver = webdriver.Chrome()
    else:
        driver = wbdriver
    analysis = analysisPage(driver, url, downloadLocation)
    analysis.defaultDeal()
    # bsObj = analysis.getBsobj(analysis.link)
    # html = bsObj.decode('utf-8')
    # print(html)
    # a = input()
    # analysis.close()


if __name__ == '__main__':
    # url = 'https://www.zhihu.com/question/28560777'
    # loc = 'D:\\Computer\\Desk\\test\\知乎漂亮女朋友话题'
    # url = 'http://www.sohu.com/a/132436972_142816'
    # loc = 'D:\\Computer\\Desk\\test\\小米4'
    # analysisDefault(url, loc)
    # i = 124
    # location = 'D:\\Computer\\Desk\\test'
    # links = ['https://www.zhihu.com/question/56460139']
    # for link in links:
    #     loc = location + '\\' + str(i)
    #     analysisDefault(link, loc)
    #     i += 1
    # print('全部分析完成！')

    url = 'https://www.zhihu.com/question/29954258'
    loc = 'D:\\Computer\\Desk\\test\\a'
    driver = webdriver.Chrome()
    a = analysisPage(driver, url, 1, 2, 3, 6, loc, 5, 6, 7)
    a.defaultDeal()