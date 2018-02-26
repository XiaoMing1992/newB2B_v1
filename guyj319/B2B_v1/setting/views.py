#coding=utf-8
from setting.changePW import Change_password
from setting.changePhone import Change_phone
from setting.setHeadIcon import Set_head_icon
from setting.form import ImageUploadForm
from account.models import user_info_table

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from account.account_manage import Tools
from user.register.sendVerifyCode import Send_verify_code
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from first_page.views import handler500
from first_page.views import handler404

mChange_password = Change_password()
mChange_phone = Change_phone()
mSet_head_icon = Set_head_icon()
mSend_verify_code = Send_verify_code()

def setting(request):
    mTools = Tools()
    user_id = mTools.getSession(request,'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if user_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    context = {"is_login": True}
    return render(request, "setting.html", context)

@csrf_exempt
def setting_post(request):
    """
    验证输入的数据是否正确。如果正确返回1，否则返回0。
    """
    mTools = Tools()
    user_id = mTools.getSession(request,'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if user_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if request.method == "POST":
        old_password = request.POST.get("oldPassword",None)
        new_password = request.POST.get("newPassword",None)
        old_phone_number = request.POST.get("oldPhoneNumber",None)
        new_phone_number = request.POST.get("newPhoneNumber",None)
        current_password = request.POST.get("currentPassword",None)
        newPhoneNumberExist = request.POST.get("newPhoneNumberExist",None)

        # TODO:验证其中一项信息
        if old_password is not None:
           result_code = mChange_password.checkPassword(user_id, old_password)
           if result_code == 666:
              return HttpResponse("1")
           elif result_code == 0:
              return handler500(request)

        if new_password is not None:
            result_code = mChange_password.changePassword(user_id, new_password)
            if result_code == 666:
                return HttpResponse("1")

        #修改AI手机
        if current_password is not None:
           result_code = mChange_password.checkPassword(user_id, current_password)
           if result_code == 666:
            return HttpResponse("1")

        if old_phone_number is not None:
            result_code = mChange_phone.checkPhone(old_phone_number)
            if result_code == 666:
               return HttpResponse("1")

        if newPhoneNumberExist is not None:
            result_code = mChange_phone.newPhoneIsExist(newPhoneNumberExist)
            if result_code == 666: #查询到存在该手机号
               return HttpResponse("2") #该手机号已经被注册

        if new_phone_number is not None:
            result_code = mChange_phone.changePhone(user_id, new_phone_number)
            if result_code == 666:
               request.session['phone'] = new_phone_number
               return HttpResponse("1")

        return HttpResponse("0")
    else:
        return handler404(request)

@csrf_exempt
def send_phone_verify_code_post(request):
        # TODO:向手机号发送验证码a
        # 状态码说明：
        # 1: 发送成功
        # 0: 发送失败

    if request.method == "POST":
        verifyCode = mSend_verify_code.getVerifyCode()
        oldPhone = request.POST.get("phoneNumber","")

        result = mSend_verify_code.sendVerifyCode(oldPhone,verifyCode)
        if result == True: #成功发送验证码
            request.session['changePhoneVerifyCode'] = verifyCode #将验证码保存到session中
            return HttpResponse("1")
        else:  #发送验证码失败
            return HttpResponse('0')
    else:
        return handler404(request)  #404 请求错误

@csrf_exempt
def verify_code_post(request):
    mTools = Tools()
    user_id = mTools.getSession(request,'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if user_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if request.method == "POST":
        verify_code = request.POST.get("verifyCode",None)

        #验证码验证
        verifyCode = mTools.getSession(request,'changePhoneVerifyCode') #获取会话的验证码
        if verify_code != verifyCode: #验证码不对
             return HttpResponse('0')
        else:
            return HttpResponse("1")
    else:
        return handler404(request)  #404 请求错误

@csrf_exempt
def upload_pic(request):
    mTools = Tools()
    current_user_phone_number = mTools.getSession(request,'phone')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if current_user_phone_number is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if request.method == 'POST':
          form = ImageUploadForm(request.POST, request.FILES )  # 有文件上传要传如两个字段
          if form.is_valid():
              result_code = mSet_head_icon.setHeadIcon(current_user_phone_number,form.cleaned_data['image'])
              if result_code == 666:
                 return HttpResponse('image upload success')
              else:
                  return HttpResponse('image upload fail')
    else:
         context = {"is_login": True}
         return render(request, "setHeadIcon2.html", context)
    #return HttpResponseForbidden('allowed only via POST')

#=================================================================作废=============================================================
#处理上传头像照片 =================================================================================================================================
@csrf_exempt
def set_head_icon(req):
    mTools = Tools()
    user_id = mTools.getSession(req,'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if user_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'POST':#确定
        try:
            head_icon_path = mTools.upload_icon(req,user_id,'file_icon') #保存头像照片
            result_code = mSet_head_icon.setHeadIcon(user_id,head_icon_path) #调用这个函数来处理用户上传头像
            if result_code == 0:
                return handler500(req) #数据库更新出错
            elif result_code == 666:
                return HttpResponse("1")
        except:
            return HttpResponse("上传头像照片出错")
    else: # get 请求
         return render(req, "setHeadIcon.html")

#修改密码
@csrf_exempt
def change_password(request):
    mTools = Tools()
    current_user_phone_number = mTools.getSession(request,'current_user_phone_number')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if current_user_phone_number is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if request.method == 'POST':
        if 'saveButton' in request.POST:
            oldPassword = request.POST.get('oldPassword', '')
            newPassword = request.POST.get('newPassword', '')
            againPassword = request.POST.get('againPassword', '')

            #
            email = request.POST.get('email', '') #邮箱
            #
            result_code = mChange_password.changePassword(current_user_phone_number,oldPassword,newPassword,email) #调用这个函数处理用户旧密码验证以及旧密码修改
            if result_code == 0:
                return handler500(request) #数据库更新出错
            elif result_code == 1:
               context = {"is_login": True,'oldpassword_is_wrong':True,'phone':current_user_phone_number}
               return render(request, "setting.html", context)
            elif result_code == 666:
               context = {"is_login": True,'phone':current_user_phone_number,'changepwd_success':True,'picture':'images/temp/5.jpg'}
               return render(request, "setting.html", context)

    else:
         context = {"is_login": True,'phone':current_user_phone_number}
         return render(request, "setting.html", context)

#修改手机号 =================================================================================================================================
@csrf_exempt
def change_phone(request):
    mTools = Tools()
    current_user_phone_number = mTools.getSession(request,'current_user_phone_number')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if current_user_phone_number is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if request.method == 'POST':
        oldPhone = request.POST.get('oldPhoneNumber', '')
        newPhone = request.POST.get('newPhoneNumber', '')
        password = request.POST.get('password', '')
        myverifyCode = request.POST.get('verifyCode','') #获取表单的验证码

        #验证码验证
        verifyCode = mTools.getSession(request,'changePhoneVerifyCode') #获取会话的验证码
        if myverifyCode != verifyCode: #验证码不对
             return HttpResponse('0')

        result_code = mChange_phone.changePhone(oldPhone,password,newPhone) #调用这个函数处理用户旧密码验证以及旧密码修改
        if result_code == 0:
            return handler500(request) #数据库更新出错
        elif result_code == 1:
            context = {"is_login": True,'oldpassword_is_wrong':True,'phone':current_user_phone_number}
            return render(request, "setting.html", context)
        elif result_code == 666:
            context = {"is_login": True,'phone':current_user_phone_number,'success':True,'picture':'images/temp/5.jpg'}
            return render(request, "setting.html", context)

    else:
         context = {"is_login": True,'phone':current_user_phone_number}
         return render(request, "setting.html", context)
