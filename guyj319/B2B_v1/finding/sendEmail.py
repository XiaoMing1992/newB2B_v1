# -*- coding: utf-8 -*-
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext


def contacts(request):
    if request.method == 'POST':
            topic = '12345'
            message = '12345'
            sender = 'guyuanjun92@163.com'
            send_mail(
                'Feedback from your site, topic: %s' % topic,
                message, sender,
                ['guyuanjun92@163.com']
            )
            return HttpResponse('thanks')
    else:
       return render_to_response('contact.html', RequestContext(request))


def sendEmail(request):

    if request.method == "POST":
#        方式一：
#         send_mail('subject', 'this is the message of email', 'pythonsuper@gmail.com', ['1565208411@qq.com','1373763906@qq.com'], fail_silently=True)

#        方式二：
#         message1 = ('subject1','this is the message of email1','pythonsuper@gmail.com',['1565208411@qq.com','xinxinyu2011@163.com'])
#         message2 = ('subject2','this is the message of email2','pythonsuper@gmail.com',['1373763906@qq.com','xinxinyu2011@163.com'])
#         send_mass_mail((message1,message2), fail_silently=False)

#        方式三：防止邮件头注入
#         try:
#             send_mail(subject, message, from_email, recipient_list, fail_silently, auth_user, auth_password, connection)
#         except BadHeaderError:
#             return HttpResponse('Invaild header fount.')

#        方式四：EmailMessage()
        #首先实例化一个EmailMessage()对象
#         em = EmailMessage('subject','body','from@example.com',['1565208411@qq.com'],['xinxinyu2011@163.com'],header={'Reply-to':'another@example.com'})
        #调用相应的方法

#         方式五：发送多用途邮件
        subject,form_email,to = 'hello','1422297148@qq.com','1422297148@qq.com'
        text_content = 'This is an important message'
        html_content = u'<b>激活链接：</b><a href="http://www.baidu.com">http:www.baidu.com</a>'
        msg = EmailMultiAlternatives(subject,text_content,form_email,[to])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

#       发送邮件成功了给管理员发送一个反馈
#         mail_admins(u'用户注册反馈', u'当前XX用户注册了该网站', fail_silently=True)
        return HttpResponse(u'发送邮件成功')
    return render_to_response('testEmail.html',RequestContext(request))

from django.core.mail import send_mail
def send(req):
    #try:
       send_mail('Test', 'This is a test', 'guyuanjun92@163.com', ['1422297148@qq.com'],fail_silently=False)
       return HttpResponse(u'发送邮件成功')
    #except:
    #   return HttpResponse(u'发送邮件失败')

import smtplib
import string
def smtpSendEmail(req):
    smtp=smtplib.SMTP("admin@qq.com")
    smtp.login("admin@qq.com","admin")
    smtp.noop()
    From = "1422297148@qq.com"
    TO = "1422297148@qq.com"
    SUBJECT = 'HELLO'
    BODY='hello,python'

    body=string.join(("From: %s"%From,"TO: %s"%TO,"Subject: %s"%SUBJECT,"",BODY),"\r\n")
    print(body)
    smtp.sendmail(From,[TO],body)
    smtp.quit()


from django.core.mail import EmailMessage
from django.template import loader
from B2B_v1.settings import EMAIL_HOST_USER   #项目配置邮件地址，请参考发送普通邮件部分

import time

def send_html_mail(subject, content, recipient_list):
    html_content = loader.render_to_string(
                        'mail_template.html',               #需要渲染的html模板
                        {
                            'name':content['name'],
                            'date':time.strftime("%Y-%m-%d %X",time.localtime()),    #参数
                            'info':content['info']
                        }
                   )
    msg = EmailMessage(subject, html_content, EMAIL_HOST_USER, recipient_list)
    msg.content_subtype = "html" # Main content is now text/html
    msg.send()

#send_html_mail(subject, html_content, [收件人列表])
def sendHtmlMail(req):
    send_html_mail('你有待审批工单', {'name':'zheng','info':'lvs vip申请'}, ['1422297148@qq.com',])