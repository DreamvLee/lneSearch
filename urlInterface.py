import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mBox
from tkinter.filedialog import askdirectory
import threading
import dealUrl
import configparser

class urlTab:
    def __init__(self, root):
        self.tab = root
        self.dealurl = dealUrl.durl()
        self.configLocation = 'spider.conf'
        self.dealurlCf = 'dealurl'

    def doNothing(self):
        mBox.showinfo('来到了程序的荒原', '玩命开发中...')
        return None

    def setPath(self):
        path = askdirectory()
        self.varDownloadLoc.set(path)

    def getConfig(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(self.configLocation)
        return self.cf

    # url = 'https://www.zhihu.com/question/27364360'
    # 如果没有添加cookies，则start是没有driver的
    def start(self):
        cf = self.getConfig()
        self.urlValue = self.varUrl.get()
        print(self.varPiCount.get())
        if self.varPiCount.get() == '':
            self.piCountValue = None
        else:
            self.piCountValue = int(self.varPiCount.get())
        if self.varInterval.get() == '':
            self.intervalValue = cf.get(self.dealurlCf, 'interval')
        else:
            self.intervalValue = int(self.varInterval.get())
        if self.varSlideTime.get() == '':
            self.intervalValue = cf.get(self.dealurlCf, 'slidetime')
        else:
            self.slideTimeValue = int(self.varSlideTime.get())
        self.downloadLocValue = self.varDownloadLoc.get()
        self.cookiesValue = self.varCookie.get()
        self.pathValue = 'webdriver path'
        th = threading.Thread(target=self.dealurl.start, args=(self.urlValue, self.isGetPic,
                                                               self.piCountValue, self.intervalValue,
                                                               self.slideTimeValue, self.downloadLocValue,
                                                               self.isGetText, self.isGetLink))
        th.setDaemon(True)
        th.start()

    def openWebdriver(self):
        self.url = self.varUrl.get()
        self.dealurl.url = self.url
        th = threading.Thread(target=self.dealurl.openUrl, args=())
        th.setDaemon(True)
        th.start()
        self.btnGetCookie.config(state='normal')
        self.btnOpenWebdriver.config(state='disabled')

    def getCookies(self):
        th = threading.Thread(target=self.dealurl.getCookies, args=())
        th.setDaemon(True)
        th.start()
        self.btnGetCookie.config(state='disabled')

    # 要更改driver到此处更改
    def addCookies(self):
        self.cookies = self.varCookie.get()
        if self.cookies == '':
            self.cookies = None
        th = threading.Thread(target=self.dealurl.addCookies, args=(self.cookies, ))
        th.setDaemon(True)
        th.start()
        self.btnOpenWebdriver.config(state='normal')
        self.btnGetCookie.config(state='normal')

    def checkCallBack(self, *ignoredArgs):
        if self.varIsGetPic.get():
            self.isGetPic = True
            print('pic')
            self.piCount.config(state='normal')
            self.intertal.config(state='normal')
        else:
            self.isGetPic = False
            print('pic no')
            self.piCount.config(state='disabled')
            self.intertal.config(state='disabled')
        if self.varIsGetText.get():
            self.isGetText = True
            print('text')
        else:
            self.isGetText = False
            print('text no')
        if self.varIsGetLink.get():
            self.isGetLink = True
            print('link')
        else:
            self.isGetLink = False
            print('link no')


    def leftPart(self):
        pady = 4
        padxU = 0
        widthU = 60
        self.varUrl = tk.StringVar()
        titleUrl = ttk.Label(self.tab, text='    URL：')
        titleUrl.grid(row=2, column=1, columnspan=4, sticky='W', pady=pady)
        urlInput = ttk.Entry(self.tab, width=widthU, textvariable=self.varUrl)
        urlInput.grid(row=2, column=1, columnspan=4, padx=padxU, sticky='E', pady=pady)

        titleCheckPic = ttk.Label(self.tab, text='    获取图片')
        titleCheckPic.grid(row=4, column=1, sticky='W', pady=pady)
        self.varIsGetPic = tk.IntVar()
        checkPic = tk.Checkbutton(self.tab, text='    ', variable=self.varIsGetPic)
        checkPic.grid(row=4, column=1, sticky='E', pady=pady)
        padxTPC = 20
        widthPC = 4
        self.varPiCount = tk.StringVar()
        titlePiCount = ttk.Label(self.tab, text='  图片数量:')
        titlePiCount.grid(row=4, column=2, sticky='W', pady=pady)
        self.piCount = ttk.Entry(self.tab, width=widthPC, textvariable=self.varPiCount, state='disabled')
        self.piCount.grid(row=4, column=2, sticky='E', pady=pady)

        widthI = 4
        self.varInterval = tk.StringVar()
        titleInterval = ttk.Label(self.tab, text='    间隔时间：         ')
        titleInterval.grid(row=6, column=1, sticky='W', pady=pady)
        self.intertal = ttk.Entry(self.tab, width=widthI, textvariable=self.varInterval, state='disabled')
        self.intertal.grid(row=6, column=1, sticky='E', pady=pady)

        widthT = 4
        self.varSlideTime = tk.StringVar()
        titleSlideTime = ttk.Label(self.tab, text='  滑动次数:')
        titleSlideTime.grid(row=6, column=2, sticky='W', pady=pady)
        self.slideTime = ttk.Entry(self.tab, width=widthT, textvariable=self.varSlideTime)
        self.slideTime.grid(row=6, column=2, sticky='E', pady=pady)

        titleGetTxt = ttk.Label(self.tab, text='    获取文本')
        titleGetTxt.grid(row=8, column=1, sticky='W', pady=pady)
        self.varIsGetText = tk.IntVar()
        getTxt = tk.Checkbutton(self.tab, text='    ', variable=self.varIsGetText)
        getTxt.grid(row=8, column=1, sticky='E', pady=pady)

        titleGetPage = ttk.Label(self.tab, text='获取网页链接       ')
        titleGetPage.grid(row=8, column=2, pady=pady)
        self.varIsGetLink = tk.IntVar()
        getPage= tk.Checkbutton(self.tab, variable=self.varIsGetLink)
        getPage.grid(row=8, column=2, sticky='E', pady=pady)

        widthD = 16
        widthBD = 5
        self.varDownloadLoc = tk.StringVar()
        titleDownloadLoc = ttk.Label(self.tab, text='存储：                                        ')
        titleDownloadLoc.grid(row=10, column=1, columnspan=2, sticky='E', pady=pady)
        downloadLoc = ttk.Entry(self.tab, width=widthD, textvariable=self.varDownloadLoc)
        downloadLoc.grid(row=10, column=1, columnspan=2, pady=pady)
        btnLoc = ttk.Button(self.tab, text='选择', width=widthBD, command=self.setPath)
        btnLoc.grid(row=10, column=1, columnspan=2, sticky='E', pady=pady)

        btnStart = ttk.Button(self.tab, text='开始', command=self.start)
        btnStart.grid(row=12, column=1, columnspan=2, pady=pady)

    def rightPart(self):

        widthC = 24
        self.varCookie = tk.StringVar()
        titleCookie = ttk.Label(self.tab, text='      Cookie:  ')
        titleCookie.grid(row=4, column=3, sticky='E')
        cookie = ttk.Entry(self.tab, width=widthC, textvariable=self.varCookie)
        cookie.grid(row=4, column=4, sticky='E')

        self.btnAddCookie = ttk.Button(self.tab, text='添加指定cookie', command=self.addCookies)
        self.btnAddCookie.grid(row=6, column=3, columnspan=2)

        self.btnOpenWebdriver = ttk.Button(self.tab, text='打开浏览器', command=self.openWebdriver)
        self.btnOpenWebdriver.grid(row=8, column=3, columnspan=2)

        titleHint = ttk.Label(self.tab, text='在网页手动登陆后获取')
        titleHint.grid(row=10, column=3, columnspan=2)

        self.btnGetCookie = ttk.Button(self.tab, text='获得cookie',
                                       command=self.getCookies, state='disabled')
        self.btnGetCookie.grid(row=12, column=3, columnspan=2)

    def defaultDeal(self):
        '''
            输入url:
            获取该页图片
            获取图片数量
            获取网页
            获取链接
            每张图片间隔 上下选择框，秒
            滑动次数    上下选择框，秒
            获取网页cookies
            添加网页cookies
            下载路径设定
            :return:
        '''
        self.leftPart()
        self.rightPart()
        self.varIsGetPic.trace('w', lambda unused0, unused1, unused2: self.checkCallBack())
        self.varIsGetText.trace('w', lambda unused0, unused1, unused2: self.checkCallBack())
        self.varIsGetLink.trace('w', lambda unused0, unused1, unused2: self.checkCallBack())
        return None

def default(root):
    urltab = urlTab(root)
    urltab.defaultDeal()

    return None

if __name__ == '__main__':
    print('dpInterface')
    root = tk.Tk()
    default(root)
    root.geometry('480x258+550+300')
    root.mainloop()