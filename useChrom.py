from selenium import webdriver
import configparser

class UseChrome:
    """
        设置Chrome的一些参数，然后调用
        webDriverLocation   浏览器路径
        header      设定头请求
        cookies     设定饼干
        url         获取的网址，如果设定了url
        language    设定接受语言
        downloadLocation    设定下载路径
        windowSize  窗口大小
        hide        是否隐藏
    """


    def __init__(self, webDriverPath):
        self.webDriverPath = webDriverPath
        self.url = 'http://httpbin.org/headers'
        self.language = "lang=zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2"
        self.userAgent = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"
        self.location = 'D:\\Computer\\Desk\\C'
        # 默认为源代码上一级的Download目录下
        self.hide = False
        # 默认不隐藏
    # 设定浏览器路径

    def setDriver(self):
        driver = self.addOptions(self.location, self.language, self.userAgent)
        return driver


    def addOptions(self, location, language, head):
        # 创建chrome参数对象
        options = webdriver.ChromeOptions()
        # options.add_argument('lang=zh-CN,zh')
        # options.add_argument(
        #      'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0')
        # 设置请求头和语言
        options.add_argument(language)
        options.add_argument(head)
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': location}
        options.add_experimental_option('prefs', prefs)
        # 设置自动下载路径，让下载的时候不再选择下载路径
        driver = webdriver.Chrome(chrome_options=options)
        # 添加设置，并获得一个浏览器
        # ...

        return driver
    # 设置一些参数，然后将他添加至浏览器之中

    def getCookies(self, driver):
        cookies = driver.get_cookies()
        return cookies

    def addCookies(self, driver, url, cookies):
        # cookies = [{}, {}]类似这样的cookies
        driver.get(url)
        driver.delete_all_cookies()
        # 清除所有cookies
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get(url)
        # 使用cookies，必须先指明是哪个网站，再使用cookies
        return driver

    def defaultGetDriver(self):
        pass

def defaultUse():
    # 这是一个默认使用driver的操作，主要用于爬虫，无界面显示
    cf = configparser.ConfigParser()
    cf.read('spider.conf')
    userAgent = 'user-agent=' + cf.get('webDriver', 'user-agent')
    # userAgent = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"
    language = 'lang=' + cf.get('webDriver', 'lang')
    # language = "lang=zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2"
    location = cf.get('webDriver', 'downloadLocation')
    # location = 'Download'
    options = webdriver.ChromeOptions()
    isHide = cf.get('webDriver', 'isHide')
    if isHide == 'True':
        options.set_headless()
    # 爬虫设定隐藏窗口
    # options.add_argument('lang=zh-CN,zh')
    # options.add_argument(
    #      'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0')
    options.add_argument(language)
    options.add_argument(userAgent)
    # 设置请求头和语言
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': location}
    options.add_experimental_option('prefs', prefs)
    # 设置自动下载路径，让下载的时候不再选择下载路径
    driver = webdriver.Chrome(chrome_options=options)
    return driver


if __name__ == '__main__':
    # loc = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    # c = UseChrome(loc)
    # driver = c.setDriver()
    # print('set over')
    # driver.get('https://www.baidu.com/')
    # print(driver.page_source)
    # a = input()
    # driver.quit()
    driver = defaultUse()
    driver.get('https://www.baidu.com/s?wd=水稻')
    print(driver.page_source)
    driver.quit()

