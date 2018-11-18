import time
import socket
import socks
import requests
from stem import Signal
from stem.control import Controller


class utor:
    def __init__(self):
        self.controller = Controller.from_port(port=9151)

    def connectTor(self):
        socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, "localhost", 9150, True)
        socket.socket = socks.socksocket

    def renew_tor(self):
        self.controller.authenticate()
        self.controller.signal(Signal.NEWNYM)

    def showmyip(self):
        r = requests.get('http://icanhazip.com/')
        ip_address = r.text.strip()
        print(ip_address)






if __name__ == '__main__':
    for i in range(10):
        print('start')
        renew_tor()
        connectTor()
        showmyip()
        time.sleep(10)