# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# 输入Email地址和口令:
from_addr = '1186388488@qq.com'
password = 'zj123456!'
# 输入收件人地址:
to_addr = 'z_jie@yadea.com.cn'
# 输入SMTP服务器地址:
smtp_server = 'smtp.qq.com'

import smtplib
server = smtplib.SMTP(smtp_server, 465) # SMTP协议默认端口是25
server.set_debuglevel(1)
server.login(from_addr, password)

messge = "hello python"
server.sendmail(from_addr, [to_addr], messge)
server.quit()