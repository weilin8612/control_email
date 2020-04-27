import smtplib
from email.mime.text import MIMEText
import logging
from email.mime.multipart import MIMEMultipart
from email.header import Header

class control_email:
    '''
    发送邮件需要使用POP3/SMTP服务（收邮件），IMAP/SMTP服务（发邮件），这个服务接口的启用在所登陆邮箱的服务器设置，
    QQ邮箱需要登陆网页版设置，手机验证得到一个授权码，此授权码是MUA（用户代理）收发邮件的登陆密码。
    所有的输出都是logging形式，所以使用前需要设置logging接收信息，想要完全接收信心，设置成info，如下
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    '''
    def __init__(self, user, passwd, sever=None):
        '''

        :param user:邮箱地址（也就是登陆邮箱账号）
        :param passwd: 授权码（不是登陆密码）
        :param sever: 邮箱账户所在的服务器，默认QQ服务器
        '''
        self.user = user
        self.passwd = passwd
        if sever == None:
            self.sever = "smtp.qq.com"


    def send_alone_email(self, text, to_addr, From_email = None, To_email = None, Subject = None):
        '''
        发送简单的文本文件
        :param text: 文本内容，可以是HTML在内的所有文本
        :param to_addr: 发送至哪个邮箱
        :param from_email: 邮件来源
        :param To_email: 邮件去向
        :param Subject: 主题
        :return:
        '''
        if From_email == None:
            from_email = self.user
        if To_email == None:
            To_email = self.user
        if Subject == None:
            Subject = "无主题"
        message = MIMEText(text, "plain", "utf-8")
        #填写信息
        message["From"] = Header("<{}>".format(From_email), "utf-8")
        message["To"] = Header("<{}>".format(To_email), "utf-8")
        message["Subject"] = Header(Subject, "utf-8")

        try:
            #构建邮件服务器实例，第一个参数是bytes类型
            srv = smtplib.SMTP_SSL(self.sever.encode(), 465)
            #登陆邮箱
            srv.login(self.user, self.passwd)
            #发送邮件，第三个参数是str类型
            srv.sendmail(user, [to_addr], message.as_string())
            srv.quit()
            logging.info("发送邮件成功")
        except Exception as e:
            logging.warning("发送邮件失败")

    def send_mul_email(self, text, filename, to_addr):
        '''
        发送带有附件的邮件，目前不怎么用，所以象征性的只支持一个附件
        :param text: 文本文件，包括HTML在内的所有文本文件
        :param filename: 附件文件名
        :param to_addr: 发送至哪个邮箱
        :return:
        '''
        mail_mul = MIMEMultipart()
        #构建正文
        mail_text = MIMEText(text, "plain", "utf-8")
        #把构建好的邮件正文附加到邮件中
        mail_mul.attach(mail_text)
        #读取附件并且附加到邮件中
        with open(filename, 'rb') as f:
            s = f.read()
            #设置福建的MIME和文件名
            m = MIMEText(s, 'base64', 'utf-8')
            m['Content-Type'] = "application/octet-stream"
            #需要注意的是
            #1. attachment后分号为英文状态
            #2. filename后面需要用引号包裹，注意与外面引号错开
            m["Content-Disposition"] = "attachment; filename={}".format(filename)
            #添加到邮件中
            mail_mul.attach(m)
            try:
                # 构建邮件服务器实例，第一个参数是bytes类型
                srv = smtplib.SMTP_SSL(self.sever.encode(), 465)
                # 登陆邮箱
                srv.login(self.user, self.passwd)
                # 发送邮件，第三个参数是str类型
                srv.sendmail(user, [to_addr], mail_mul.as_string())
                srv.quit()
                logging.info("发送邮件成功")
            except Exception as e:
                logging.warning("邮件发送失败")

    def receive_email(self):
        pass


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    text = "I love you "
    user = "398344250@qq.com"
    passwd = "验证码"

    ser = control_email(user, passwd)
    ser.send_alone_email(text, user, From_email=user, To_email=user, Subject="okokok")