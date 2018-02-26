#coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect
from myadmin.admin_tools import Admin_tools
from django.shortcuts import render
from myadmin.admin_login import Login
from myadmin.admin_logout import Logout
from myadmin.admin_home import Home
from myadmin.admin_search import Admin_search
from first_page.views import handler500
from first_page.views import handler404
from django.views.decorators.csrf import csrf_exempt

from myadmin.blackList import BlackList
from account.my_friends.inviteFriend import Invite_friends
import time
mInvite_friends = Invite_friends()

mLogin = Login()
mLogout = Logout()
mHome = Home()
mAdmin_search = Admin_search()
mBlackList = BlackList()

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
#登录
@csrf_exempt
def admin_login(req):
    if req.method == 'POST':
        #获取表单用户名和其密码
        username = req.POST.get('user_name', None)
        password = req.POST.get('password', None)

        mTools = Admin_tools()
        user_ip = mTools.get_client_ip(req) #获取用户的IP
        admin_id = mLogin.login(user_ip, username, password) #返回0表示验证失败,返回1表示手机号或者密码有错；返回登录活动记录表的id表示登录成功,返回404表示登录被限制
        if admin_id == 0:
            return handler500(req)
        elif admin_id == -1: #返回1表示手机号或者密码有错
            return HttpResponse('0')
        elif admin_id == -404: #登录时，错误次数超过6次，锁住IP，返回404
            return HttpResponse('2')
        else:            #验证成功
            id = mLogin.activity_log(admin_id, user_ip)
            if id == 0:
                return handler500(req)
            req.session['admin_id'] = admin_id      #建立一个会话，该管理员的id
            req.session['admin_login_id'] = id    #用来在退出时，找到相应的登录记录，从而修改登录退出的时间
            #return HttpResponseRedirect('/adminHome/')   #转向登录成功后的页面
            return HttpResponse('1')
    else:    #GET请求
       return render(req, 'admin/home/login.html')

#退出
@csrf_exempt
def admin_logout(req):
    mAdmin_tools = Admin_tools()
    admin_id = mAdmin_tools.getSession(req, 'admin_id')
    if admin_id is None:
        return HttpResponseRedirect('/sessionExceedTime/')
    if req.method == 'POST':
        action = req.POST.get('action', '0')
        if action == '1':
            admin_login_id = mAdmin_tools.getSession(req, 'admin_login_id')

            result_code = mLogout.logout(admin_login_id, admin_id)
            if result_code == 0:
                return handler500(req)
            elif result_code == 666:
               mAdmin_tools.delSession(req,'admin_id')
               mAdmin_tools.delSession(req,'admin_login_id')
               return HttpResponse("1")
               #return HttpResponseRedirect("/adminLogin/")
        else:
            return HttpResponse("0")
    else:
        return handler404(req)

#主页
@csrf_exempt
def admin_home(req):
    mTools = Admin_tools()
    admin_id = mTools.getSession(req,'admin_id')
    if admin_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == "GET":
        context = {"notice": notice}
        return render(req, 'admin/common/base.html', context)

        result = mHome.is_super_admin(admin_id)
        if result == 0:
            return handler500(req)
        elif result == 1:
            is_super_admin = False
        else:
            is_super_admin = True
        context = {'is_super_admin': is_super_admin}
        return render(req, 'admin/home.html', context)
    else:
        return handler404(req)

#邀请好友
@csrf_exempt
def admin_invite_friend(req):
    mTools = Admin_tools()
    admin_id = mTools.getSession(req, 'admin_id')
    if admin_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'POST':
             #获得当前时间时间戳
             now_time = int(time.time())  #这是时间戳，即将当前时间转换为的毫秒数
             last_time = mTools.getSession(req,'last_time')
             if last_time is not None:
                  if (now_time-last_time) < (1*60*1000): #1分钟
                      req.session['last_time'] = now_time
                      return HttpResponse('2')     #操作过于频繁
                  else:
                      req.session['last_time'] = now_time
             else:
                 req.session['last_time'] = now_time

             mobiles = req.POST.getlist("phoneNumberList[]")

             current_user_phone_number = 'admin'
             result = mInvite_friends.inviteFriend(current_user_phone_number, mobiles) #调用这个函数处理当前用户输入的电话号码
             if result == 0:
                 return handler500(req) #更新或者插入邀请码出错
             else:
                success = result['success']
                fail = result['fail']
                return HttpResponse('1')

    else: #get请求
       context = {"is_login": True}
       return render(req, "sendInvitationCode.html", context)

#搜索
def keyword_search(req):
    mTools = Admin_tools()
    admin_id = mTools.getSession(req, 'admin_id')
    if admin_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == "POST":
        condition = {}
        condition['user_company_name'] = req.POST.get('user_company_name', None)
        condition['user_type'] = req.POST.get('user_type', None)
        condition['user_trademark'] = req.POST.get('user_trademark', None)
        condition['province'] = req.POST.get('province', None)
        condition['city'] = req.POST.get('city', None)

        condition['user_name'] = req.POST.get('user_name', None)
        condition['user_phone'] = req.POST.get('user_phone', None)

        result_list = mAdmin_search.OneWordGetData(condition)
        if result_list == 0:
            return handler500(req)
        else:
            req.session['search_datas'] = result_list
            req.session['length_search_datas'] = len(result_list)
        return HttpResponseRedirect("/viewSearch/")
    else:
        return handler404(req)

def view_search(req):
    mTools = Admin_tools()
    admin_id = mTools.getSession(req, 'admin_id')
    if admin_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == "GET":
        data = get_result_search(req)

        merchant_id_list = data.get('results','')
        allPage = data.get('allPage', '1')  #总页数
        curPage = data.get('curPage', '1')  #获取处理后的当前页数

        user_infos_piece = mAdmin_search.findMerchant(merchant_id_list)
        context = {"allPage":allPage,
                "curPage":curPage,
               "result_list": user_infos_piece}
        return context #返回所需要的数据
        #return render(req, template, context)
    else:
        return handler404(req)

def get_result_search(req):
    mTools = Admin_tools()
    admin_id = mTools.getSession(req, 'admin_id')
    if admin_id is None:
        return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'GET':
        pageType = req.GET.get('pageType', '')
        curPage = int(req.GET.get('curPage', '1'))
        allPage = int(req.GET.get('allPage', '1'))

        user_infos_piece = mTools.getSession(req, 'search_datas')
        length_user_infos_piece = mTools.getSession(req, 'length_search_datas')

        data = mAdmin_search.searchPaging(user_infos_piece, length_user_infos_piece, curPage, allPage, pageType)
        return data
    else:
        return handler404(req)

