from tkinter import Menu
from tkinter import messagebox as mBox
import tkinter as tk
import dealMenu

class winMenu:
    def __init__(self, root):
        self.root = root
        self.dm = dealMenu.dmenu()

    def doNothing(self):
        mBox.showinfo('来到了程序的荒原', '正在玩命开发中...')
        # mBox.showinfo('a', 'b')
        return None

    def webdriverMenu(self, menuBar):
        '''
            浏览器设置
                    请求头设置   接受语言    默认下载路径    界面是否显示
                    自定义添加cookie   窗口大小    浏览器自身路径
            :param menuBar:
            :return:
        '''
        menu = Menu(menuBar)
        menu.add_command(label='请求头', command=self.dm.changeHead)
        # menu.add_command(label='接受语言', command=self.doNothing)
        menu.add_command(label='是否隐藏', command=self.dm.changeHide)
        menu.add_command(label='下载路径', command=self.dm.changeDownloadLocation)
        # menu.add_command(label='添加cookie', command=self.doNothing)
        # menu.add_command(label='窗口大小', command=self.doNothing)
        # menu.add_command(label='浏览器路径', command=self.doNothing)
        return menu

    def ipMenu(self, menuBar):
        '''
            IP设置
                    查看当前ip    使用高匿tor   使用服务器   自我添加   初始路径
            :param menuBar:
            :return:
        '''
        menu = Menu(menuBar)
        menu.add_command(label='查看当前ip', command=self.dm.showIp)
        menu.add_command(label='高匿tor', command=self.dm.employTor)
        menu.add_command(label='默认端口', command=self.dm.changeDefaultShadowsocks)
        menu.add_command(label='自我添加', command=self.dm.changeShadowsocks)
        return menu

    def setMenu(self, menuBar):
        '''
            设置
                    搜索结果数量   自定义排序   逐页分析
            :param menuBar:
            :return:
        '''
        menu = Menu(menuBar)
        menu.add_command(label='结果数量', command=self.dm.changeOutcome)
        menu.add_command(label='智能排序', command=self.dm.changeIntelligentSort)
        menu.add_command(label='逐页分析', command=self.dm.changeAnalyzeAllPage)
        return menu

    def urlMenu(self, menuBar):
        '''

              URL单页面设置
                滑动次数   滑动间隔
            :param menuBar:
            :return:
        '''
        menu = Menu(menuBar)
        menu.add_command(label='滑动次数', command=self.dm.changeSildeTime)
        menu.add_command(label='时间间隔', command=self.dm.changeInterval)
        return menu


    def aboutMenu(self, menuBar):
        '''

             关于
                    软件说明    我要反馈    特别鸣谢
            :param menuBar:
            :return:
        '''
        menu = Menu(menuBar)
        menu.add_command(label='软件说明', command=self.doNothing)
        menu.add_command(label='我要反馈', command=self.dm.feedback)
        menu.add_command(label='特别鸣谢', command=self.dm.showAbout)
        return menu

    def defaultMenu(self):
        '''
            主菜单
                浏览器 IP 设置 url 关于
        '''
        mainMenu = Menu(self.root)
        self.root.config(menu=mainMenu)

        menu_webdriver = self.webdriverMenu(mainMenu)
        mainMenu.add_cascade(label='浏览器', menu=menu_webdriver)

        menu_ip = self.ipMenu(mainMenu)
        mainMenu.add_cascade(label='IP', menu=menu_ip)

        menu_set = self.setMenu(mainMenu)
        mainMenu.add_cascade(label='设置', menu=menu_set)

        menu_url = self.urlMenu(mainMenu)
        mainMenu.add_cascade(label='url', menu=menu_url)

        menu_about = self.aboutMenu(mainMenu)
        mainMenu.add_cascade(label='关于', menu=menu_about)

def default(root):
    rootMenu = winMenu(root)
    rootMenu.defaultMenu()


if __name__ == '__main__':
    root = tk.Tk()
    default(root)
    root.mainloop()