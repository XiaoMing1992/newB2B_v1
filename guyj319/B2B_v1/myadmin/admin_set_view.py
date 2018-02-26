#coding=utf-8
from django.http import HttpResponse,HttpResponseRedirect
from myadmin.admin_tools import Admin_tools
from django.shortcuts import render
from myadmin.admin_set import Set_admin
from first_page.views import handler500
from first_page.views import handler404
from django.views.decorators.csrf import csrf_exempt
from myadmin.blackList import BlackList
from myadmin.admin_home import Home

mSet_admin = Set_admin()
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

#管理员设置
@csrf_exempt
def set_admin_home(req):
    mTools = Admin_tools()
    admin_id = mTools.getSession(req, 'admin_id')
    if admin_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == "GET":
        result = mSet_admin.search_admin_account()
        if result == 0:
            return handler500(req)
        else:
           context = {"notice": notice, "administrator_list": result}
           return render(req, 'admin/setting/administrator_setting.html', context)

        result = mSet_admin.search_admin_account()
        if result == 0:
            return handler500(req)
        else:
           context = {'admin_infos_list':result}
           return render(req, 'admin/set_admin_home.html',context)
    else:
        return handler404(req)

@csrf_exempt
def add_admin(req):
    mTools = Admin_tools()
    admin_id = mTools.getSession(req,'admin_id')
    if admin_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == "POST":
        user_name = req.POST.get("account", None)
        name = req.POST.get("name", None)
        password = req.POST.get("password", None)

        #againpassword = req.POST.get("againpassword", None)
        #if againpassword != password:
        #    return HttpResponse('两次密码不一样')

        result = mSet_admin.add_admin(user_name, name, password)
        if result == 0:
            return handler500(req)
        elif result == 1:
            return HttpResponse('账号已经存在，请设置其他账号')
        elif result == 666:
            return HttpResponse("1") #添加账号成功
    else:
        result = mSet_admin.search_admin_account()
        if result == 0:
            return handler500(req)
        else:
           context = {'admin_infos_list':result}
           return render(req, 'admin/add_admin.html',context)

@csrf_exempt
def delete_admin(req):
    mTools = Admin_tools()
    admin_id = mTools.getSession(req, 'admin_id')
    if admin_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'POST':
        operation_id = req.POST.get('id', 0)

        result = mSet_admin.delete_admin(operation_id)
        if result == 0:
            return HttpResponse("0") #删除该管理员失败
            #return handler500(req)
        elif result == 666:
            return HttpResponse("1") #删除该管理员成功
    else:
        return handler404(req)

@csrf_exempt
def modify_admin(req):
    mTools = Admin_tools()
    admin_id = mTools.getSession(req, 'admin_id')
    if admin_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == "POST":
        user_name = req.POST.get("account", None)
        name = req.POST.get("name", None)
        old_password = req.POST.get("oldpassword", None)
        new_password = req.POST.get("newpassword", None)

        againpassword = req.POST.get("againpassword", None)
        if againpassword != new_password:
            return HttpResponse('两次新密码不一样')

        result = mSet_admin.modify_adamin(user_name, name, old_password, new_password)
        if result == 0:
            return handler500(req)
        elif result == 1:
            return HttpResponse('用户不存在')
        elif result == 666:
            return HttpResponse('修改成功')
    else:
        return render(req, 'admin/modify_admin.html')

#超级管理员设置
@csrf_exempt
def set_super_admin_home(req):
    mTools = Admin_tools()
    admin_id = mTools.getSession(req, 'admin_id')
    if admin_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == "GET":
        result = mSet_admin.find_not_super_admins()
        if result == 0:
            return handler500(req)
        else:
           context = {'admin_infos_list': result}
           return render(req, 'admin/set_super_admin.html', context)
    else:
        return handler404(req)

@csrf_exempt
def set_super_admin(req):
    mTools = Admin_tools()
    admin_id = mTools.getSession(req,'admin_id')
    if admin_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'GET':
        operation_id = req.GET.get('operation_id', 0)

        result = mSet_admin.set_super_admin(operation_id)
        if result == 0:
            return handler500(req)
        elif result == 666:
            return HttpResponseRedirect('/setSuperAdminHome/')
    else:
        return handler404(req)