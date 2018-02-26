#coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect
from myadmin.admin_tools import Admin_tools
from django.shortcuts import render
from myadmin.allVIP import VIP
from first_page.views import handler500
from first_page.views import handler404
from django.views.decorators.csrf import csrf_exempt
from myadmin.blackList import BlackList
from myadmin.admin_home import Home

mVIP = VIP()
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

#全部会员
@csrf_exempt
def all_vip_home(req):
    mTools = Admin_tools()
    admin_id = mTools.getSession(req, 'admin_id')
    if admin_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == "GET":
        member_list = mVIP.get_vip_list()
        if member_list == 0:
            return handler500(req)
        else:
            context = {"notice": notice,
                       "member_list": member_list}
            return render(req, "admin/member/member_list.html", context)

        result = mVIP.get_vip_list()
        if result == 0:
            return handler500(req)
        else:
           context = {'vip_list': result}
           return render(req, 'admin/all_vip_home.html', context)
    else:
        return handler404(req)

@csrf_exempt
def edit_vip_in_all_vip(req):
    mTools = Admin_tools()
    admin_id = mTools.getSession(req, 'admin_id')
    if admin_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'POST':
        trademark = req.POST.get('trademark', 0)
        operation_id = req.POST.get('operation_id', 0)

        operation_id = 1 #假设为1先
        condition = {}
        condition['trademark'] = trademark
        result = mVIP.edit_vip(operation_id, condition)
        if result == 0:
            return handler500(req)
        elif result == 666:
            return HttpResponseRedirect('/allVipHome/')
    else:
        operation_id = req.GET.get('operation_id', 0)
        result = mVIP.preview_vip(operation_id)
        if result == 0:
            return handler500(req)
        else:
           context = {'vip_info': result}
           return render(req, 'admin/edit_vip.html', context)
        #return handler404(req)

@csrf_exempt
def black_vip_in_all_vip(req):
    mTools = Admin_tools()
    admin_id = mTools.getSession(req, 'admin_id')
    if admin_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'GET':
        operation_id = req.GET.get('operation_id', 0)
        result = mVIP.black_vip(operation_id)
        if result == 0:
            return handler500(req)
        elif result == 666:
            return HttpResponseRedirect('/allVipHome/')
    else:
        return handler404(req)

@csrf_exempt
def delete_vip_in_all_vip(req):
    mTools = Admin_tools()
    admin_id = mTools.getSession(req, 'admin_id')
    if admin_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'GET':
        delete_type = req.GET.get('delete_type', '0')

        if delete_type == '0':   #一个个删除
            operation_id = req.GET.get('operation_id', 0)
            result = mVIP.delete_vip_one_by_one(operation_id)
        elif delete_type == '1': #批量删除
            operation_id_list = req.GET.getlist("operationIdList[]")
            result = mVIP.delete_vip_some(operation_id_list)
        else: #全部删除
            result = mVIP.delete_vip_all()

        if result == 0:
            return handler500(req)
        elif result == 666:
            return HttpResponseRedirect('/allVipHome/')
    else:
        return handler404(req)

#会员审核
@csrf_exempt
def vip_check_home(req):
    mTools = Admin_tools()
    admin_id = mTools.getSession(req, 'admin_id')
    if admin_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == "GET":
        context = {"notice": notice}
        return render(req, "admin/member/member_audit.html", context)


        result = mVIP.get_vip_list()
        if result == 0:
            return handler500(req)
        else:
           context = {'vip_list': result}
           return render(req, 'admin/vip_home.html', context)
    else:
        return handler404(req)

@csrf_exempt
def preview_vip(req):
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
            context = {'vip_info': result}
            return render(req, 'admin/preview_vip.html', context)
        #return handler404(req)

