#coding=utf-8
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from account.account_manage import Tools
from message.myMessage import My_message
from first_page.views import handler500
from first_page.views import handler404
from django.views.decorators.cache import cache_control

#指定缓存是否需要总是检查新版本, 如果没有变化则仅传送缓存版本. (某些缓存即使服务器端页面变化也仅传递缓存版本--仅仅因为缓存拷贝尚未到期).
# 在这个例子里 cache_control 通知缓存每次检验缓存版本, 直到 600 秒到期:
#@cache_control(must_revalidate=True, max_age=600)

mMy_message = My_message()

#处理我的消息 =================================================================================================================================
@csrf_exempt
def my_message(req):
   mTools = Tools()
   user_id = mTools.getSession(req,'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
   if user_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

   if req.method == 'GET':
         record_dirct = mMy_message.manage_message(user_id) #调用manage_message()来获取我的消息记录
         if record_dirct == 0:
             return handler500(req) #查询我的消息失败
         message_list = record_dirct.get('message_list','')
         date_list = record_dirct.get('date_list','')
         context = {"is_login": True,'message_list':message_list,'date_list':date_list}
         return render(req, "myMessage.html", context)
   else: # POST 请求
       return handler404(req)  #404 请求错误

#删除我的需求
@csrf_exempt
def delete_message(req):
    '''
    删除我的消息
    :param req:
    :param operation_id:
    :return:
    '''
    mTools = Tools()
    current_user_phone_number = mTools.getSession(req,'phone')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if current_user_phone_number is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'POST':
         operation_id = req.POST.get('id',None)
         result_code = mMy_message.DeleteMyMessage(operation_id)

         if result_code == 0:
             return HttpResponse("0")
             #return handler500(req) #数据库删除失败
         elif result_code == 666:
             return HttpResponse("1")
             #context = {"is_login": True}
             #return render(req, "myDemand.html", context)
    else:
        return handler404(req) #404 请求错误
