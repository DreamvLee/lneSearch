import configparser
from tkinter import messagebox as mBox
from tkinter.filedialog import askdirectory
import tkinter as tk
from tkinter import ttk
from urllib.request import urlopen
import re
import useTor
from stem import SocketError
import feedBack
from tkinter import scrolledtext
from time import sleep

class dmenu:
    def __init__(self):
        self.configLocation = 'spider.conf'
        self.webDriverSection = 'webDriver'
        self.useragents_pc = 'useragents-pc'
        self.useragents_mobile = 'useragents-mobile'
        self.useragents = 'useragents'
        self.seturl = 'dealurl'
        self.setnormal = 'normalsetting'
        self.shadowsocks_c = 'shadowsocks-c'
        self.shadowsocks_u = 'shadowsocks'  # 用户配置的ss
        self.root = None
        self.path = None
        self.cf = self.getConfig()
        print("初始化...")

    def showWarning(self, massage, title='警告'):
        mBox.showwarning(title, massage)

    def showInfo(self, massage, title='通知'):
        mBox.showinfo(title, massage)

    def showError(self, massage, title='错误'):
        mBox.showerror(title, massage)

    def askPath(self):
        self.path = askdirectory()
        self.varPath.set(self.path)
        print('选择的路径为：', self.path)
        return self.path

    def setPath(self):
        self.path = self.varPath.get()
        # 获得输入框的path
        print(self.path)
        # 如果没有选择任何路径的直接按确定的话，则警告没有填写路径
        if self.path == '' or self.path is None:
            massage = '未选择任何路径'
            print(massage)
            self.showWarning(massage)
            return None
        cf = self.getConfig()
        cf.set(self.webDriverSection, 'downloadlocation', str(self.path))
        self.path = None
        # 修改默认下载路径
        self.doWrite(cf)
        self.closeWindows()

    def getWindows(self):
        # self.root = tk.Tk()
        self.root = tk.Toplevel()
        self.root.wm_attributes('-topmost', 1)
        # 置于顶层
        return self.root

    def setWindows(self):
        self.root.resizable(False, False)
        self.root.wm_iconbitmap('spider.ico')
        print("开始展现")
        self.root.mainloop()
        print("展现结束")

    def closeWindows(self):
        # self.root.quit()
        # 主窗口一起销毁
        self.root.destroy()
        # 将该窗口销毁
        self.root = None

    def getConfig(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(self.configLocation)
        return self.cf

    def doWrite(self, cf):
        with open(self.configLocation, 'w+') as f:
            cf.write(f)
        print('修改config配置成功！')

    # 改变默认的下载路径
    def changeDownloadLocation(self):
        '''
            弹窗，选择路径或者填写，选择路径之后则会在框中显示
            确定则是获取框中的路径，如未填写，则警告要求填写
            否则只能按取消或者未填写
            :return:
        '''
        self.getWindows()
        dwidth = 40
        pady = 5
        title = ttk.Label(self.root, text='请选择默认下载路径：')
        title.grid(row=1, column=1, columnspan=3, sticky='W')
        self.varPath = tk.StringVar()
        inputDownloadLocation = ttk.Entry(self.root, width=dwidth, textvariable=self.varPath)
        inputDownloadLocation.grid(row=2, column=1, columnspan=3, pady=pady)
        btnConfirm = ttk.Button(self.root, text='确定', command=self.setPath)
        btnConfirm.grid(row=4, column=1)
        btnChoose = ttk.Button(self.root, text='选择路径', command=self.askPath)
        btnChoose.grid(row=4, column=2)
        btnCancle = ttk.Button(self.root, text='取消', command=self.closeWindows)
        btnCancle.grid(row=4, column=3)
        self.root.geometry('288x85+650+380')
        self.setWindows()
        pass

    def changeHide(self):
        cf = self.getConfig()
        ishide = mBox.askyesno('', '是否选择隐藏爬虫界面')
        print(ishide)
        cf.set(self.webDriverSection, 'ishide', str(ishide))
        self.doWrite(cf)

    def setHead(self):
        head = self.varRad.get()
        print('所选择的head是：', head)
        if self.head == head:
            print('没修改')
            self.closeWindows()
            return
        print(head)
        cf = self.getConfig()
        cf.set(self.webDriverSection, 'user-agent-name', head)
        user_agent = cf.get(self.useragents, head)
        cf.set(self.webDriverSection, 'user-agent', user_agent)
        self.doWrite(cf)
        print('修改请求头成功！')
        self.closeWindows()

    def changeHead(self):
        self.getWindows()
        cf = self.getConfig()
        self.varRad = tk.StringVar()
        self.head = cf.get(self.webDriverSection, 'user-agent-name')
        print(self.head)
        self.varRad.set(self.head)
        title_pc = ttk.Label(self.root, text='电脑端：')
        title_pc.grid(row=2, column=2, sticky='W')
        head = cf.get(self.useragents_pc, 'ua-0')
        pc0 = ttk.Radiobutton(self.root, text=head[0:len(head)-2],
                              variable=self.varRad, value=head)
        pc0.grid(row=4, column=2, sticky='E')
        head = cf.get(self.useragents_pc, 'ua-1')
        pc1 = ttk.Radiobutton(self.root, text=head[0:len(head)-2],
                              variable=self.varRad, value=head)
        pc1.grid(row=4, column=4, sticky='E')
        head = cf.get(self.useragents_pc, 'ua-2')
        pc2 = ttk.Radiobutton(self.root, text=head[0:len(head)-2],
                              variable=self.varRad, value=head)
        pc2.grid(row=4, column=6, sticky='E')
        head = cf.get(self.useragents_pc, 'ua-3')
        pc3 = ttk.Radiobutton(self.root, text=head[0:len(head)-2],
                              variable=self.varRad, value=head)
        pc3.grid(row=4, column=8, sticky='E')
        title_mb = ttk.Label(self.root, text='手机端：')
        title_mb.grid(row=8, column=2, sticky='W')
        head = cf.get(self.useragents_mobile, 'ua-0')
        mb0 = ttk.Radiobutton(self.root, text=head[0:len(head)-2],
                              variable=self.varRad, value=head)
        mb0.grid(row=10, column=4, sticky='E')
        head = cf.get(self.useragents_mobile, 'ua-1')
        mb1 = ttk.Radiobutton(self.root, text=head[0:len(head)-2],
                              variable=self.varRad, value=head)
        mb1.grid(row=10, column=6, sticky='E')
        head = cf.get(self.useragents_mobile, 'ua-2')
        mb2 = ttk.Radiobutton(self.root, text=head[0:len(head)-2],
                              variable=self.varRad, value=head)
        mb2.grid(row=10, column=8, sticky='E')
        btnConfirm = ttk.Button(self.root, text='确定', command=self.setHead)
        btnConfirm.grid(row=12, column=4)
        btnCancel = ttk.Button(self.root, text='取消', command=self.closeWindows)
        btnCancel.grid(row=12, column=6)
        self.root.geometry('280x120+650+380')
        self.setWindows()

    def showIp(self):
        url = 'http://icanhazip.com/'
        reg = "'(.*?)\\\\n'"
        ip = urlopen(url).read()
        ip = re.findall(reg, str(ip))
        print(ip[0])
        massage = 'IP: ' +ip[0]
        self.showInfo(massage)

    def employTor(self):
        # self.showIp()
        torClose = False
        try:
            ut = useTor.utor()
            ut.connectTor()
        except(SocketError, ConnectionRefusedError):
            torClose = True
        if torClose is True:
            massage = '该程序依赖tor...请开启'
            self.showError(massage=massage)
        else:
            massage = 'using tor success'
            self.showInfo(massage)
        # self.showIp()
        # ut.renew_tor()
        # print('更新完成')
        # ut.connectTor()
        # print('连接完成')
        # self.showIp()

    def showAbout(self):
        self.getWindows()
        cf = self.getConfig()
        opts = cf.options('aboutn')
        # for opt in opts:
        for i in range(0, len(opts)-1):
            opt = opts[i]
            name = cf.get('aboutn', opt)
            info = cf.get('about', name) + ':' + cf.get('about', name + 'name')
            label = tk.Label(self.root, text=info)
            label.grid(row=i // 2, column=i % 2)
            print(info)
        opt = opts[len(opts)-1]
        name = cf.get('aboutn', opt)
        info = cf.get('about', name) + cf.get('about', name + 'name')
        label = tk.Label(self.root, text=info)
        label.grid(row=len(opts)-1, column=0, columnspan=2)
        self.root.geometry('150x120+650+380')
        self.setWindows()

    def sendMail(self):
        massage = self.scr.get("1.0", "end-1c")
        print(massage)
        # th = Thread(target=self.sending, args=())
        # th.setDaemon(True)
        # th.start()
        fd = feedBack.fdbk()
        fd.defaultSend(massage)
        self.closeWindows()
        self.showInfo('反馈成功！')

    def sending(self):
        self.scr.insert('insert', '\n正在发送邮件，请稍后...')
        self.scr.config(state='disabled')
        while True:
            if self.root is None:
                return None
            sleep(1)
            self.scr.config(state='normal')
            self.scr.insert('insert', ' ...')
            self.scr.config(state='disabled')
            self.scr.see(tk.END)

    def feedback(self):
        self.getWindows()
        width = 55
        height = 15
        self.scr = scrolledtext.ScrolledText(self.root, width=width, height=height, wrap=tk.WORD)
        self.scr.grid(row=2, column=2, columnspan=4)
        btnCfm = ttk.Button(self.root, text='提交', command=self.sendMail)
        btnCfm.grid(row=4, column=3, sticky='E')
        btnCc = ttk.Button(self.root, text='取消', command=self.closeWindows)
        btnCc.grid(row=4, column=4, sticky='W')
        self.root.geometry('390x228+600+320')
        self.setWindows()

    def changeSildeTime(self):
        cf = self.getConfig()
        self.getWindows()
        padx = 20
        pady = 8
        title = ttk.Label(self.root, text='默认次数：')
        title.grid(row=2, column=2)
        self.slideTime = tk.IntVar()
        self.slideTime.set(cf.get(self.seturl, 'slidetime'))
        print(self.slideTime)
        self.slidetimespin = tk.Spinbox(self.root, from_=0, to=15, textvariable=self.slideTime, width=5, bd=3)
        self.slidetimespin.grid(row=2, column=4, padx=padx, pady=pady)
        widthBtn = 5
        btnCf = ttk.Button(self.root, text='确定', width=widthBtn, command=self.setSlideTime)
        btnCf.grid(row=4, column=2, sticky='E', padx=padx, pady=pady)
        btnCc = ttk.Button(self.root, text='取消', width=widthBtn, command=self.closeWindows)
        btnCc.grid(row=4, column=4, sticky='W', padx=padx, pady=pady)
        self.root.geometry('190x90+710+400')
        self.setWindows()

    def setSlideTime(self):
        self.slideTime = self.slidetimespin.get()
        cf = self.getConfig()
        cf.set(self.seturl, 'slidetime', self.slideTime)
        self.doWrite(cf)
        self.closeWindows()
        self.showInfo('修改成功！')

    def changeInterval(self):
        cf = self.getConfig()
        self.getWindows()
        padx = 20
        pady = 8
        title = ttk.Label(self.root, text='时间间隔：')
        title.grid(row=2, column=2)
        self.interval = tk.IntVar()
        self.interval.set(cf.get(self.seturl, 'interval'))
        print(self.interval)
        self.intervalspin = tk.Spinbox(self.root, from_=0, to=15, textvariable=self.interval, width=5, bd=3)
        self.intervalspin.grid(row=2, column=4, padx=padx, pady=pady)
        widthBtn = 5
        btnCf = ttk.Button(self.root, text='确定', width=widthBtn, command=self.setInterval)
        btnCf.grid(row=4, column=2, sticky='E', padx=padx, pady=pady)
        btnCc = ttk.Button(self.root, text='取消', width=widthBtn, command=self.closeWindows)
        btnCc.grid(row=4, column=4, sticky='W', padx=padx, pady=pady)
        self.root.geometry('190x90+710+400')
        self.setWindows()

    def setInterval(self):
        self.interval = self.intervalspin.get()
        cf = self.getConfig()
        cf.set(self.seturl, 'interval', self.interval)
        self.doWrite(cf)
        self.closeWindows()
        self.showInfo('修改成功！')

    def changeOutcome(self):
        cf = self.getConfig()
        self.getWindows()
        padx = 20
        pady = 8
        title = ttk.Label(self.root, text='结果数量：')
        title.grid(row=2, column=2)
        self.outcome = tk.IntVar()
        self.outcome.set(cf.get(self.setnormal, 'outcome'))
        print(self.outcome)
        self.outcomespin = tk.Spinbox(self.root, from_=0, to=15, textvariable=self.outcome, width=5, bd=3)
        self.outcomespin.grid(row=2, column=4, padx=padx, pady=pady)
        widthBtn = 5
        btnCf = ttk.Button(self.root, text='确定', width=widthBtn, command=self.setOutcome)
        btnCf.grid(row=4, column=2, sticky='E', padx=padx, pady=pady)
        btnCc = ttk.Button(self.root, text='取消', width=widthBtn, command=self.closeWindows)
        btnCc.grid(row=4, column=4, sticky='W', padx=padx, pady=pady)
        self.root.geometry('190x90+710+400')
        self.setWindows()

    def setOutcome(self):
        self.outcome = self.outcomespin.get()
        cf = self.getConfig()
        cf.set(self.setnormal, 'outcome', self.outcome)
        self.doWrite(cf)
        self.closeWindows()
        self.showInfo('修改成功！')

    def changeIntelligentSort(self):
        cf = self.getConfig()
        intelligentsort = mBox.askyesno('', '是否选择智能排序')
        print('智能排序：', intelligentsort)
        cf.set(self.setnormal, 'intelligentsort', str(intelligentsort))
        self.doWrite(cf)

    def changeAnalyzeAllPage(self):
        cf = self.getConfig()
        analyzeallpage = mBox.askyesno('', '是否选择逐页分析')
        print('逐页分析：', analyzeallpage)
        cf.set(self.setnormal, 'analyzeallpage', str(analyzeallpage))
        self.doWrite(cf)

    def changeDefaultShadowsocks(self):
        cf = self.getConfig()
        shadowsocksdefault = mBox.askyesno('', '是否激活连接默认服务器')
        print('是否激活连接默认服务器：', shadowsocksdefault)
        cf.set(self.shadowsocks_c, 'shadowsocksdefault', str(shadowsocksdefault))
        self.doWrite(cf)

    def changeShadowsocks(self):
        self.getWindows()
        width = 20
        padx = 5
        pady = 5
        frameS = ttk.LabelFrame(self.root, text='服务器')
        frameS.pack(pady=pady, padx=padx)
        self.server = tk.StringVar()
        titleServer = ttk.Label(frameS, text='服务器IP')
        titleServer.grid(row=2, column=2, sticky='E', padx=padx, pady=pady)
        entryServer = ttk.Entry(frameS, textvariable=self.server, width=width)
        entryServer.grid(row=2, column=4, sticky='W', padx=padx, pady=pady)

        self.serverPort = tk.StringVar()
        titleServerPort = ttk.Label(frameS, text='服务器端口')
        titleServerPort.grid(row=4, column=2, sticky='E', padx=padx, pady=pady)
        entryServerPort = ttk.Entry(frameS, textvariable=self.serverPort, width=width)
        entryServerPort.grid(row=4, column=4, sticky='W', padx=padx, pady=pady)

        self.password = tk.StringVar()
        titlePassword = ttk.Label(frameS, text='密码')
        titlePassword.grid(row=6, column=2, sticky='E', padx=padx, pady=pady)
        entryPassword = ttk.Entry(frameS, textvariable=self.password, width=width)
        entryPassword.grid(row=6, column=4, sticky='W', padx=padx, pady=pady)

        methodKind = ('table', 'rc4-md5', 'salsa20', 'chacha20',
                      'aes-256-cfb', 'aes-192-cfb', 'aes-128-cfb', 'rc4')
        self.method = tk.StringVar()
        titleMethod = ttk.Label(frameS, text='加密')
        titleMethod.grid(row=8, column=2, sticky='E', padx=padx, pady=pady)
        comboboxMethod = ttk.Combobox(frameS, textvariable=self.method, width=width-2)
        comboboxMethod['values'] = methodKind
        comboboxMethod.grid(row=8, column=4, sticky='W', padx=padx, pady=pady)
        comboboxMethod.current(0)
        comboboxMethod.config(state='readonly')

        self.remarks = tk.StringVar()
        titleRemarks = ttk.Label(frameS, text='备注')
        titleRemarks.grid(row=10, column=2, sticky='E', padx=padx, pady=pady)
        entryRemarks = ttk.Entry(frameS, textvariable=self.remarks, width=width)
        entryRemarks.grid(row=10, column=4, sticky='W', padx=padx, pady=pady)

        widthB = 10
        btnCf = ttk.Button(frameS, text='添加', width=widthB, command=self.setShadowsocks)
        btnCf.grid(row=12, column=2, sticky='E', pady=pady)
        btnCfu = ttk.Button(frameS, text='添加并使用', width=widthB, command=self.addSetShadowsocks)
        btnCfu.grid(row=12, column=4, sticky='W', pady=pady)
        btnCc = ttk.Button(frameS, text='取消', width=widthB, command=self.closeWindows)
        btnCc.grid(row=12, column=4, sticky='E', pady=pady)
        self.root.geometry('250x233+650+320')
        self.setWindows()

    def setShadowsocks(self):
        cf = self.getConfig()
        cf.set(self.shadowsocks_u, 'server', self.server.get())
        cf.set(self.shadowsocks_u, 'server_port', self.serverPort.get())
        cf.set(self.shadowsocks_u, 'password', self.password.get())
        cf.set(self.shadowsocks_u, 'method', self.method.get())
        cf.set(self.shadowsocks_u, 'remarks', self.remarks.get())
        self.doWrite(cf)
        self.closeWindows()
        self.showInfo('修改成功')

    # 添加并修改shadowsocks配置
    def addSetShadowsocks(self):
        cf = self.getConfig()
        cf.set(self.shadowsocks_c, 'shadowsocksdefault', 'False')
        cf.set(self.shadowsocks_c, 'shadowsocks', 'True')
        self.doWrite(cf)
        self.setShadowsocks()

if __name__ == '__main__':
    dm = dmenu()
    # dm.changeHide()
    # dm.changeDownloadLocation()
    # dm.changeHead()
    # dm.showIp()
    # dm.showAbout()
    # dm.feedback()
    # dm.changeOutcome()
    # dm.changeIntelligentSort()
    # dm.changeAnalyzeAllPage()
    dm.changeShadowsocks()