#coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect
from myadmin.admin_tools import Admin_tools
from django.shortcuts import render
from myadmin.allVIP import VIP
from myadmin.allContent import ContentHome
from first_page.views import handler500
from first_page.views import handler404
from django.views.decorators.csrf import csrf_exempt
from myadmin.blackList import BlackList
from myadmin.admin_home import Home

mVIP = VIP()
mContentHome = ContentHome()
mBlackList = BlackList()
mHome = Home()

#计算黑名单的个数
def get_black_list_num():
     black_list_num = mBlackList.get_black_list_num()
     if black_list_num == -1:
        return '...'
     return black_list_num

#计算注册的新用户的个数
def get_new_user_num():
     new_user_num = mHome.get_new_user_num()
     if new_user_num == -1:
        return '...'
     return new_user_num

notice = {"blacklist_total": get_black_list_num(),
          "new_user_total": get_new_user_num()}

#内容管理
@csrf_exempt
def content_home(req):
    mTools = Admin_tools()
    admin_id = mTools.getSession(req, 'admin_id')
    if admin_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')


    if req.method == "GET":
        content_list = mContentHome.content_list()
        if content_list == 0:
            return handler500(req)
        else:
            context = {"notice": notice, "content_list": content_list}
            return render(req, 'admin/content/content_list.html', context)

        result = mContentHome.content_list()
        if result == 0:
            return handler500(req)
        else:
           context = {'content_list': result}
           return render(req, 'admin/all_content_home.html', context)
    else:
        return handler404(req)

@csrf_exempt
def modify_vip_in_content(req):
    mTools = Admin_tools()
    admin_id = mTools.getSession(req, 'admin_id')
    if admin_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'POST':
        state = req.POST.get('check', 0)
        operation_id = req.POST.get('check', 0)

        result = mVIP.check_vip(operation_id, state)
        if result == 0:
            return handler500(req)
        elif result == 666:
            return HttpResponseRedirect('/vipCheckHome/')
    else:
        operation_id = req.GET.get('operation_id', 0)
        result = mVIP.preview_vip(operation_id)
        if result == 0:
            return handler500(req)
        else:
            context = {'vip_info':result}
            return render(req, 'admin/modify_vip_in_content.html', context)
        #return handler404(req)

@csrf_exempt
def delete_vip_in_content(req):
    mTools = Admin_tools()
    admin_id = mTools.getSession(req, 'admin_id')
    if admin_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'GET':
        delete_type = req.GET.get('delete_type', '0')

        if delete_type == '0':   #一个个删除
            operation_id = req.GET.get('operation_id', 0)
            result = mContentHome.delete_vip_one_by_one(operation_id)
        elif delete_type == '1': #批量删除
            operation_id_list = req.GET.getlist("operationIdList[]")
            result = mContentHome.delete_vip_some(operation_id_list)
        else: #全部删除
            result = mContentHome.delete_vip_all()

        if result == 0:
            return handler500(req)
        elif result == 666:
            return HttpResponseRedirect('/contentHome/')
    else:
        return handler404(req)
