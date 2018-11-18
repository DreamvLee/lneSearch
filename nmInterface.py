import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mBox
from tkinter.filedialog import askdirectory
import threading
import dealNormal
from tkinter import scrolledtext
from selenium import webdriver


class nmTab:
    def __init__(self, tab):
        self.tab = tab
        self.init()
        self.dealnormal = dealNormal.dnm()
        # self.tab = tk.LabelFrame(tab)

    def init(self):
        self.isUseGoolge = False
        self.isUseBaiDu = False
        self.isUseBing  = False
        self.isUseTsz = False
        self.isGetPic = False
        self.isGetTxt = False
        self.isGetLink = False
        self.path = None

    def doNothing(self):
        mBox.showinfo('来到了程序的荒原', '玩命开发中...')
        return None

    # 选择搜索引擎，选择框
    def chooseSearch(self):
        title = tk.Label(self.tab, text='      选择搜索引擎：      ')
        title.grid(row=2, column=1, sticky='W')

        self.varIsUseGoolge = tk.IntVar()
        ggcheck = tk.Checkbutton(self.tab, text='谷歌    ', variable=self.varIsUseGoolge)
        ggcheck.grid(row=2, column=2, sticky='W')

        self.varIsUseBaiDu = tk.IntVar()
        bdcheck = tk.Checkbutton(self.tab, text='百度    ', variable=self.varIsUseBaiDu)
        bdcheck.grid(row=2, column=3, sticky='W')

        self.varIsUseBing = tk.IntVar()
        bingcheck = tk.Checkbutton(self.tab, text='必应    ', variable=self.varIsUseBing)
        bingcheck.grid(row=2, column=4, sticky='W')

        self.varIsUseTsz = tk.IntVar()
        tszcheck = tk.Checkbutton(self.tab, text='360    ', variable=self.varIsUseTsz)
        tszcheck.grid(row=2, column=5, sticky='W')

    # 此项是关键期输入框
    def keyWordsInput(self):
        titleK = ttk.Label(self.tab, text='      关键词')
        titleW = ttk.Label(self.tab, text='权重')

        widthK = 15
        padx = 4
        pady = 4
        titleK.grid(row=4, column=1, sticky='W')
        titleW.grid(row=4, column=2)

        self.varKeyWord0 = tk.StringVar()
        self.keyWord0 = ttk.Entry(self.tab, width=widthK, textvariable=self.varKeyWord0)
        self.keyWord0.grid(row=6, column=1, padx=padx, pady=pady)

        self.varKeyWord1 = tk.StringVar()
        self.keyWord1 = ttk.Entry(self.tab, width=widthK, textvariable=self.varKeyWord1)
        self.keyWord1.grid(row=8, column=1, padx=padx, pady=pady)

        self.varKeyWord2 = tk.StringVar()
        self.keyWord2 = ttk.Entry(self.tab, width=widthK, textvariable=self.varKeyWord2)
        self.keyWord2.grid(row=10, column=1, padx=padx, pady=pady)

        self.varKeyWord3 = tk.StringVar()
        self.keyWord3 = ttk.Entry(self.tab, width=widthK, textvariable=self.varKeyWord3)
        self.keyWord3.grid(row=12, column=1, padx=padx, pady=pady)

        self.varKeyWord4 = tk.StringVar()
        self.keyWord4 = ttk.Entry(self.tab, width=widthK, textvariable=self.varKeyWord4)
        self.keyWord4.grid(row=14, column=1, padx=padx, pady=pady)

        widthW = 5

        self.varWeight0 = tk.StringVar()
        self.weight0 = ttk.Entry(self.tab, width=widthW, textvariable=self.varWeight0)
        self.weight0.grid(row=6, column=2, padx=padx, pady=pady)

        self.varWeight1 = tk.StringVar()
        self.weight1 = ttk.Entry(self.tab, width=widthW, textvariable=self.varWeight1)
        self.weight1.grid(row=8, column=2, padx=padx, pady=pady)

        self.varWeight2 = tk.StringVar()
        self.weight2 = ttk.Entry(self.tab, width=widthW, textvariable=self.varWeight2)
        self.weight2.grid(row=10, column=2, padx=padx, pady=pady)

        self.varWeight3 = tk.StringVar()
        self.weight3 = ttk.Entry(self.tab, width=widthW, textvariable=self.varWeight3)
        self.weight3.grid(row=12, column=2, padx=padx, pady=pady)

        self.varWeight4 = tk.StringVar()
        self.weight4 = ttk.Entry(self.tab, width=widthW, textvariable=self.varWeight4)
        self.weight4.grid(row=14, column=2, padx=padx, pady=pady)

    def rightPart(self):
        widthLike = 3

        titleLike = ttk.Label(self.tab, text='相似度阈值:')
        titleLike.grid(row=6, column=3, sticky='w')
        self.varWeightLike = tk.StringVar()
        self.weightLike = ttk.Entry(self.tab, width=widthLike, textvariable=self.varWeightLike)
        self.weightLike.grid(row=6, column=4, sticky='w')

        symbol = ttk.Label(self.tab, text='%')
        symbol.grid(row=6, column=4)

        titleCount = ttk.Label(self.tab, text='结果数量：')
        titleCount.grid(row=6, column=5, sticky='E')

        widthO = 3
        self.varOutcomeCount = tk.StringVar()
        self.outcomeCount = ttk.Entry(self.tab, width=widthO, textvariable=self.varOutcomeCount)
        self.outcomeCount.grid(row=6, column=6, sticky='W')

        titleKind = ttk.Label(self.tab, text='获取资料：')
        titleKind.grid(row=8, column=3, sticky='W')
        self.varIsGetPic = tk.IntVar()
        self.btnPic = tk.Checkbutton(self.tab, text='图片', variable=self.varIsGetPic)
        self.btnPic.grid(row=8, column=4, sticky='W')
        self.varIsGetTxt = tk.IntVar()
        self.btnTxt = tk.Checkbutton(self.tab, text='文本', variable=self.varIsGetTxt)
        self.btnTxt.grid(row=8, column=5, sticky='W')
        self.varIsGetLink = tk.IntVar()
        self.btnLk = tk.Checkbutton(self.tab, text='链接', variable=self.varIsGetLink)
        self.btnLk.grid(row=8, column=6, sticky='W')

        btnPg = tk.Checkbutton(self.tab, text='网页文件')
        # 并未挂载

        widthL = 10
        titleSave = tk.Label(self.tab, text='存储路径：')
        titleSave.grid(row=10, column=3, sticky='W')
        self.varDownloadLoc = tk.StringVar()
        self.locInput = ttk.Entry(self.tab, width=widthL, textvariable=self.varDownloadLoc)
        self.locInput.grid(row=10, column=4, sticky='W')
        self.btnLoc = ttk.Button(self.tab, text='路径选择', command=self.setPath)
        self.btnLoc.grid(row=10, column=5)

        self.btnStart = tk.Button(self.tab, text='开始', width=10, height=2, command=self.start, background='#E1E1E1')
        self.btnStart.grid(row=12, column=4, rowspan=4)

    def checkCallBack(self, *ignoredArgs):
        if self.varIsGetPic.get():
            self.isGetPic = True
        else:
            self.isGetPic = False

        if self.varIsGetTxt.get():
            self.isGetTxt = True
        else:
            self.isGetTxt = False

        if self.varIsGetLink.get():
            self.isGetLink = True
        else:
            self.isGetLink = False

        if self.varIsUseGoolge.get():
            self.isUseGoolge = True
        else:
            self.isUseGoolge = False

        if self.varIsUseBaiDu.get():
            self.isUseBaiDu = True
        else:
            self.isUseBaiDu = False

        if self.varIsUseBing.get():
            self.isUseBing = True
        else:
            self.isUseBing = False

        if self.varIsUseTsz.get():
            self.isUseTsz = True
        else:
            self.isUseTsz = False

    def printInfo(self):
        print('google:', self.isUseGoolge)
        print('baidu:', self.isUseBaiDu)
        print('bing:', self.isUseBing)
        print('360:', self.isUseTsz)
        print('picture:', self.isGetPic)
        print('text:', self.isGetTxt)
        print('link:', self.isGetLink)
        print('------------------------')
        print('keyWord:', self.varKeyWord0.get(), 'weight:', self.varWeight0.get())
        print('keyWord:', self.varKeyWord1.get(), 'weight:', self.varWeight1.get())
        print('keyWord:', self.varKeyWord2.get(), 'weight:', self.varWeight2.get())
        print('keyWord:', self.varKeyWord3.get(), 'weight:', self.varWeight3.get())
        print('keyWord:', self.varKeyWord4.get(), 'weight:', self.varWeight4.get())
        print(self.varWeightLike.get(), self.varOutcomeCount.get())
        print(self.path)
        print('--------------------------')

    def getWindows(self):
        # self.root = tk.Tk()
        self.rootResult = tk.Toplevel()
        self.rootResult.wm_attributes('-topmost', 1)
        # self.rootOutcome = tk.Toplevel()
        # self.rootOutcome.wm_attributes('-topmost', 1)
        # 置于顶层
        self.setWindows()
        return self.rootResult

    def setWindows(self):
        # self.rootOutcome.resizable(False, False)
        # self.rootOutcome.wm_iconbitmap('spider.ico')
        # print("开始展现")
        # self.rootOutcome.mainloop()
        # print("展现结束")
        self.rootResult.resizable(False, False)
        self.rootResult.wm_iconbitmap('spider.ico')
        self.rootResult.geometry('400x315+140+275')
        print("开始展现")

    def start(self):
        # self.startSearch()
        self.getWindows()
        self.showResult()
        th = threading.Thread(target=self.startSearch, args=())
        th.setDaemon(True)
        th.start()

    def startSearch(self):
        keyWords = []
        keyWords.append(self.varKeyWord0)
        keyWords.append(self.varKeyWord1)
        keyWords.append(self.varKeyWord2)
        keyWords.append(self.varKeyWord3)
        keyWords.append(self.varKeyWord4)
        weights = []
        weights.append(self.varWeight0)
        weights.append(self.varWeight1)
        weights.append(self.varWeight2)
        weights.append(self.varWeight3)
        weights.append(self.varWeight4)
        self.k = []
        self.w = []
        if keyWords[0].get() == '':
            self.rootResult.destroy()
            mBox.showwarning('警告', '存在未填写的参数！')
            return None
        for i in range(0, 5):
            if keyWords[i].get() != '':
                try:
                    self.k.append(keyWords[i].get())
                    self.w.append(int(weights[i].get()))
                except ValueError:
                    mBox.showerror('错误', '输入格式不正确！')
                    return None
            else:
                break

        print('google:', self.isUseGoolge)
        print('baidu:', self.isUseBaiDu)
        print('bing:', self.isUseBing)
        print('360:', self.isUseTsz)

        self.outcomes = self.dealnormal.start(self.isUseGoolge, self.isUseBaiDu, self.isUseBing, self.isUseTsz,
                              self.isGetPic, self.isGetTxt, self.isGetLink,
                              self.k, self.w, int(self.varWeightLike.get()), int(self.varOutcomeCount.get()), self.path)
        self.showOutcomes(self.outcomes)
        self.dealnormal.analysisAllPage()
        # 这里处理是否要逐页分析

    def setPath(self):
        self.path = askdirectory()
        self.varDownloadLoc.set(self.path)

    # 打开该网页
    def openPage(self, link):
        driver = webdriver.Chrome()
        driver.get(link)

    # 通过浏览器展示页面的网页,以下是处理得出的结果
    def showPage(self, link):
        th = threading.Thread(target=self.openPage, args=(link,))
        th.setDaemon(True)
        th.start()
        # 打开该网页
        pass

    def showDetail(self):
        self.rootOutcome = tk.Toplevel()
        self.rootOutcome.wm_attributes('-topmost', 1)
        self.scrOtm = scrolledtext.ScrolledText(self.rootOutcome)
        self.scrOtm.pack()
        self.scrOtm.config(state='normal')
        for outcome in self.outcomes:
            if outcome.title is not None:
                self.scrOtm.insert('insert', outcome.title + '\n')
            else:
                self.scrOtm.insert('insert', '未获取到标题' + '\n')
            if outcome.link is not None:
                self.scrOtm.insert('insert', outcome.link + '\n')
            else:
                self.scrOtm.insert('insert', '未获取到连接' + '\n')
            if outcome.description is not None:
                self.scrOtm.insert('insert', outcome.description + '\n')
            else:
                self.scrOtm.insert('insert', '未获取到描述' + '\n')
            self.scrOtm.insert('insert', '\n\n')
        self.scrOtm.config(state='disabled')
        self.rootOutcome.resizable(False, False)
        self.rootOutcome.wm_iconbitmap('spider.ico')
        print("开始展现")
        self.rootOutcome.mainloop()
        print("展现结束")
        pass

    def showAns(self):
        cur = 0 * self.numT + 0
        if cur < len(self.resultLink):
            print(self.resultLink[cur])
            self.showPage(self.resultLink[cur])
            # 访问该连接！！！

    def showAns0(self):
        cur = 0 * self.numT + 0
        if cur < len(self.resultLink):
            print(self.resultLink[cur])
            self.showPage(self.resultLink[cur])
            # 访问该连接！！！

    def showAns1(self):
        cur = 0 * self.numT + 1
        if cur < len(self.resultLink):
            print(self.resultLink[cur])
            self.showPage(self.resultLink[cur])
            # 访问该连接！！！

    def showAns2(self):
        cur = 0 * self.numT + 2
        if cur < len(self.resultLink):
            print(self.resultLink[cur])
            self.showPage(self.resultLink[cur])
            # 访问该连接！！！

    def showAns3(self):
        cur = 0 * self.numT + 3
        if cur < len(self.resultLink):
            print(self.resultLink[cur])
            self.showPage(self.resultLink[cur])
            # 访问该连接！！！

    def showAns4(self):
        cur = 0 * self.numT + 4
        if cur < len(self.resultLink):
            print(self.resultLink[cur])
            self.showPage(self.resultLink[cur])
            # 访问该连接！！！

    def showAns5(self):
        cur = 0 * self.numT + 5
        if cur < len(self.resultLink):
            print(self.resultLink[cur])
            self.showPage(self.resultLink[cur])
            # 访问该连接！！！

    def showAns6(self):
        cur = 0 * self.numT + 6
        if cur < len(self.resultLink):
            print(self.resultLink[cur])
            self.showPage(self.resultLink[cur])
            # 访问该连接！！！

    def showAns7(self):
        cur = 0 * self.numT + 7
        if cur < len(self.resultLink):
            print(self.resultLink[cur])
            self.showPage(self.resultLink[cur])
            # 访问该连接！！！

    def showAns8(self):
        cur = 0 * self.numT + 8
        if cur < len(self.resultLink):
            print(self.resultLink[cur])
            self.showPage(self.resultLink[cur])
            # 访问该连接！！！

    def showAns9(self):
        cur = 0 * self.numT + 9
        if cur < len(self.resultLink):
            print(self.resultLink[cur])
            self.showPage(self.resultLink[cur])
            # 访问该连接！！！

    def showBtnAns(self):
        width = 56
        padx = 1
        pady = 1
        # self.titleAns = tk.StringVar()
        # self.btnAns = ttk.Button(self.rootResult, textvariable=self.titleAns, command=self.showAns, width=width)
        # self.btnAns.grid(row=2, column=2, padx=padx, pady=pady)

        self.titleAns0 = tk.StringVar()
        self.btnAns0 = ttk.Button(self.rootResult, textvariable=self.titleAns0, command=self.showAns0, width=width)
        self.btnAns0.grid(row=4, column=2, padx=padx, pady=pady)

        self.titleAns1 = tk.StringVar()
        self.btnAns1 = ttk.Button(self.rootResult, textvariable=self.titleAns1, command=self.showAns1, width=width)
        self.btnAns1.grid(row=6, column=2, padx=padx, pady=pady)

        self.titleAns2 = tk.StringVar()
        self.btnAns2 = ttk.Button(self.rootResult, textvariable=self.titleAns2, command=self.showAns2, width=width)
        self.btnAns2.grid(row=8, column=2, padx=padx, pady=pady)

        self.titleAns3 = tk.StringVar()
        self.btnAns3 = ttk.Button(self.rootResult, textvariable=self.titleAns3, command=self.showAns3, width=width)
        self.btnAns3.grid(row=10, column=2, padx=padx, pady=pady)

        self.titleAns4 = tk.StringVar()
        self.btnAns4 = ttk.Button(self.rootResult, textvariable=self.titleAns4, command=self.showAns4, width=width)
        self.btnAns4.grid(row=12, column=2, padx=padx, pady=pady)

        self.titleAns5 = tk.StringVar()
        self.btnAns5 = ttk.Button(self.rootResult, textvariable=self.titleAns5, command=self.showAns5, width=width)
        self.btnAns5.grid(row=14, column=2, padx=padx, pady=pady)

        self.titleAns6 = tk.StringVar()
        self.btnAns6 = ttk.Button(self.rootResult, textvariable=self.titleAns6, command=self.showAns6, width=width)
        self.btnAns6.grid(row=16, column=2, padx=padx, pady=pady)

        self.titleAns7 = tk.StringVar()
        self.btnAns7 = ttk.Button(self.rootResult, textvariable=self.titleAns7, command=self.showAns7, width=width)
        self.btnAns7.grid(row=18, column=2, padx=padx, pady=pady)

        self.titleAns8 = tk.StringVar()
        self.btnAns8 = ttk.Button(self.rootResult, textvariable=self.titleAns8, command=self.showAns8, width=width)
        self.btnAns8.grid(row=20, column=2, padx=padx, pady=pady)

        self.titleAns9 = tk.StringVar()
        self.btnAns9 = ttk.Button(self.rootResult, textvariable=self.titleAns9, command=self.showAns9, width=width)
        self.btnAns9.grid(row=22, column=2, padx=padx, pady=pady)

        self.titleAns0.set('正在获取信息，请稍后...')
        self.titleAns1.set('正在获取信息，请稍后...')
        self.titleAns2.set('正在获取信息，请稍后...')


    def nextPage(self):
        if (self.numT * 10) < len(self.resultTitle):
            self.numT += 1
            self.updateAns()
        else:
            print('已经是尾页！')

    def previousPage(self):
        if self.numT > 0:
            self.numT -= 1
            self.updateAns()
        else:
            print('已经是起始页！')

    # 更新答案标签
    def updateAns(self):
        if (10 * self.numT + 0) < len(self.resultTitle):
            self.titleAns0.set(self.resultTitle[10 * self.numT + 0])
        if (10 * self.numT + 1) < len(self.resultTitle):
            self.titleAns1.set(self.resultTitle[10 * self.numT + 1])
        if (10 * self.numT + 2) < len(self.resultTitle):
            self.titleAns2.set(self.resultTitle[10 * self.numT + 2])
        if (10 * self.numT + 3) < len(self.resultTitle):
            self.titleAns3.set(self.resultTitle[10 * self.numT + 3])
        if (10 * self.numT + 4) < len(self.resultTitle):
            self.titleAns4.set(self.resultTitle[10 * self.numT + 4])
        if (10 * self.numT + 5) < len(self.resultTitle):
            self.titleAns5.set(self.resultTitle[10 * self.numT + 5])
        if (10 * self.numT + 6) < len(self.resultTitle):
            self.titleAns6.set(self.resultTitle[10 * self.numT + 6])
        if (10 * self.numT + 7) < len(self.resultTitle):
            self.titleAns7.set(self.resultTitle[10 * self.numT + 7])
        if (10 * self.numT + 8) < len(self.resultTitle):
            self.titleAns8.set(self.resultTitle[10 * self.numT + 8])
        if (10 * self.numT + 9) < len(self.resultTitle):
            self.titleAns9.set(self.resultTitle[10 * self.numT + 9])

    def showResult(self):
        self.showBtnAns()
        btnNext = ttk.Button(self.rootResult, text='下一页', command=self.nextPage)
        btnNext.grid(row=1, column=2, sticky='E')
        btnPre = ttk.Button(self.rootResult, text='上一页', command=self.previousPage)
        btnPre.grid(row=1, column=2, sticky='W')
        btnDetail = ttk.Button(self.rootResult, text='详细信息', command=self.showDetail)
        btnDetail.grid(row=1, column=2, sticky='N')

    # 将信息显示至
    def showOutcomes(self, outcomes):
        self.resultLink = []
        self.resultTitle = []
        self.numT = -1
        for outcome in outcomes:
            self.resultLink.append(outcome.link)
            self.resultTitle.append(outcome.title)
        self.nextPage()

    def defaultDeal(self):
        self.chooseSearch()
        self.keyWordsInput()
        self.rightPart()
        self.varIsGetPic.trace('w', lambda unused0, unused1, unused2: self.checkCallBack())
        self.varIsGetTxt.trace('w', lambda unused0, unused1, unused2: self.checkCallBack())
        self.varIsGetLink.trace('w', lambda unused0, unused1, unused2: self.checkCallBack())
        self.varIsUseGoolge.trace('w', lambda unused0, unused1, unused2: self.checkCallBack())
        self.varIsUseBaiDu.trace('w', lambda unused0, unused1, unused2: self.checkCallBack())
        self.varIsUseBing.trace('w', lambda unused0, unused1, unused2: self.checkCallBack())
        self.varIsUseTsz.trace('w', lambda unused0, unused1, unused2: self.checkCallBack())


def default(tab):
    nmtab = nmTab(tab)
    nmtab.defaultDeal()


if __name__ == '__main__':
    root = tk.Tk()
    default(root)
    root.mainloop()