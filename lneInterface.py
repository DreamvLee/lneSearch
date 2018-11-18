import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mBox
import lneMenu
import nmInterface as nmitf
import dpInterface as dpitf
import urlInterface as urlitf

class interface:
    # 这是爬虫的界面
    def __init__(self):
        self.root = tk.Tk()
        self.width = 495    # 图形界面的宽
        self.height = 238   # 图形界面的高 原始258
        self.x_loc = 550    # 在屏幕中显示的位置x
        self.y_loc = 300    # 在屏幕中显示的位置y
        self.root.title('永远相信美好的事情即将发生.')
        # 软件标题
        # self.root.wm_iconbitmap('spider.ico')
        # 软件图标, 在此处设置，会先弹小窗
        # self.root.wm_attributes('-topmost', 1)
        self.rootSize = str(self.width) + 'x' + str(self.height) \
                        + '+' + str(self.x_loc) + '+' + str(self.y_loc)
        # 前两个参数是文本框的大小，后两个参数是在屏幕上显示的位置
    # 默认显示的样子

    def doNothing(self):
        mBox.showinfo('来到了程序的荒原', '玩命开发中...')
        return None

    def menu(self):
        lneMenu.default(self.root)

    def tab(self):
        tabControl = ttk.Notebook(self.root)  # Create Tab Control
        tab_normal = ttk.Frame(tabControl)  # Create a tab
        tabControl.add(tab_normal, text='普通搜索')  # Add the tab
        nmitf.default(tab_normal)

        tab_url = ttk.Frame(tabControl)  # Create a tab
        tabControl.add(tab_url, text='自定义URL')  # Add the tab
        urlitf.default((tab_url))

        tab_dp = ttk.Frame(tabControl)  # Create a tab
        tabControl.add(tab_dp, text='DPchallenge')  # Add the tab
        dpitf.default(tab_dp)

        tabControl.grid(row=1, column=4, columnspan=7, sticky='S')
        # tabControl.pack(fill="both", anchor='center')

    def defaultInterface(self):
        self.menu()
        self.tab()
        self.root.resizable(width=False, height=False)
        self.root.geometry(self.rootSize)
        # 设置窗口大小，且要规定屏幕的位置，要所有东西添加完了才能设置
        self.root.wm_iconbitmap('spider.ico')
        # 软件图标
        self.root.mainloop()
        # 此处使用多线程并不会带来优化



def main():
    lne = interface()
    lne.defaultInterface()



if __name__ == '__main__':
    main()