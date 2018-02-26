#coding=utf-8
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from account.account_manage import Tools
from demand.my_demands import My_demands
from demand.modify_demands import Modify_demands
from first_page.views import handler500
from first_page.views import handler404

mMy_demands = My_demands()
mModify_demands = Modify_demands()

#处理我的需求页面内容 =================================================================================================================================
@csrf_exempt
def my_demand(req):
    mTools = Tools()
    user_id = mTools.getSession(req,'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if user_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    brand_list = ["路虎", "法拉利", "劳斯莱斯"]
    car_series_list = ["SUV", "中规车", "越野车"]

    if req.method == 'GET':
        record_list = mMy_demands.searchMyDemands(user_id) #调用这个函数来查询我的需求
        if record_list == 0:
            return handler500(req) #查询我的需求失败

        context = {"is_login": True,
               "demand_list": record_list,
               "brand_list": brand_list,
               "car_series_list": car_series_list}
        return render(req, "myDemand.html", context)

    else:
        actionType = req.POST.get('actionType',None)
        demandId = req.POST.get('demandId',None)
        if actionType is not None:
           if actionType == '0':
               if demandId is not None:
                  return delete_demand(req, demandId) #删除我的需求
               else:
                   return HttpResponse('0')
           elif actionType == '1':
               return update_record(req, user_id) #修改我的需求
        else:
           return handler404(req)  #404 请求错误

#删除我的需求
@csrf_exempt
def delete_demand(req, operation_id):
    if req.method == 'POST':
        result_code = mMy_demands.deleteMyDemand(operation_id) #调用这个函数来删除我的需求
        if result_code == 0:
            return handler500(req) #删除我的需求失败
        elif result_code == 666:
            return HttpResponse("1")
    else:
        return handler404(req) #404 请求错误

#更新我的需求 =================================================================================================================================
@csrf_exempt
def update_record(req, user_id):
    if req.method == 'POST':
        #表示要保存 刚刚在编辑页面 编辑的我的搜索，其实是将数据库里面的相应记录就行一次更新
        #update_record_list = req.POST.getList('update_record_list[]','')
        condition = getDtaFromForm(req)

        result_code = mModify_demands.updateRecord(user_id, condition)#根据用户输入的修改条件进行修改
        if result_code == 0:
            return HttpResponse("0")
            #return handler500(req) #更新我的搜索失败
        elif result_code == 666:
            return HttpResponse("1")
            #return HttpResponseRedirect('/myDemand/') #返回我的需求界面
    else:
        return handler404(req) #404 请求错误

def getDtaFromForm(req):
        condition = {}
        condition['demand_id'] = req.POST.get("demand_id",'')
        condition['car_type'] = req.POST.get("type",'') #车辆类型

        condition['car_brand'] = req.POST.get("brand",'')             #品牌
        condition['car_series'] = req.POST.get("series",'')           #车系
        condition['car_model'] = req.POST.get("car_model",'')         #车款

        condition['lowest_price'] = req.POST.get("lowest_price",'')
        condition['highest_price'] = req.POST.get("highest_price",'')

        condition['sell_area'] = req.POST.get("region",'')
        condition['pay_method'] = req.POST.get("payment",'')
        condition['delivery_type'] = req.POST.get("delivery_type",'')
        condition['color'] = req.POST.get("color",'')
        condition['method_logistics'] = req.POST.get("logistics",'')

        condition['expiry_date[year]'] = req.POST.get("expiry_date[year]",'')
        condition['expiry_date[month]'] = req.POST.get("expiry_date[month]",'')
        condition['expiry_date[day]'] = req.POST.get("expiry_date[day]",'')
        return condition

#没有用的
@csrf_exempt
def modify_demand(req,operation_id):
    mTools = Tools()
    user_id = mTools.getSession(req,'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if user_id is None:
      return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'POST':
       record_list = mModify_demands.getRecord(operation_id, user_id) #调用这个函数来获取用户要修改的需求
       if record_list == 0:
           return handler500(req) #查询失败
       else:
          return HttpResponse('1')
    else:
        return handler404(req) #404 请求错误
