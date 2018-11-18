import anlsPage as ap
import useChrom
from tkinter import messagebox as mBox

class durl:
    def __init__(self, path=None, driver=None):
        self.path = path
        self.cookies = None
        self.url = None
        self.driver = None
        self.us = useChrom.UseChrome(self.path)
        self.driver = driver
        self.hasAddCookie = False

    def getDriver(self):
        self.driver = useChrom.defaultUse()

    def openUrl(self):
        if self.driver is None:
            self.getDriver()
        self.driver.get(self.url)

    def getCookies(self):
        if self.driver is None:
            mBox.showerror(title='错误', massage='请先打开填写登陆信息')
        self.cookies = self.us.getCookies(self.driver)
        self.driver.quit()
        self.driver = None
        return self.cookies


    # 要更改driver到此处更改
    def addCookies(self, cookies):
        if self.driver is not None:
            self.driver.quit()
        self.getDriver()
        if cookies is not None:
            self.cookies = cookies
        self.us.addCookies(driver=self.driver, url=self.url, cookies=self.cookies)
        self.hasAddCookie = True

    def start(self, url, isGetPic, piCount, interval, slideTime,
              downloadLoc, isGetText, isGetLink):
        if self.hasAddCookie is False:
            if self.driver is not None:
                self.driver.quit()
            self.getDriver()
        self.url = url
        self.isGetPic = isGetPic
        self.piCount = piCount
        self.interval = interval
        self.slideTime = slideTime
        self.downloadLoc = downloadLoc
        self.isGetText = isGetText
        self.isGetLink = isGetLink
        self.ap = ap.analysisPage(self.driver, url, isGetPic, piCount, interval, slideTime, downloadLoc,
              isGetText, isGetLink, self.cookies)
        self.ap.defaultDeal()