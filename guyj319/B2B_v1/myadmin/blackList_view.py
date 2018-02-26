#coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect
from myadmin.admin_tools import Admin_tools
from django.shortcuts import render
from myadmin.blackList import BlackList
from first_page.views import handler500
from first_page.views import handler404
from django.views.decorators.csrf import csrf_exempt
from myadmin.admin_home import Home

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

#黑名单
@csrf_exempt
def black_list_home(req):
    mTools = Admin_tools()
    admin_id = mTools.getSession(req, 'admin_id')
    if admin_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == "GET":
        backlist = mBlackList.get_black_list()
        if backlist == 0:
            return handler500(req)
        else:
            context = {"notice": notice,
                   "backlist": backlist}
            return render(req, "admin/member/backlist.html", context)

        result = mBlackList.get_black_list()
        if result == 0:
            return handler500(req)
        else:
           context = {'black_list': result}
           return render(req, 'admin/black_list.html', context)
    else:
        return handler404(req)

@csrf_exempt
def delete_black(req):
    mTools = Admin_tools()
    admin_id = mTools.getSession(req,'admin_id')
    if admin_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'GET':
        delete_type = req.GET.get('delete_type', '0')

        if delete_type == '0':   #一个个删除
            operation_id = req.GET.get('operation_id', 0)
            result = mBlackList.delete_black_one_by_one(operation_id)
        elif delete_type == '1': #批量删除
            operation_id_list = req.GET.getlist("operationIdList[]")
            result = mBlackList.delete_black_some(operation_id_list)
        else: #全部删除
            result = mBlackList.delete_black_all()

        if result == 0:
            return handler500(req)
        elif result == 666:
            return HttpResponseRedirect('/blackList/')
    else:
        return handler404(req)
