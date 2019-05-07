#-*- endcoding:utf-8 -*-
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart

from public.read_config.config import ReadConfig
from public.util.log import *
class SendEmail(object):

    def send_email(self, message_body):
        # 获取发送邮件的配置信息
        read_config = ReadConfig()
        sender = read_config.get_sender
        receviers = [read_config.get_receviers + "," + sender]
        password = read_config.get_email_password
        report_path = read_config.get_html_report_path

        # 组建邮件格式
        message = MIMEMultipart()
        message["From"] = formataddr(["测试组", sender])
        message["To"] = ','.join(receviers)
        message['Subject'] = Header("测试报告", 'utf-8')  # 邮件的主题
        message.attach(MIMEText(message_body, _subtype="html", _charset="utf-8"))
        # 构建邮件附件
        att1 = MIMEText(open(report_path, "r", encoding="utf-8").read(), "base64", 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="TestReport.html"'
        message.attach(att1)

        # 发送邮件
        try:
            smtp = smtplib.SMTP("smtp.163.com", port=25)
            smtp.login(sender, password=password)
            smtp.sendmail(sender, message["To"].split(","), message.as_string())
        except Exception as error:
            log("发送邮件发生错误%s" % error)
        else:
            log("发送邮件成功")
        finally:
            smtp.quit()



