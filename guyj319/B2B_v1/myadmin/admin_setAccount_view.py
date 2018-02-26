#coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect
from myadmin.admin_tools import Admin_tools
from django.shortcuts import render
from myadmin.admin_setAccount import Set_account
from first_page.views import handler500
from first_page.views import handler404
from django.views.decorators.csrf import csrf_exempt
from myadmin.blackList import BlackList
from myadmin.admin_home import Home

mSet_account = Set_account()
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

#账号设置
@csrf_exempt
def set_account(req):
    mTools = Admin_tools()
    admin_id = mTools.getSession(req, 'admin_id')
    if admin_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    username = mSet_account.getUsername(admin_id)
    if username == 0:
        return handler500(req)

    if req.method == "POST":
        old_password = req.POST.get("old_password", None)
        new_password = req.POST.get("new_password", None)
        name = req.POST.get("name", None)

        result = mSet_account.setAccount2(username, name, old_password, new_password)
        if result == 0:
            return handler500(req)
        elif result == 1:
            return HttpResponse('用户不存在')
        elif result == 666:
            return HttpResponse("1")
    else:
        context = {"notice": notice, "account_name": username}
        return render(req, 'admin/setting/account_setting.html', context)

        context = {'account': username}
        return render(req, 'admin/set_account.html', context)


