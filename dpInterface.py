import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox as mBox
import dpChallenge
import threading


class dpTab:
    def __init__(self, root):
        self.tab = root
        self.count = 1
        self.thread_list = []

    def start(self):
        # 开始键收集的信息
        url = self.urlInput.get()
        # self.doNothing(url)
        startPage = self.pageInput.get()
        # self.doNothing(startPage)
        endPage = self.maxInput.get()
        # self.doNothing(endPage)
        ipFrequency = self.frequencyInput.get()
        # self.doNothing(ipFrequency)
        errorTime = self.errorTime.get()

        self.dp = dpChallenge.dpchallenge(url, startPage, endPage, ipFrequency, errorTime,
                                     self.varTime, self.varError, self.varErrorFrequency,
                                     self.varAverage, self.varPicCount, self.run)
        th = threading.Thread(target=self.dp.deal, args=())
        th.setDaemon(True)
        th.start()

        self.btnEnd.config(state='normal')
        self.btnStart.config(state='disabled')
        self.changeState('disabled')
        # --------------传值需要传set， run传自身！！！--------------------------

        # self.doNothing(errorTime)
        # dp = dpChallenge.dpchallenge(url, startPage, endPage, ipFrequency, errorTime)
        # th = threading.Thread(target=test.default, args=(self.run, ))
        # th.setDaemon(True)
        # th.start()
        # --------------采取线程去 需要修改，同时dpChallenge里面需要改显示的信息--------------------------------
        # self.thread_list.append(threading.Thread(target=test.default, args=(self.run, )))
        # self.thread_list[2].setDaemon(True)
        # self.thread_list[2].start()
        # self.thread_list[2].join()
        return None

    def close(self):
        mBox.showinfo('通知', '程序将在执行完最后一条指令后结束')
        self.dp.closeIt()
        self.btnStart.config(state='normal')
        self.btnEnd.config(state='disabled')
        self.changeState('normal')

    def changeState(self, state):
        self.urlInput.config(state=state)
        self.pageInput.config(state=state)
        self.maxInput.config(state=state)
        self.frequencyInput.config(state=state)
        self.errorTime.config(state=state)


    def doNothing(self, massage):
        # mBox.showinfo('来到了程序的荒原', '玩命开发中...')
        self.run['state'] = 'normal'
        self.count += 1
        massage += '\n'
        self.run.insert('insert', massage)
        self.run['state'] = 'disabled'
        self.run.see(tk.END)
        self.average.config(text=str(self.count))
        return None

    # def modified(self, event):
    #     self.txt.see(tk.END)  # tkinter.END if you use namespaces

    def defaultDeal(self):
        '''
            输入分类url
            开始爬取页数：
            更换ip频率：
            定时开关
            爬取图片数量
            开始
            :return:
        '''
        self.leftPart()
        self.rightPart()

        # self.thread_list.append(threading.Thread(target=self.leftPart()))
        # self.thread_list.append(threading.Thread(target=self.rightPart()))
        # self.thread_list[0].setDaemon(True)
        # self.thread_list[1].setDaemon(True)
        # self.thread_list[0].start()
        # self.thread_list[1].start()
        # self.thread_list[0].join()
        # self.thread_list[1].join()


        return None

    def leftPart(self):
        padx = 0
        pady = 2
        titleUrl = ttk.Label(self.tab, text='URL：')
        titleUrl.grid(row=2, column=1, sticky='E', padx=padx, pady=pady)

        widthU = 25
        self.urlInput = ttk.Entry(self.tab, width=widthU)
        self.urlInput.grid(row=2, column=2, columnspan=3, sticky='W', padx=padx, pady=pady)


        widthP = 5
        titlePage = ttk.Label(self.tab, text='起始页号：')
        titlePage.grid(row=4, column=1, sticky='E', padx=padx, pady=pady)
        self.pageInput = ttk.Entry(self.tab, width=widthP)
        self.pageInput.grid(row=4, column=2, sticky='W', padx=padx, pady=pady)

        widthM = 5
        titleMax = ttk.Label(self.tab, text='终止页号：')
        titleMax.grid(row=6, column=1, sticky='E', padx=padx, pady=pady)
        self.maxInput = ttk.Entry(self.tab, width=widthM)
        self.maxInput.grid(row=6, column=2, sticky='W', padx=padx, pady=pady)

        widthF = 7
        titleFrequency = ttk.Label(self.tab, text='更换ip频率:')
        titleFrequency.grid(row=4, column=3, sticky='E', padx=padx, pady=pady)
        self.frequencyInput = ttk.Entry(self.tab, width=widthF)
        self.frequencyInput.grid(row=4, column=4, padx=padx, pady=pady)

        widthET = 7
        titleErrorTime = ttk.Label(self.tab, text='中断出错次数:')
        titleErrorTime.grid(row=6, column=3, sticky='E')
        self.errorTime = ttk.Entry(self.tab, width=widthET)
        self.errorTime.grid(row=6, column=4, padx=padx, pady=pady)

        self.btnStart = ttk.Button(self.tab, text='开始', command=self.start)
        self.btnStart.grid(row=8, column=1, columnspan=2)

        self.btnEnd = ttk.Button(self.tab, text='结束', command=self.close, state='disabled')
        self.btnEnd.grid(row=8, column=3, columnspan=2)

        self.line = ttk.Label(self.tab, text='---------状态：进行中---------')
        self.line.grid(row=10, column=1, columnspan=4, padx=padx, pady=pady)

        '''
            累计爬取时间
            爬取图片数量
            出错次数
            平均爬取每张图片时间
        '''

        self.varTime = tk.StringVar()
        titleTime = ttk.Label(self.tab, text='花费时间:')
        titleTime.grid(row=12, column=1)
        time = ttk.Label(self.tab, textvariable=self.varTime)
        time.grid(row=12, column=2)
        self.varTime.set('XX时XX分')

        self.varError = tk.StringVar()
        titleError = ttk.Label(self.tab, text='出错次数:')
        titleError.grid(row=12, column=3, sticky='E', padx=padx, pady=pady)
        error = ttk.Label(self.tab, textvariable=self.varError)
        error.grid(row=12, column=4, sticky='W')
        self.varError.set('未出错')

        self.varAverage = tk.StringVar()
        titleAverage = ttk.Label(self.tab, text='平均时间:')
        titleAverage.grid(row=14, column=1, padx=padx, pady=pady)
        self.average = ttk.Label(self.tab, textvariable=self.varAverage)
        self.average.grid(row=14, column=2)
        self.varAverage.set('XX.XX秒')

        self.varErrorFrequency = tk.StringVar()
        titleErrorFrequency = ttk.Label(self.tab, text='出错率:  ')
        titleErrorFrequency.grid(row=14, column=3, sticky='E')
        errorFrequency = ttk.Label(self.tab, textvariable=self.varErrorFrequency)
        errorFrequency.grid(row=14, column=4, sticky='W')
        self.varErrorFrequency.set('未出错')

        self.varPicCount = tk.StringVar()
        titlePicCount = ttk.Label(self.tab, textvariable=self.varPicCount)
        titlePicCount.grid(row=16, column=1, columnspan=4, padx=padx, pady=pady)
        self.varPicCount.set('已获取图片数量： 未下载')

    def rightPart(self):
        widthR = 23
        heightR = 13
        padxR = 30
        titleRun = ttk.Label(self.tab, text='运行日志')
        titleRun.grid(row=2, column=6)
        self.run = scrolledtext.ScrolledText(self.tab, width=widthR, height=heightR)
        self.run.grid(row=4, column=6, rowspan=16, padx=padxR)

def default(root):
    dptab = dpTab(root)
    dptab.defaultDeal()
    return None

if __name__ == '__main__':
    print('dpInterface')
    root = tk.Tk()
    default(root)
    root.geometry('480x258+550+300')
    root.mainloop()
    # t = threading.Thread(target=root.mainloop, args=(9999, ))
    # t.setDaemon(True)
    # t.start()
    # t.join()
