import subprocess
import json


class ShadowSocks(object):
    """docstring for ShadowSocks

    初始化函数的两个参数:
        ssPath, ssConfigPath分别代表可执行程序shadowsocks.exe的路径, gui-config.json的路径

    函数:
        setShadowSocks(self, pattern=JapanA_pattern)  # 可用help查看使用
        getHtml(self)                                 # 获取页面内容
        printItem(self, pattern=JapanA_pattern)       # 获取服务器内容
    """

    def __init__(self, ssPath, ssConfigPath, item):
        '''
        文档注释

        Args:
            ssPath: 代表可执行程序shadowsocks.exe的路径
            ssConfigPath: 代表gui-config.json的路径

        '''
        super(ShadowSocks, self).__init__()
        self.ssPath = ssPath
        self.ssConfigPath = ssConfigPath
        self.item = item

    # 设置服务器
    def setShadowSocks(self):
        '''
        文档注释

        Args:
            pattern:所要爬取的服务器的模式.

        Returns:
            None, 无返回
        '''

        server = self.item[0]
        server_port = self.item[1]
        password = self.item[2]
        method = self.item[3]

        with open(self.ssConfigPath, "r+") as f:
            data = json.load(f)
        data['configs'][0]['server'] = server
        data['configs'][0]['server_port'] = server_port
        data['configs'][0]['password'] = password
        data['configs'][0]['method'] = method
        with open(self.ssConfigPath, "w") as f:
            json.dump(data, f, indent=4)

        subprocess.call('taskkill /f /im shadowsocks.exe', stdout=subprocess.PIPE)
        subprocess.Popen(self.ssPath)

    def close(self):
        subprocess.call('taskkill /f /im shadowsocks.exe', stdout=subprocess.PIPE)


def UseDefaultShadowsock():
    ssPath = "D:\\Computer\\System\\shadowsocks-win-dotnet4.0-2.3\\Shadowsocks.exe"

    # 更换为你的ss配置文件路径
    ssConfigPath = "D:\\Computer\\System\\shadowsocks-win-dotnet4.0-2.3\\gui-config.json"
    server = "45.78.73.70"
    server_port = 443
    password = "YzYyYjI3OG"
    method = "aes-256-cfb"
    # 配置信息
    item = []
    item.append(server)
    item.append(server_port)
    item.append(password)
    item.append(method)
    s = ShadowSocks(ssPath, ssConfigPath, item)
    s.setShadowSocks()
    # 需要设置utf-8


def closeShadowsocks():
    subprocess.call('taskkill /f /im shadowsocks.exe', stdout=subprocess.PIPE)


if __name__ == '__main__':
    # 更改为你的ss程序路径
    ssPath = "D:\\Computer\\System\\shadowsocks-win-dotnet4.0-2.3\\Shadowsocks.exe"

    # 更换为你的ss配置文件路径
    ssConfigPath = "D:\\Computer\\System\\shadowsocks-win-dotnet4.0-2.3\\gui-config.json"
    server = "45.78.73.70"
    server_port = 443
    password = "YzYyYjI3OG"
    method = "aes-256-cfb"
    # 配置信息
    item = []
    item.append(server)
    item.append(server_port)
    item.append(password)
    item.append(method)
    s = ShadowSocks(ssPath, ssConfigPath, item)
    s.setShadowSocks()
    # 需要设置utf-8