import smtplib
from email.mime.text import MIMEText
import time

class fdbk:
    def __init__(self):
        self.msg_from = 'beidoucore@foxmail.com'  # 发送方邮箱
        self.mfrom = 'beidoucore@foxmail.com'
        self.passwd = 'qyoaeedeafclbajf'  # 填入发送方邮箱的授权码
        self.msg_to = '1498610938@qq.com'  # 收件人邮箱
        # self.msg_to = '2632922126@qq.com' # terri
        self.title = '基于python面向主题的网络爬虫的反馈'

    def defaultSend(self, massage):
        localtime = time.asctime(time.localtime(time.time()))
        massage = massage + '\n' + localtime
        self.send(self.mfrom, self.passwd, self.msg_to, self.title, massage)

    def send(self, msgFrom, psw, msgTo, title, massage):
        try:
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
            s.login(msgFrom, psw)
            subject = title  # 主题
            content = massage # 正文
            msg = MIMEText(content)
            msg['Subject'] = subject
            # 邮件标题
            msg['From'] = msgFrom
            # 发送者
            msg['To'] = msgTo
            # 接受者
            print(msgFrom + '-------->' + msgTo)
            s.sendmail(msgFrom, msgTo, msg.as_string())
            print("发送成功")
        except smtplib.SMTPException as e:
            print(e)
            print("failed")
        finally:
            s.quit()
            print("over")


if __name__ == '__main__':
    fd = fdbk()
    fd.defaultSend('test')