#coding=utf-8
from django.http import HttpResponse,HttpResponseRedirect
from myadmin.admin_tools import Admin_tools
from django.shortcuts import render
from myadmin.manage_deal import Deal
from first_page.views import handler500
from first_page.views import handler404
from django.views.decorators.csrf import csrf_exempt

mDeal = Deal()

#管理成交
@csrf_exempt
def manage_deal(req):
    mTools = Admin_tools()
    admin_id = mTools.getSession(req, 'admin_id')
    if admin_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == "POST":
        seller_merchant_id = req.POST.get('seller_merchant_id',0)
        buyer_merchant_id = req.POST.get('buyer_merchant_id',0)
        car_id = req.POST.get('car_id',0)
        deal_price = req.POST.get('deal_price',0.0)

        seller_merchant_id = 1
        buyer_merchant_id = 1
        car_id = 1
        result = mDeal.insert_deal_table(seller_merchant_id, buyer_merchant_id, car_id, deal_price)
        if result == 0:
            return handler500(req)
        else:
           return HttpResponse(result)
           #context = {'user_list': result}
           #return render(req, 'admin/manage_deal.html', context)
    else:
        result = mDeal.get_all_user_info_list()
        if result == 0:
            return handler500(req)
        else:
           context = {'user_list': result}
           return render(req, 'admin/manage_deal.html', context)
        #return handler404(req)

#成交记录
@csrf_exempt
def deal_records(req):
    mTools = Admin_tools()
    admin_id = mTools.getSession(req, 'admin_id')
    if admin_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == "GET":
        result = mDeal.get_all_deal_records()
        if result == 0:
            return handler500(req)
        else:
           context = {'deal_record_list': result}
           return render(req, 'admin/deal_record_home.html', context)
    else:
        result = mDeal.get_all_user_info_list()
        if result == 0:
            return handler500(req)
        else:
           context = {'deal_record_list': result}
           return render(req, 'admin/deal_record_home.html', context)
        #return handler404(req)
