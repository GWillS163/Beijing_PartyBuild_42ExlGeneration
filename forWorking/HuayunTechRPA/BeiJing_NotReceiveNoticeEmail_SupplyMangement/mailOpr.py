# Github: GWillS163
# User: 駿清清 
# Date: 21/11/2022 
# Time: 14:16
import smtplib
from email.header import Header
from email.mime.text import MIMEText


def sendMail(sendMailAdd, sendMailPsd,
             toMailAdd, content):
    try:
        # 发送邮件
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = Header("未接收数据", 'utf-8')
        msg['To'] = Header(toMailAdd, 'utf-8')
        msg['Subject'] = Header("未接收数据", 'utf-8')
        server = smtplib.SMTP_SSL("smtp.163.com", 465)
        server.login(sendMailAdd, sendMailPsd)
        server.sendmail(sendMailAdd, toMailAdd, msg.as_string())
        server.quit()
        res = "发送成功"
    except Exception as e:
        res = f"发送失败，原因：{e}"
    return res


res = sendMail("GWillS@163.com", "MEAPRUHORIODPLJY",
               "GWillS@qq.com", "IPAtest")
print(res)

