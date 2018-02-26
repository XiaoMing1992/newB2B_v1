# -*- coding: utf-8 -*-
import urllib.request
import json
from django.http import HttpResponseBadRequest
import urllib,hashlib
import xml.etree.ElementTree as ET
from weixin.models import weiXinUser
from account.account_manage import LoginBackend
import time
from django.template import Context, loader
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from account.account_manage import Tools
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from first_page.views import handler500
from user.login.myLogin import Login

TOKEN='weixin'
AppID='wxda0ddf251ae0372b'
AppSecret='db908edfa2dde9582f04c9d17155a167'
access_token=''

myToken='root'
valid_time_interval=15*60*1000  #链接有效时间间隔毫秒数，现在设定为15分钟

global_from_user = ''

mLogin = Login()

def token():
  url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (AppID,AppSecret)
  result = urllib.request.urlopen(url).read().decode()
  access_token = json.loads(result).get('access_token')
  return access_token

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

@csrf_exempt
def login(req):
    if req.method == "POST":
        #获取表单用户名和其密码
        user_name = req.POST.get('userName','')
        password = req.POST.get('password','')

        mTools = Tools()
        user_ip = mTools.get_client_ip(req) #获取用户的IP
        result = mLogin.login(user_ip,user_name,password) #返回0表示验证失败,返回1表示手机号或者密码有错；返回登录活动记录表的id表示登录成功,返回404表示登录被限制
        if result == 0:
            return handler500(req)
        elif result == 1: #返回1表示手机号或者密码有错
            return HttpResponse('0')
        elif result == 404:
            return render(req, 'limit.html', status=404)
        else:            #验证成功
            try:
                  wei_xin_users = weiXinUser.objects.filter(openid=global_from_user)
                  if not wei_xin_users:  #没有通过用户OpenID和系统用户进行绑定
                     wei_xin_user = weiXinUser.objects.create(openid=global_from_user,phone=user_name)  #绑定微信用户和系统用户
            except:
                 return HttpResponse('0')

            return HttpResponse('1')
    else:
       return render(req,'weixin/login.html')

def setOpenId(from_user):
    global_from_user = from_user

def getOpenId():
    return global_from_user

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

developer_weixin = 'gh_d66381a964d8' #开发者的微信号
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

           setOpenId(from_user)

           if msg_type == 'event':
               event_name = xml.find('Event').text         #事件类型，CLICK
               if event_name == 'subscribe':
                   re_content = u'您好，欢迎关注车栈，我们致力于为您提供我们优质的服务。'
                   t = loader.get_template('reply_text.xml')
                   c = {
                        'toUser' : from_user,
                        'fromUser' : to_user,
                        'content' : re_content
                   }
                   result = t.render(Context(c))
               #elif event_name == 'CLICK':
               #   event_key = xml.find('EventKey').text       #事件KEY值，与自定义菜单接口中KEY值对应
               #   if event_key=='demand':
                      #return toUser(request,from_user) #

               #       re_content = u'点击我的需求'
               #       t = loader.get_template('reply_text.xml')
               #       c = {
               #         'toUser' : from_user,
               #         'fromUser' : to_user,
               #         'content' : re_content
               #       }
               #       result = t.render(Context(c))

               #   elif event_key=='car':
               #       re_content = u'点击我的发布'
               #       t = loader.get_template('reply_text.xml')
               #       c = {
               #         'toUser' : from_user,
               #         'fromUser' : to_user,
               #         'content' : re_content
               #       }
               #       result = t.render(Context(c))

               #try:
               #   wei_xin_users = weiXinUser.objects.filter(openid = from_user)
               #   if not wei_xin_users:  #没有通过用户OpenID和系统用户进行绑定
               #      wei_xin_user = weiXinUser.objects.create(openid =from_user)  #绑定微信用户和系统用户
               #except:
                  #return HttpResponseBadRequest("签名无效")
               #   goto = True

           else:
               return toUser(from_user)

               re_content = u'您好，欢迎使用！'
               t = loader.get_template('reply_text.xml')
               c = {
                        'toUser' : from_user,
                        'fromUser' : to_user,
                        'content' : re_content
               }
               result = t.render(Context(c))
           return HttpResponse(result)

           wei_xin_users = weiXinUser.objects.filter(openid = from_user)
           if not wei_xin_users:  #没有通过用户OpenID和系统用户进行绑定
               open_id=from_user

               #获得当前时间时间戳
               timestamp = int(time.time())  #这是时间戳，即将当前时间转换为的毫秒数

               my_token=myToken #***注意*** 不是微信公众平台里面的token
               signature=makeSignature(my_token,open_id,timestamp)#生成签名

               url=makeLink(open_id,timestamp,signature)
               return HttpResponseRedirect(url)
           else:
                wei_xin_user = wei_xin_users[0]

           if msg_type == 'event':
              if event_name == 'CLICK':
                  if event_key=='demand':
                      return HttpResponseRedirect("http://www.panxl.cn/")
                  elif event_key=='car':
                      return HttpResponseRedirect("http://www.panxl.cn/")
           return HttpResponseRedirect("http://www.panxl.cn/")

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


def makeLink(open_id,timestamp,signature):
    '''
    :param open_id:
    :param timestamp:
    :param signature:
    :return:
     1. 用户OpenID：因为你需要在绑定页面中取到是哪个微信用户想要绑定系统用户。
     2. 时间戳timestamp：这是为了防止链接泄漏出去被恶意利用，具体来说就是一个你指定的过期时间，超过这个时间这个链接就失效了，用户只能再次获取。
     3. 签名signature：这是为了保证此验证链接只有你才可能生成，用户及第三方均无法伪造。
    '''
    url="http://www.panxl.cn/login/?OpenID=%sandtimestamp=%sandsignature=%s"%(open_id,timestamp,signature)
    return url

def checkLinkSignature(request):
    if request.method=='GET':
        open_id = request.GET.get("OpenID",'')
        timestamp = request.GET.get("timestamp", '')
        signature=request.GET.get("signature", '')

        token = myToken #***注意*** 不是微信公众平台里面的token
        tmpList = [token,open_id,timestamp]
        tmpList.sort()
        tmpstr = "%s%s%s" % tuple(tmpList)
        tmpstr =tmpstr.encode("utf-8")        #注意一下
        tmpstr = hashlib.sha1(tmpstr).hexdigest()
        if tmpstr == signature:  #签名有效
            timestamp=int(timestamp)  #链接中的有效时间戳，字符串转变为 int 型
            now_timestamp=int(time.time())  #这是时间戳，即将当前时间转换为的毫秒数
            if (valid_time_interval+timestamp)<=now_timestamp: #链接没有过期
                 request.session['openID']=open_id
                 return render(request,"login.html")
            else:  #链接过期，返回微信重新验证
                return HttpResponse("链接过期")
        else:
            #签名无效，返回微信重新验证
            return HttpResponseBadRequest("签名无效")
    else:
        if 'openID' in request.session:
            del request.session['openID']
            open_id=request.session['openID']
            phone=request.POST.get("phone", '')
            password=request.POST.get("password", '')
            result=handlerLogin(request,open_id,phone,password)
            if result==True:
                return HttpResponse('验证成功，返回微信可以继续操作哦')
            else:
                return HttpResponseBadRequest("验证失败，返回微信重新验证")
        else:
            return HttpResponseBadRequest("验证失败，返回微信重新验证")

def handlerLogin(open_id,phone,password):
    #TODO 处理登录验证
    mLoginBackend=LoginBackend()
    user=mLoginBackend.authenticate(phone=phone,password=password) #调用其验证函数验证用户是否输入正确
    if user is not None:
        try:
            weiXinUser.objects.create(openid=open_id,phone=phone)  #绑定微信用户和系统用户
            return True
        except:
            return False
    else:
        return False