#coding=utf-8
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from account.account_manage import Tools
from user.login.myLogout import Logout
from user.login.myLogin import Login
from user.register.registerHome import Register
from user.register.sendVerifyCode import Send_verify_code
from user.register.inviteCode import Invite_code
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from first_page.views import handler500
from first_page.views import handler404
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_GET
from user.LoginStatus import LoginStatus

mLogout = Logout()
mLogin = Login()
mRegister = Register()
mSend_verify_code = Send_verify_code()
mInvite_code = Invite_code()


#处理登录表单
# 使用ajax的post方式提交数据时必须添加装饰符 @csrf_exempt
#@require_POST
@csrf_exempt
def verify_login(req):
    if req.method == 'POST':
        #获取表单用户名和其密码
        user_name = req.POST.get('userName','')
        password = req.POST.get('password','')
        avoid_login = req.POST.get('avoidLogin','0') # 免登陆

        mTools = Tools()
        user_ip = mTools.get_client_ip(req) #获取用户的IP
        user_id = mLogin.login(user_ip, user_name, password) #返回0表示验证失败,返回1表示手机号或者密码有错；返回登录活动记录表的id表示登录成功,返回404表示登录被限制
        if user_id == LoginStatus.SERVER_ERROR: #服务器出错
            return handler500(req)
        elif user_id == LoginStatus.WRONG: #返回1表示手机号或者密码有错
            return HttpResponse('0')
        elif user_id == LoginStatus.ERROR_EXCEED: #登录时，错误次数超过6次，锁住IP，返回404
            return HttpResponse('2')
        elif user_id == LoginStatus.IS_BLACK: #该账号已经被拉黑
            return HttpResponse('3')
        else:            #验证成功
            #user_have_login = mTools.getSession(req,'phone')
            #if user_have_login == result:
            #     return HttpResponse('该用户已经登录，如果要重新登录，请先前往去退出该账号。')

            id = mLogin.activity_log(user_id, user_ip)
            if id == 0:
                return handler500(req)

            if avoid_login == '1':
                req.session.set_expiry(7*24*60*60) #一周免登陆

            req.session['user_id'] = user_id #建立一个会话
            req.session['login_id'] = id    #用来在退出时，找到相应的登录记录，从而修改登录退出的时间
            result = mLogout.timeout(id, user_id)  #假设会话过期
            if result == 0:
                return handler500(req)

            url=mTools.getSession(req, 'login_from')
            mTools.delSession(req, 'login_from')
            if url is None:
                url="/"   #重定向到首页
            #重定向到来源的url
            #return HttpResponseRedirect("/")
            return HttpResponse("1")
    else:
        return handler404(req)  #404 请求错误

#退出
def my_logout(req):
    mTools = Tools()
    user_id = mTools.getSession(req, 'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if user_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    login_id = mTools.getSession(req, 'login_id')

    result_code = mLogout.logout(login_id, user_id)
    if result_code == 0:
        return handler500(req)
    elif result_code == 666:
       mTools.delSession(req, 'user_id')
       mTools.delSession(req, 'login_id')
       return HttpResponseRedirect("/")

#处理邀请码表单
#@require_POST
@csrf_exempt
def verify_invitation_code(req):
     if req.method == 'POST':
        #获得表单数据
        invitationCode = req.POST.get('invitationCode','')

        mTools = Tools()
        user_ip = mTools.get_client_ip(req) #获取用户的IP
        phones = mInvite_code.mangageInviteCode(invitationCode, user_ip) #返回1表示邀请码过期，返回2表示邀请码不存在或者有错,返回3表示邀请码不能为空,返回404表示登录被限制
        if phones == 0:
            return handler500(req)
        elif phones == 1:  #邀请码过期
            return HttpResponse('0')
        elif phones == 2: #邀请码不存在或者有错
            return HttpResponse('0')
        elif phones == 3:  #邀请码不能为空
            return HttpResponse('0')
        elif phones == 404:
            #return render(req, 'limit.html', status=404)
            return HttpResponse('错误次数过多，稍后重试')
        else:  #邀请码验证成功
            req.session["phones"] = phones #建立一个会话，传递找到的符合条件的电话号码
            return HttpResponse('1')
     else:
         return handler404(req)  #404 请求错误

#@require_POST
@csrf_exempt
def send_phone_verify_code_post(request):
        # TODO:向register_phone_number手机号发送验证码
        # 状态码说明：
        # 1: 发送成功
        # 0: 发送失败

    if request.method == "POST":
        verifyCode = mSend_verify_code.getVerifyCode()
        register_phone_number = request.POST.get("registerPhoneNumber","")

        result = mSend_verify_code.sendVerifyCode(register_phone_number, verifyCode)
        if result == True: #成功发送验证码
            request.session['verifyCode'] = verifyCode #将验证码保存到session中
            return HttpResponse("1")
        else:  #发送验证码失败
            return HttpResponse('0')
    else:
         return handler404(request)  #404 请求错误

#处理注册表单
@require_POST
@csrf_exempt
def verify_register(req):
    if req.method == 'POST': #点击注册按钮，需要全面检查
        mTools = Tools()

        user_name = req.POST.get('userName','')
        phone = req.POST.get('registerPhoneNumber','')
        password = req.POST.get('password','')
        myverifyCode = req.POST.get('verifyCode',None) #获取表单的验证码

        #验证码验证
        verifyCode = mTools.getSession(req, 'verifyCode') #获取会话的验证码
        if myverifyCode != verifyCode: #验证码不对
            return HttpResponse('0')
        else:
            mTools.delSession(req, 'verifyCode')

        phones = mTools.getSession(req, "phones")
        flag = False
        for i in range(len(phones)): #判断输入的电话号码是否是受到了邀请
            if phones[i] == phone:
                flag = True
                break
        if flag == False:  #电话号码不存在,返回1.没有受到邀请（尽管邀请码正确，但是可能是看到别人的或者猜中的）
            return HttpResponse('0')

        user_ip = mTools.get_client_ip(req) #获取用户的IP
        user_id = mRegister.register(user_name, phone, password, user_ip) #调用该函数处理这个url.数据库出错，返回0；用户已经存在，返回1；成功则返回用户的id
        if user_id == 0:
            return handler500(req)
        elif user_id == -1: #用户已经存在
            return HttpResponse('0')
        else:
            mTools.delSession(req, 'phones')     #数据传递完毕，删除该会话
            mTools.delSession(req, 'verifyCode') #验证完毕，删除该验证码会话

            login_id = mRegister.finishRegister(user_ip, user_id) #调用这个函数来记录用户注册成功后的活动记录，与记录登录活动记录一样
            if login_id == 0:
                return handler500(req)
            else:
                req.session['user_id'] = user_id        #建立一个会话
                req.session['login_id'] = login_id    #用来在退出时，找到相应的登录记录，从而修改登录退出的时间
                return HttpResponse('1')
    else:
         return handler404(req)  #404 请求错误

#会话超时
def session_exceed_time(req):
    if req.method == 'GET':
        req.session['login_from'] = req.META.get('HTTP_REFERER', '/') #记住来源的url，如果没有则设置为首页('/')
        return render(req, "session_exceed_time.html")
    else:
        if 'sure' in req.POST:
            mTools = Tools()
            mTools.delSession(req, 'user_id')
            mTools.delSession(req, 'login_id')
            return HttpResponseRedirect('/')

def mylogin(req):
    if req.method == 'POST': #点击注册按钮
        name = req.POST.get('username','')
        pw = req.POST.get('password','')
        print(name)
        print(pw)
        return HttpResponse('1')
    else:
        return HttpResponse('0')