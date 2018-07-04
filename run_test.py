#coding=utf-8
import time, sys, smtplib
sys.path.append('./interface')
sys.path.append('./db_fixture')
from HTMLTestRunner import HTMLTestRunner
import unittest
from db_fixture import test_data
from email.mime.text import MIMEText
from email.header import Header
from  email.utils import  parseaddr,formataddr
from email.mime.multipart import MIMEMultipart

#输入发送测试报告的email地址和密码
sender = ['xwzeng@grandstream.cn','zeng@07150830']
#输入接收测试报告的email地址
receiver = ['xwzeng@grandstream.cn']

# 指定测试用例为当前文件夹下的interface目录
test_dir = './interface'
discover = unittest.defaultTestLoader.discover(test_dir, pattern='*_test.py')

def _format_addr(s):
    name,addr = parseaddr(s)
    return formataddr((
        Header(name,'utf-8').encode(),
               addr.encode('utf-8')
               if isinstance(addr,unicode) else addr))

def send(fp):
    #发送主题
    subject = 'Guest Manage System Interface Test Report'
    #发送邮箱服务器
    smtpserver = "smtp.qiye.163.com"

    #发件邮箱用户和密码
    username = sender[0]
    password = sender[1]

    #获取测试报告
    f = open(fp,'rb')
    mail_body = f.read()
    f.close()

   #中文需参数'utf-8'，单字节字符不需要
    header = MIMEText('Dear all:\n      Guest Manget System Interface test has finished,please check test report!',\
                      'plain','utf-8') #中文需参数‘utf-8'，单字节字符不需要


    #附件传送
    msgroot = MIMEMultipart('related')
    #添加发件人
    msgroot['From'] = _format_addr('The Automation Tester<%s>'%sender[0])
    #添加收件人,首先将收件人生生成邮件格式即：XXX<xx@grandstream.cn>
    to =[]
    for i in receiver:
       to.append(_format_addr(i))
    #群发收件人使用逗号链接
    strto = ','.join(to)

    msgroot['To'] = strto
    #添加主题
    msgroot['Subject'] = subject

    #构造附件--测试报告
    att = MIMEText(mail_body,'base64','utf-8')
    att["content-type"] = 'application/octet-stream'
    att["content-Disposition"] = 'attachment;filename=%s'%fp


    msgroot.attach(header)
    msgroot.attach(att)

    #开启smtp链接，发送邮件
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username,password)
    smtp.sendmail(sender[0],receiver,msgroot.as_string())
    smtp.quit()
    print 'email has send out!'


if __name__ == "__main__":
    test_data.init_data()    # 初始化接口测试数据

    now = time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
    subject ='Guest_Manage_System_Interface_Test_Report_'
    #测试报告名字
    filename ='./report/'+subject+now+'.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp, title='Guest Manage System Interface Test Report', description='The_Result_of_TestCase_Execution:')
    runner.run(discover)
    fp.close()
    #发送测试报告
    send(filename)
