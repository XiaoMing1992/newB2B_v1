# -*- coding: utf-8 -*-
import urllib.request
import json
from django.http import HttpResponseBadRequest
import urllib,hashlib
import xml.etree.ElementTree as ET
from weixin.models import weiXinUser
from account.account_manage import LoginBackend
import datetime
from django.template import Context, loader
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from account.account_manage import Tools
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from first_page.views import handler500
from user.login.myLogin import Login
#import requests

TOKEN='weixin'
AppID='wxda0ddf251ae0372b'
AppSecret='db908edfa2dde9582f04c9d17155a167'
access_token=''

###
global_from_user = ''
developer_weixin = 'gh_d66381a964d8' #开发者的微信号
mLogin = Login()

def token():
  url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (AppID,AppSecret)
  result = urllib.request.urlopen(url).read().decode()
  access_token = json.loads(result).get('access_token')
  return access_token

#通过授权来获取用户的openid
def getOpenidByOauth2(req):
  #获取state
  state = req.GET('state','777')
  #获取id，这个是用户在数据库里面的id
  id = req.GET('id','0')
  if state == '777':
      #scope=snsapi_base 表示应用授权作用域为 不弹出授权页面，直接跳转，只获取用户openid
      url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=http://www.panxl.cn/oauth2&response_type=code&scope=snsapi_base&state=%s#wechat_redirect' % (AppID,id)
      #url_code = urllib.request.urlopen(url).read().decode() #返回回调页面，如：http://israel.duapp.com?code=02a9bed29b2185a9f0ed3a48fe56e700&state=1
      url_code = urllib.request.urlopen(url) #返回回调页面，如：http://israel.duapp.com?code=02a9bed29b2185a9f0ed3a48fe56e700&state=1
  else:
     id = state #这个是用户在数据库里面的id
     #获取code
     code = req.GET('code')
     #再使用code获取OpenID
     url_openid = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" % (AppID,AppSecret,code)
     result_openid = urllib.request.urlopen(url_openid).read().decode()
     openid = json.loads(result_openid).get('openid')

     return bangding(id, openid)
     #return openid

def bangding(id,openid):
    try:
        wei_xin_users = weiXinUser.objects.filter(id=id)
        if not wei_xin_users:  #没有通过用户OpenID和系统用户进行绑定
            #绑定微信用户和系统用户
            wei_xin_users.openid = openid
            wei_xin_users.state = 1
            wei_xin_users.save()
        return HttpResponse('1')
    except:
        return HttpResponse('0')

#@login_required(login_url='/')
def createMenu(request):
  access_token=token()
  url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % access_token
  data = {
   "button":[
   {
      "type":"view",
      "name":"找车",
      "url":"http://www.autohome.com.cn/beijing/"
   },
   {
      "type":"view",
      "name":"发布车源",
      "url":"http://www.panxl.cn/login/"
   },
   {
      "type":"view",
      "name":"个人中心",
      "url":"http://www.panxl.cn/personalCenter/"
   }]}

  data=json.dumps(data,ensure_ascii=False).encode('utf-8') #加上参数ensure_ascii=False 后 提交的数据中的中文就不会再被转码，然后再编下UTF-8
  req = urllib.request.Request(url)
  req.add_header('Content-Type', 'application/json')
  req.add_header('encoding', 'utf-8')
  response = urllib.request.urlopen(url, data)
  result = response.read()
  return HttpResponse(result)


to_url = "http://www.pcauto.com.cn/"
template_id = "yBq7kAtnVl31PTYNtI2IoWcsVlwHHVMDawgKGFIDsOc"
open_id_1 = "o-liUv07HzlXlv7GMsXLuyNpUL14"
open_id_2 = "o-liUvy_e5qiisyu6S7qSsF6pu9U"
to_open_id = open_id_1

#发送模板消息
def handPushMessage(req):
    who = '小明'
    number = 2
    content = '劳斯莱斯，土豪金，20-30万'
    time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    remark = "点击查看"
    return pushMessage(to_open_id,template_id,to_url,who,number,content,time_str,remark)

def pushMessage(to_open_id,template_id,to_url,who,number,content,time_str,remark):
  access_token=token()

  url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s" % access_token
  data ={
           "touser":to_open_id,
           "template_id":template_id,
           "url":to_url,
           "topcolor":"#7B68EE",
           "data":{
                   "first": {
                       "value":"%s发布的需求收到了%s个匹配需求"%(who,number),
                       "color":"#173177"
                   },
                   "keynote1":{
                       "value":content,
                       "color":"#173177"
                   },
                   "keynote2": {
                       "value":time_str,
                       "color":"#173177"
                   },
                   #"keynote3": {
                   #    "value":"2014年9月22日",
                   #    "color":"#173177"
                   #},
                   "remark":{
                       "value":remark,
                       "color":"#173177"
                   }
           }
        }

  data=json.dumps(data,ensure_ascii=False).encode('utf-8') #加上参数ensure_ascii=False 后 提交的数据中的中文就不会再被转码，然后再编下UTF-8
  req = urllib.request.Request(url)
  req.add_header('Content-Type', 'application/json')
  req.add_header('encoding', 'utf-8')
  response = urllib.request.urlopen(url, data)
  result = response.read()
  return HttpResponse(result)

@csrf_exempt
def login(req):
    if req.method == "POST":
        #获取表单用户名和其密码
        user_name = req.POST.get('userName','')
        password = req.POST.get('password','')

        mTools = Tools()
        user_ip = mTools.get_client_ip(req) #获取用户的IP
        result = mLogin.login(user_ip,user_name,password)
        if result == 0:
            return handler500(req)
        elif result == 1: #返回1表示手机号或者密码有错
            return HttpResponse('0')
        elif result == 404: #登录时，错误次数超过6次，锁住IP，返回404
            return HttpResponse('2')
        else:            #验证成功
            try:
                wei_xin_users = weiXinUser.objects.filter(phone=result)
                if not wei_xin_users:  #没有通过用户OpenID和系统用户进行绑定
                   #绑定微信用户和系统用户
                   user = weiXinUser.objects.create(phone=result)
                   return HttpResponse(user.id)
                return HttpResponse('#')
            except:
               return HttpResponse('0')
    else:
       return render(req,'weixin/login.html')

@csrf_exempt
def personal_center(req):
    return render(req,'weixin/user.html')

@csrf_exempt
def register(req):
    return render(req,'register.html')

def checkWeiXinSignature(request):
    signature=request.GET.get("signature", '')
    timestamp = request.GET.get("timestamp", '')
    nonce = request.GET.get("nonce", '')

    token = TOKEN
    tmpList = [token,timestamp,nonce]
    tmpList.sort()
    tmpstr = "%s%s%s" % tuple(tmpList)
    tmpstr=tmpstr.encode("utf-8")       #注意一下
    tmpstr = hashlib.sha1(tmpstr).hexdigest()
    if tmpstr == signature:
        return True
    else:
        return False

@csrf_exempt
def toUser(from_user):
    #try:
    #    wei_xin_users = weiXinUser.objects.get(id=2)
    #    from_user = wei_xin_users.openid
    #except:
    #    return HttpResponseBadRequest("推送失败")

    re_content = u'推送信息给用户'
    t = loader.get_template('push_msg_text.xml')
    c = {
        'toUser' : from_user,
        'fromUser' : developer_weixin,
        'content' : re_content,
        'title': u'用户信息',
        'description': u'劳斯莱斯，土豪金，20-30万',
        'picurl':'http://mmbiz.qpic.cn/mmbiz/L4qjYtOibummHn90t1mnaibYiaR8ljyicF3MW7XX3BLp1qZgUb7CtZ0DxqYFI4uAQH1FWs3hUicpibjF0pOqLEQyDMlg/0',
		'url':'http://www.pcauto.com.cn/'

    }
    result = t.render(Context(c))
    return HttpResponse(result)

@csrf_exempt
def handleRequest(request):
    createMenu(request)  #创建菜单
    if request.method == 'GET':
        check_result=checkWeiXinSignature(request)
        if check_result==True: #验证成功
           echoStr = request.GET.get("echostr",None)
           return HttpResponse(echoStr,content_type="text/plain")
        return HttpResponseBadRequest('Verify Failed')

    else:
           str_xml = request.body
           xml = ET.fromstring(str_xml)

           to_user = xml.find('ToUserName').text       #开发者微信号
           from_user = xml.find('FromUserName').text   #发送方帐号（一个OpenID）
           msg_type = xml.find('MsgType').text         #消息类型，event

           dict_from_user = {}
           dict_from_user['openId'] = from_user

           if msg_type == 'event':
               event_name = xml.find('Event').text   #事件类型
               if event_name == 'subscribe':
                   re_content = u'您好，欢迎关注车栈，我们致力于为您提供我们优质的服务。'
                   t = loader.get_template('reply_text.xml')
                   c = {
                        'toUser' : from_user,
                        'fromUser' : to_user,
                        'content' : re_content
                   }
                   result = t.render(Context(c))

           else:
               re_content = u'您好，欢迎使用！'
               t = loader.get_template('reply_text.xml')
               c = {
                        'toUser' : from_user,
                        'fromUser' : to_user,
                        'content' : re_content
               }
               result = t.render(Context(c))
           return HttpResponse(result)

def makeSignature(token,open_id,timestamp):
    '''
    :param token:
    :param open_id:
    :param timestamp:
    :return:
     1. 将token、OpenID、timestamp三个参数进行字典序排序。
     2. 将三个参数字符串拼接成一个字符串进行sha1加密，得到链接的signature参数。
    '''

    tmpList = [token,open_id,timestamp]
    tmpList.sort()
    tmpstr = "%s%s%s" % tuple(tmpList)
    tmpstr =tmpstr.encode("utf-8")     #注意一下
    tmpstr = hashlib.sha1(tmpstr).hexdigest()
    return tmpstr