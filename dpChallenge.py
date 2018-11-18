# DPchallenge_spider
import ssl
import os
import re
import time
# import socks
import socks
import socket
import random
import urllib.request
from stem import Signal
from stem.control import Controller
from stem import SocketError
# 错误列表 OSError socks.GeneralProxyError   socks.SOCKS5Error  socks.SOCKS5Error  ConnectionAbortedError
from http.client import RemoteDisconnected
from urllib.error import URLError
from http.client import IncompleteRead
import tkinter as tk
from tkinter import messagebox as mBox
from _tkinter import TclError


class ParamsError(Exception):
    def __init__(self, name):
        print(name, '--该参数在模块内部没有定义！')


class ParamsNotFilledError(Exception):
    def __init__(self):
        print('存在未填写的参数')
        mBox.showerror('错误', '存在未填写的参数')


class dpchallenge:
    def __init__(self, *params, **dparams):
        '''
             需要键入的参数值：
                url:    基类URL 该可通过修改page页数来更改页面图片的
                startPage:起始页号，从该页开始爬取
                endPage:终止页号
                ipFrequency: 更换ip频率
                errorTime: 连续出错多少次，则停止爬取
            :param params:
            :param dparams:
        '''
        self.names = ['url', 'startPage', 'endPage', 'ipFrequency', 'errorTime',
                      'time', 'error', 'errorFrequency', 'average',
                      'titlePicCount', 'run']
        self.param = {'url': None, 'startPage': None, 'endPage': None, 'ipFrequency': None, 'errorTime': None,
                      'time': None, 'error': None, 'errorFrequency': None, 'average': None,
                      'titlePicCount': None, 'run': None}

        for i in range(0, len(params)):
            self.param[self.names[i]] = params[i]

        for name, value in dparams.items():
            if name not in self.names:
                raise (ParamsError(name))
            self.param[name] = value
        # print(self.param)
        for i in range(0, len(self.names)):
            if self.param[self.names[i]] == '':
                raise (ParamsNotFilledError)
        # ----------------------使用param的参数列表--------------------
        self.ip = None
        self.startTime = 0  # 开始时间
        self.nowTime = 0  # 现在时间
        self.runTime = 0  # 运行时间，单位：秒
        self.runTimeInfo = [0, 0, 0, 0, 0, 0]
        self.average = 0  # 平均一张图片的时间
        self.errorCount = 0  # 出错次数
        self.hasDownloadCount = 0  # 打开网页次数
        self.picCount = 0  # 已经下载的图片张数
        self.maxErrorTime = int(self.param['errorTime'])
        self.flagClose = False
        self.errorFlag = False
        # -----------------------一些存储的信息------------------------
        self.massageTime = 'XX时XX分'
        self.massageError = 'XX次'
        self.massageAverage = 'XX.XXX秒'
        self.massageErrorFrequency = 'XX.X%'
        self.massagePicCount = 'xxxx张'
        # ----------------------需要返回的参数列表----------------------
        # self.showError(massage='aaa')
        # mBox.showinfo('aaa', 'bbbb')
        # 开始的秒数
        # -----------------------初始化的一些操作---------------------

    # 返回的是运行时间，依次是年 月 日 小时 分 秒，但是有点问题，它是依据1970年的
    def updateTimeInfo(self):
        self.nowTime = time.time()
        self.runTime = self.nowTime - self.startTime
        runTimeFormat = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(self.runTime + 57600))
        runTimeInfoS = runTimeFormat.split('-')
        for i in range(0, len(runTimeInfoS)):
            self.runTimeInfo[i] = int(runTimeInfoS[i])
        self.runTimeInfo[0] -= 1970
        self.runTimeInfo[1] -= 1
        self.runTimeInfo[2] -= 2

    def closeIt(self):
        self.flagClose = True

    def updatePicInfo(self):
        self.updateTimeInfo()
        self.massageTime = str(self.runTimeInfo[3]) + '时' + str(self.runTimeInfo[4]) + '分'
        self.massageAverage = str(self.runTime / self.picCount)[0:5] + '秒'
        self.massagePicCount = '已获取图片数量：' + str(self.picCount) + '张'
        print('运行时间：', self.massageTime, '平均时间：', self.massageAverage, '图片数量：', self.massagePicCount)
        # 每下完一张图片->更新框中该显示的信息
        self.param['time'].set(self.massageTime)
        self.param['average'].set(self.massageAverage)
        self.param['titlePicCount'].set(self.massagePicCount)

    def updateErrorInfo(self):
        self.updateTimeInfo()
        self.massageTime = str(self.runTimeInfo[3]) + '时' + str(self.runTimeInfo[4]) + '分'
        self.massageError = str(self.errorCount) + '次'
        self.massageErrorFrequency = str((self.errorCount * 100) / self.hasDownloadCount)[0:5] + '%'
        print('运行时间：', self.massageTime, '出错次数:', self.massageError, '出错率：', self.massageErrorFrequency)
        # 出错之后->更新框中该显示的信息

        self.param['time'].set(self.massageTime)
        self.param['error'].set(self.massageError)
        self.param['errorFrequency'].set(self.massageErrorFrequency)

    def updateRun(self, massage):
        self.param['run'].config(state='normal')
        log = massage + '\n'
        self.param['run'].insert('insert', log)
        self.param['run'].config(state='disabled')
        self.param['run'].see(tk.END)
        self.param['run'].update()

    def showWarning(self, massage, title='警告'):
        mBox.showwarning(title, massage)

    def showError(self, massage, title='错误'):
        mBox.showerror(title, massage)

    def showInof(self, massage, title='通知'):
        mBox.showinfo(title, massage)


    def url_open(self, url):
        response = None
        try:
            self.hasDownloadCount += 1
            # 是尝试链接的次数
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0")
            # 加入headers伪装成浏览器访问
            response = urllib.request.urlopen(req)
            print('网页获取成功')
        except (OSError, socks.GeneralProxyError, socks.SOCKS5Error, ConnectionAbortedError,
                RemoteDisconnected, URLError, IncompleteRead, UnboundLocalError):
            self.dealError()
        # 得到了一个直接访问该网站的对象——即访问完成，得到所有网站的信息
        return response

    def connectTor(self):
        # 建立连接
        print("建立连接中...")
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "localhost", 9150, True)
        socket.socket = socks.socksocket
        ip = str(self.url_open('https://icanhazip.com/').read().decode("utf-8", "ignore"))
        if ip == self.ip:
            massage = '使用的是自身ip...请注意！'
            print(massage)
            self.showError(massage)
            self.prevent()
        else:
            print(ip)

    def prevent(self):
        print('出现了需要暂停的地方...输入任意键暂停')
        a = input()
        print(a)

    def renew_tor(self):
        # 刷新连接
        print("刷新连接中...")
        self.controller.authenticate()
        self.controller.signal(Signal.NEWNYM)

    def findall(self, pattern, html):
        return pattern.findall(html)

    # 存在异常，需要修改
    def find_picture(self, count, url):
        # try:
        #     res = self.url_open(url)
        #     res = res.read()
        # except(OSError, socks.GeneralProxyError, socks.SOCKS5Error, ConnectionAbortedError,
        #         RemoteDisconnected, URLError, IncompleteRead):
        #     self.dealError()
        res = self.url_open(url)
        if self.errorFlag is True:
            print('find_picture该函数出现异常')
            return
        try:
            res = res.read()
        except (OSError, socks.GeneralProxyError, socks.SOCKS5Error, ConnectionAbortedError,
                RemoteDisconnected, URLError, IncompleteRead):
            self.dealError()
            return
        print("正在存储图像" + str(count) + "....")
        with open(str(count) + ".jpg", "wb") as f:
            f.write(res)

    def find_wenzi1(self, count, item_list, i):
        title = "Photograph Information\nChallenge:"
        if (not item_list):
            return
        print("正在存储文字" + str(i) + "_1....")
        pattern = re.compile("<(.*?)>", re.S)
        for item in item_list:
            item = item.replace("<br>", "\n")
            item = re.sub(pattern, "", item)
            # 对于一个输入的字符串，利用正则表达式，来实现字符串替换处理的功能返回处理后的字符串
            # 详情请百度
            item = item.replace("	", "")  # 字符串的替换
            with open(str(count) + ".txt", "a") as f:  # 保存
                f.write(title)
                f.write(item)

    def find_wenzi1_1(self, count, item_list, i):
        title = "Photograph Information\n"
        if (not item_list):
            return
        print("正在存储文字" + str(i) + "_1_1....")
        pattern = re.compile("<(.*?)>", re.S)
        for item in item_list:
            item = item.replace("<br>", "\n")
            item = re.sub(pattern, "", item)
            item = item.replace("	", "")
            with open(str(count) + ".txt", "a") as f:  # 保存
                f.write(title)
                f.write(item)

    def find_wenzi1_2(self, count, item_list, i):
        title = "Photograph Information\n"
        if (not item_list):
            return
        print("正在存储文字" + str(i) + "_1_2....")
        pattern = re.compile("<(.*?)>", re.S)
        for item in item_list:
            item = item.replace("<br>", "\n")
            item = re.sub(pattern, "", item)
            item = item.replace("	", "")
            with open("123" + ".txt", "a") as f:  # 保存
                f.write(title)
                f.write(item)

    def find_wenzi2(self, count, item_list, i):
        title = "Photographer's Comments\n"
        print("正在存储文字" + str(i) + "_2....")
        for item in item_list:
            item = item.replace("<br>", "\n")
            item = item.replace("	", "")
            # 找出文字中的链接图片ID
            pattern_ID = re.compile(r'IMAGE_ID=(.*?)" target=">', re.S)
            ID = re.findall(pattern_ID, item)
            finall = ""
            for i in range(0, len(ID)):
                if (i == 0):
                    finall = "\nID = "

                finall += ID[i]
                finall += " "
            finall += "\n"
            # 去除链接
            pattern = re.compile("<(.*?)>", re.S)
            item = re.sub(pattern, "", item)
            with open(str(count) + ".txt", "a") as f:
                f.write(title)
                f.write(item)

    def find_wenzi3(self, count, item_list, i):
        title = "\nStatistics\n"
        print("正在存储文字" + str(i) + "_3....")
        pattern = re.compile("<(.*?)>", re.S)
        for item in item_list:
            item = item.replace("<br>", "\n")
            item = re.sub(pattern, "", item)
            item = item.replace("	", "")
            with open(str(count) + ".txt", "a") as f:
                f.write(title)
                f.write(item)

    def dealError(self):
        self.errorCount += 1
        self.maxErrorTime -= 1
        self.updateErrorInfo()
        self.errorFlag = True
        # 捕获异常，则代表出错了，出错次数+1
        print('...出现异常...不要着急，正在处理...')
        massage = '出现异常，等待一分钟'
        self.updateRun(massage)
        time.sleep(60)
        self.renew_tor()
        self.connectTor()


    def deal(self):
        response = None
        html = None
        torClose = False
        self.ip = str(self.url_open('https://icanhazip.com/').read().decode("utf-8", "ignore"))
        print('自身ip为：', self.ip)
        try:
            self.controller = Controller.from_port(port=9151)
            ssl._create_default_https_context = ssl._create_unverified_context
            self.connectTor()
        except(SocketError, ConnectionRefusedError):
            torClose = True
        if torClose is True:
            massage = '该程序依赖tor...请开启'
            self.showError(massage=massage)
            return None

        # self.renew_tor()

        self.startTime = time.time()

        for i in range(0, len(self.names)):
            if self.param[self.names[i]] is None:
                print('参数不完整！')
                self.showError('参数不完整或错误!')
                return None
        baseUrl = str(self.param['url'])
        p = int(self.param['startPage'])
        endPage = int(self.param['endPage'])
        ipFrequency = int(self.param['ipFrequency'])

        massage = '...start...'
        self.updateRun(massage)
        whe = r'<img src="http://images.dpchallenge.com/images_'
        # 判断是否有这一句,如果有则证明有图片，如果没有则直接跳过
        pic = "https://www.dpchallenge.com/image.php?IMAGE_ID="
        # 查找图片网址
        pattern_p = re.compile(r'<img src="//images.dpchallenge.com/images_(.*?)" width="', re.S)
        pattern_w1 = re.compile(r'<b>Challenge:</b>(.*?)<div style=', re.S)
        pattern_w1_1 = re.compile(r'<td class="textsm" >\n\t\t\t\t\t\t\t\t<b>(.*?)<div style=', re.S)
        pattern_w1_2 = re.compile(r'<td class="textsm" >(.*?)<div style=', re.S)
        pattern_w2 = re.compile(r'<td valign="top" width="450" class="textsm">(.*?)</td>', re.S)
        pattern_w3 = re.compile(r'<td class="textsm" valign="top">(.*?)</td>', re.S)
        pattern_pic = re.compile(r'IMAGE_ID=(.*?)" class="i">', re.S)
        # 正则表达式选取需要的东西  根据源码找到规律  目标在(.*?)里
        # page代表是该类有多少页
        while p < endPage:
            # baseUrl = "https://www.dpchallenge.com/photo_gallery.php?GALLERY_ID="
            url = baseUrl + "&page=" + str(p)

            print("正在搜索该类型的第%d页" % (p))
            print(url)
            massage = '正在搜索该类型的第' + str(p) + '页'
            self.updateRun(massage)
            # self.updateRun(url)
            # try:
            #     response = self.url_open(url)
            #     if response is not None:
            #         html = response.read().decode("utf-8", "ignore")  # 忽视一些非utf-8编码的东西
            #     else:
            #         continue
            # except (OSError, socks.GeneralProxyError, socks.SOCKS5Error, ConnectionAbortedError,
            #         RemoteDisconnected, URLError, IncompleteRead, UnboundLocalError):
            #     print('....外面出现错误....')
            #     self.dealError()
            # 用response.read()在本地获取网站的信息——此时已经访问完成
            # 用该格式解码所得的信息
            response = self.url_open(url)
            if self.errorFlag is True:
                print('errorFlag is True, 执行跳过一次')
                self.errorFlag = False
                continue
            # html = response.read().decode("utf-8", "ignore")  # 忽视一些非utf-8编码的东西
            try:
                html = response.read().decode("utf-8", "ignore")
            except (OSError, IncompleteRead, UnboundLocalError):
                self.errorFlag = True
            if self.errorFlag is True:
                print('页面循环里面read出现异常...')
                self.errorFlag = False
                continue
            item_list_pic = pattern_pic.findall(html)
            # 保存了这一页所有详细图片网页的ID号
            # print("已经获取该类型第%d页图片的所有id号" % (p))
            massage = '已经获取该类型第' + str(p) + '页图片的所有id号'
            self.updateRun(massage)
            max_num = len(item_list_pic)
            # 这一页有多少张图片

            for i in range(0, max_num):
                # print(i, "/", max_num)
                # 已经下载的图片达到了这个数量才需要刷新
                if self.maxErrorTime < 0:
                    massage = '由于连续出错次数达到设定值，停止爬取...'
                    print(massage)
                    self.showError(massage)
                    return None

                if (os.path.exists(str(item_list_pic[i]) + ".jpg")):
                    # 代表存在该张图，则默认不跳过
                    print(str(item_list_pic[i]) + "号文件已存在，正在跳过....")
                    massage = 'ID=' + item_list_pic[i] + '\n存在，执行跳过'
                    self.updateRun(massage)
                    continue
                if ((self.picCount + 1) % ipFrequency == 0):
                    massage = '    ...更换ip中...'
                    self.updateRun(massage)
                    self.renew_tor()  # 刷新连接
                    self.connectTor()  # 建立连接
                    massage = '！！！更换成功！！！'
                    self.updateRun(massage)
                print(0)
                pic_url = pic + item_list_pic[i]  # 图片详细信息网址
                # html = url_open(pic_url).read().decode("utf-8", "ignore")  # 图片详细信息,第二个参数是为了忽视一些微小的不可编码二进制
                '''

                    # 错误列表 OSError socks.GeneralProxyError   socks.SOCKS5Error  socks.SOCKS5Error  ConnectionAbortedError
                    from http.client import RemoteDisconnected
                    from urllib.error import URLError
                    from http.client import IncompleteRead

                '''
                # try:
                #     response = self.url_open(pic_url)
                #     if response is not None:
                #         html = response.read().decode("utf-8", "ignore")
                #     else:
                #         continue
                #     # 图片详细信息,第二个参数是为了忽视一些微小的不可编码二进制
                # except (OSError, socks.GeneralProxyError, socks.SOCKS5Error, ConnectionAbortedError,
                #         RemoteDisconnected, URLError, IncompleteRead, UnboundLocalError):
                #     massage = '外面出现异常'
                #     self.updateRun(massage)
                #     self.showWarning(massage=massage)
                #     self.dealError()
                response = self.url_open(pic_url)
                if self.errorFlag is True:
                    print('图片循环里面出现错误，跳过')
                    self.errorFlag = False
                    continue
                try:
                    html = response.read().decode("utf-8", "ignore")
                except (OSError, IncompleteRead, UnboundLocalError):
                    self.errorFlag = True
                if self.errorFlag is True:
                    print('循环里面read出现异常...')
                    self.errorFlag = False
                    continue
                print(1)  # 出现1代表这次获取图片的详细信息成功
                item_list_p = pattern_p.findall(html)
                # 在所有网页信息中寻找符合正则表达式的信息，返回的是列表
                print(2)  # 出现2代表从详细信息中提取出了我需要的信息
                if (not item_list_p):
                    self.errorCount += 1
                    print(html)
                    print('该号文件不存在dpchallenge中或该ip失效')
                    continue
                if (len(item_list_p[0]) > 100):
                    self.errorCount += 1
                    print('该文件本机没有访问权限，正在跳过...')
                    continue
                picture = "http://images.dpchallenge.com/images_" + item_list_p[0]
                # 返回一个字符串，是保存图片的网址
                print(3)  # 出现3证明访问要保存的图片的网址成功

                self.find_picture(item_list_pic[i], picture)
                if self.errorFlag is True:
                    self.errorFlag = False
                    print('在获取图片的时候出现异常， 后部跳过')
                    continue
                print('id=%s...获取图片成功...' % item_list_pic[i])
                massage = 'id=' + item_list_pic[i] + '图片获取成功'
                self.updateRun(massage)
                item_list_w1 = pattern_w1.findall(html)
                flag_0 = self.find_wenzi1(item_list_pic[i], item_list_w1, i)
                # i代表是该页的第几张图
                if (flag_0 == -1):
                    item_list_w1_1 = pattern_w1_1.findall(html)
                    flag_1 = self.find_wenzi1_1(item_list_pic[i], item_list_w1_1, i)
                if (flag_0 == -1 and flag_1 == -1):
                    item_list_w1_2 = pattern_w1_2.findall(html)
                    self.find_wenzi1_2(item_list_pic[i], item_list_w1_2, i)
                item_list_w2 = pattern_w2.findall(html)
                self.find_wenzi2(item_list_pic[i], item_list_w2, i)
                item_list_w3 = pattern_w3.findall(html)
                self.find_wenzi3(item_list_pic[i], item_list_w3, i)
                print('id=%s...获取文本成功...' % item_list_pic[i])
                massage = 'id=' + item_list_pic[i] + '文本获取成功'
                self.updateRun(massage)
                # 上述都是正则匹配项
                self.picCount += 1
                self.updatePicInfo()
                self.maxErrorTime = int(self.param['errorTime'])
                if self.flagClose is True:
                    massage = '执行关闭成功'
                    print(massage)
                    self.showInof(massage=massage)
                    return None
                # -------上述完成了图片和文本的下载，则是对一张图片的完整下载
                # time.sleep(random.randint(0,3))  # 暂停0~3秒的整数秒，时间区间：[0,3]
            p += 1
        print('该分类已经全部下载完成...请更换爬取信息！')
        massage = '设定值已全部爬取完成'
        self.updateRun(massage=massage)
        self.showInof(massage=massage)

def default(url, startPage, endPage, ipFrequency, errorTime):
    dp = dpchallenge(url, startPage, endPage, ipFrequency, errorTime)
    dp.deal()
    return None


if __name__ == '__main__':
    # 重写姜璐聪的代码
    '''

               # 错误列表 OSError socks.GeneralProxyError   socks.SOCKS5Error  socks.SOCKS5Error  ConnectionAbortedError
               from http.client import RemoteDisconnected
               from urllib.error import URLError
               from http.client import IncompleteRead

           '''
    # try:
    #     html = url_open(pic_url).read().decode("utf-8", "ignore")  # 图片详细信息,第二个参数是为了忽视一些微小的不可编码二进制
    # except (OSError, socks.GeneralProxyError, socks.SOCKS5Error, ConnectionAbortedError, RemoteDisconnected, URLError,
    #         IncompleteRead):
    #     print(item_list_pic[i], '...出现了问题，将跳过此图片和等待一分钟...并重新建立连接')
    #     errorFlag = True
    #     time.sleep(60)
    #     renew_tor()  # 刷新连接
    #     connectTor()  # 建立连接
    #     pass
    '''
        需要键入的参数值：
            url:    基类URL 该可通过修改page页数来更改页面图片的
            startPage:起始页号，从该页开始爬取
            endPage:终止页号
            ipFrequency: 更换ip频率
            errorTime: 连续出错多少次，则停止爬取
            
        需要返回的参数:
            time:总时间（换算成时分），因此要设立一个起始时间和一个现在时间，相减
            average:平均时间，总时间（秒数）/总图片张数
            -----上面两项每爬取一张图片就修改-----
            error: 出错次数, 出现except, 自己也分一个类，然后显示的是总出错次数
            出错率： 出错次数/总尝试爬取图片数
            -----出错一次则修改一下-----
            
        需要修改的问题：
            重新建立class类和一个defaultDeal供调用的方法
            如果是连续跳过图片，则不需要在那里更换ip了
            多处try except需要加入以及新的error
            OS问题常出现，注意观察
            在同目录下建立一个download文件夹其中有pictrue 和 infomation文件夹
            
    '''
    print('--------dpChallenge--------')
    url = 'https://www.dpchallenge.com/photo_gallery.php?GALLERY_ID=53'
    startPage = 1
    endPage = 2
    ipFrequency = 10
    errorTime = 10
    dp = dpchallenge(url, startPage, endPage, ipFrequency, errorTime)
    dp.deal()

