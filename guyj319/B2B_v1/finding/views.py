#coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from account.account_manage import Tools
from finding.findPW import Find_password
from user.register.sendVerifyCode import Send_verify_code
from first_page.views import handler404
from finding.form import CaptachaTestForm

mFind_password = Find_password()
mSend_verify_code = Send_verify_code()

@csrf_exempt
def forget_password(request):
    if request.POST:
        form = CaptachaTestForm(request.POST)
        if form.is_valid():
            human = True
    else:
        form = CaptachaTestForm()
    context = {'form':form}
    return render(request, 'forgetPassword.html',context)

@csrf_exempt
def forget_password_post(request):
    if request.method == "POST":
        phone_number = request.POST.get("phoneNumber",None)
        verify_code = request.POST.get("verifyCode",None)
        new_password = request.POST.get("newPassword",None)
        print(phone_number)
        if phone_number is not None:
           result_code = mFind_password.phoneIsExist(phone_number)
           if result_code == 666:
              request.session['phoneSetPasswordByPhone'] = phone_number
              return send_phone_verify_code_post(request,phone_number)
              #return HttpResponse("1")
           elif result_code == 999:
              print('该用户已经被拉黑')
              return HttpResponse("该用户已经被拉黑")
              #return HttpResponse("1")
           else:
               return HttpResponse("0")

        if verify_code is not None:
            return verify_code_post(request, verify_code)
        if new_password is not None:
           return set_new_password_by_phone(request, new_password)

        return HttpResponse("0")
    else:
        return handler404(request)

#找回密码 =================================================================================================================================
@csrf_exempt
def send_phone_verify_code_post(request,phone):
        # TODO:向手机号发送验证码
    mTools = Tools()
    if request.method == "POST":
        verifyCode = mSend_verify_code.getVerifyCode()

        result = mSend_verify_code.sendVerifyCode(phone,verifyCode)
        if result==True: #成功发送验证码
            request.session['findingByPhoneVerifyCode'] = verifyCode #将验证码保存到session中
            return HttpResponse("1")
        else:            #发送验证码失败
            mTools.delSession(request,'phoneSetPasswordByPhone')
            return HttpResponse("0")
    else:
        return handler404(request)

@csrf_exempt
def verify_code_post(request,verify_code):
    mTools = Tools()
    if request.method == "POST":
        #验证码验证
        verifyCode = mTools.getSession(request,'findingByPhoneVerifyCode') #获取会话的验证码
        if verify_code != verifyCode: #验证码不对
             return HttpResponse('0')
        else:
            return HttpResponse("1")
    else:
        return handler404(request)  #404 请求错误

#通过电话号码来找回密码
@csrf_exempt
def set_new_password_by_phone(request,new_password):
    mTools = Tools()
    if request.method == "POST":
        #new_password = request.POST.get("newPassword",None)
        #if new_password is None:
        #    return HttpResponse("0")
        phone = mTools.getSession(request,'phoneSetPasswordByPhone')
        if phone is None:
            return HttpResponse("超时，请返回重新验证身份")

        result_code = mFind_password.findPWByPhone(phone,new_password) #调用这个函数来帮忙用户找回密码
        if result_code == 0:
            return HttpResponse("0")
        elif result_code == 666:
            mTools.delSession(request,'findingByPhoneVerifyCode')  #会话结束
            mTools.delSession(request,'phoneSetPasswordByPhone')  #会话结束
            return HttpResponse("1")
    else:
        return handler404(request)

#通过电话号码来找回密码
@csrf_exempt
def find_password_by_phone(request):
    if request.method == 'POST':
          phone = request.POST.get('phone','')
          newpassword = request.POST.get('newpassword1', '')
          myverifyCode = request.POST.get('verifyCode','') #获取表单的验证码

          mTools = Tools()
          #验证码验证
          verifyCode = mTools.getSession(request,'findingByPhoneVerifyCode') #获取会话的验证码
          if myverifyCode != verifyCode:
             context = {'wrong_verifyCode':True}
             return render(request, "forgetPassword.html", context)

          result_code = mFind_password.findPWByPhone(phone,newpassword) #调用这个函数来帮忙用户找回密码
          if result_code == 0:
             context = {'no_user':True}
             return render(request, "forgetPassword.html", context)

          elif result_code == 666:
             context = {'success':True}
             return render(request, "forgetPassword.html", context)  #重置成功，转向成功重置密码界面
    else:
        return render(request, "forgetPassword.html")

#通过邮箱来找回密码
#找回密码 =================================================================================================================================
@csrf_exempt
def send_email(request):
        # TODO:发送email
    if request.method == "POST":    #发送邮件
        verifyCode = mSend_verify_code.getVerifyCode() ######
        email = request.POST.get('email','')

        result = mSend_verify_code.sendVerifyCode(email,verifyCode)   #发送邮件，邮件里面含验证码
        if result == True: #成功发送邮件
            request.session['findingByEmailVerifyCode'] = verifyCode #将验证码保存到session中
            return HttpResponse("1")
        else:            #发送邮件失败
            return HttpResponse('0')
    else:
        return handler404(request)

@csrf_exempt
def find_password_by_email(request):
    if request.method == 'POST':
          mTools = Tools()

          email = request.POST.get('email','')
          newpassword = request.POST.get('newpassword1', '')
          newpassword2 = request.POST.get('newpassword2', '')
          myverifyCode = request.POST.get('verifyCode','') #获取表单的验证码

          #验证码验证
          verifyCode = mTools.getSession(request,'findingByEmailVerifyCode') #获取会话的验证码
          if myverifyCode != verifyCode:
             context = {'wrong_verifyCode':True}
             return render(request, "setting.html", context)

          result_code = mFind_password.findPWByEmail(email,newpassword) #调用这个函数来帮忙用户找回密码
          if result_code == 0:
             context = {'no_user':True}
             return render(request, "setting.html", context)
          elif result_code == 666:
             context = {'success':True}
             return render(request, "setting.html", context)  #重置成功，转向成功重置密码界面
    else:
        return render(request, "setting.html")
