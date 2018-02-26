#coding=utf-8
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from account.account_manage import Tools
from publish_car.publish_home import Publish_car
from django.shortcuts import render
from first_page.views import handler500
from first_page.views import handler404
from django.views.decorators.csrf import csrf_exempt

mPublish_car = Publish_car()

#处理发布车
def publish(req):
    mTools=Tools()
    user_id = mTools.getSession(req, 'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if user_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'POST': #提交
        publish_info = getFormData(req) #获取表单数据
        req.session['publish_info'] = publish_info #建立一个会话，传递数据

        context ={"is_login": True, 'source_detail_list': publish_info}
        return render(req, "publish.html", context)

    else:
        #先检查该用户是否具备发布车的权限a
        #try:
        #    user=audit_table.objects.get(phone=current_user_phone_number)
        #    if user.license != 1 or user.IDcard != 1:
        #        return HttpResponseRedirect('/publish_car/no_permisson/')
        #except:
        #    return HttpResponseRedirect('/publish_car/no_permisson/')

        #从导航栏“发布车源”进入的
        contact = mPublish_car.getPublishPeople(user_id)
        if contact == 0:
            return handler500(req)
        else:
            context = {"is_login": True,"contact": contact}#传递联系人
            return render(req, "publish.html", context)

@csrf_exempt
def go_back(req):
    #返回修改
    mTools=Tools()
    user_id = mTools.getSession(req,'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if user_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'POST':
        publish_info=mTools.getSession(req,'publish_info') #从会话中取出数据
        context ={"is_login": True, 'each_car_info': publish_info}
        return render(req, "publish.html", context)
    else:
        return handler404(req)  #404 请求错误

@csrf_exempt
def sure_publish(req):
    #确认发布
    mTools = Tools()
    user_id = mTools.getSession(req, 'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if user_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'POST':
        content = getFormData(req) #获取表单数据

        #content=mTools.getSession(req,'publish_info') #从会话中取出数据

        operation_id_modify = mTools.getSession(req,'operation_id_modify')
        if operation_id_modify != None:#表示要进行修改发布的有效期的车的信息，在这里需要删除该车，然后重新插入
            modify_result_code = mPublish_car.updateData(operation_id_modify, content)
            #modify_result_code=deletePublishValidTimeCar(operation_id_modify,current_user_phone_number)
            if modify_result_code == 0:
                return handler500(req) #修改发布的有效期的车的信息失败

        operation_id_againPublish = mTools.getSession(req,'operation_id_againPublish')
        if operation_id_againPublish != None:#表示要进行重新发布过期的车的信息，在这里需要删除该车，然后重新插入
            againPublish_result_code = mPublish_car.deletePublishInalidTimeCar(operation_id_againPublish)
            if againPublish_result_code == 0:
                return handler500(req) #重新发布过期的车的信息失败
            else:
                result_code = mPublish_car.firstPublishInsertData(user_id, content) #插入数据
                if result_code == 0:
                   return handler500(req) #发布失败

        result_code = mPublish_car.firstPublishInsertData(user_id, content) #插入数据
        if result_code == 0:
            return handler500(req) #发布失败

        mTools.delSession(req,'publish_info') #删除会话
        mTools.delSession(req,'operation_id_modify')
        mTools.delSession(req,'operation_id_againPublish')
        return HttpResponse("1")
    else:
        return handler404(req)  #404 请求错误


def DangagePermission(req):
    mTools = Tools()
    user_id = mTools.getSession(req,'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if user_id is None:
      return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'POST':
        if 'complete_info' in req.POST: #完善资料
            return HttpResponseRedirect('/complete_info/')
        if 'go_car_home' in req.POST: #返回车源列表
            return HttpResponseRedirect('/search/')
    else:
       context = {"is_login": True}
       return render(req, "permisson.html",context)

#获得表单数据
def getFormData(req):
        '''
        :param req:
        :return:返回获取到的表单数据
        '''
        #获得表单数据
        car_info={} #保存发布的car的信息
        delivery_date={}       #交货时间
        out_date={}            #过期
        price={}

        car_info['carType'] = req.POST.getlist("specificationList[]",'[]')      #车辆类型
        car_info['color'] = req.POST.getlist("colorList[]",'[]')                #颜色


        car_info['car_brand'] = req.POST.get('brand','')             #品牌
        car_info['car_series'] = req.POST.get('series','')           #车系
        car_info['car_model'] = req.POST.get('style','')            #车款

        delivery_date['year'] = req.POST.get('shipType[year]','0')            #交货时间的年份
        delivery_date['month'] = req.POST.get('shipType[month]','0')          #交货时间的月份
        delivery_date['day'] = req.POST.get('shipType[day]','0')              #交货时间的天数
        car_info["delivery_date"] = delivery_date                             #交货时间

        car_info['delivery_type'] = req.POST.get('shipType[type]','')

        out_date['year'] = req.POST.get('exceedDate[year]','0')            #过期的年份
        out_date['month'] = req.POST.get('exceedDate[month]','0')          #过期的月份
        out_date['day'] = req.POST.get('exceedDate[day]','0')              #过期的天数
        car_info["out_date"] = out_date                                    #交货时间

        car_info['pay_method'] = req.POST.get('payment','')                 #付款方式

        #car_info['sell_area'] = req.POST.get('region[province]','')                    #销售区域
        car_info['sell_area'] = req.POST.get('region[type]','')+' '+req.POST.get('region[province]','')+' '+req.POST.get('region[city]','') #销售区域

        car_info['method_logistics']=req.POST.get('logistics','')     #物流方式

        car_info['lowest_price']=req.POST.get('price[discountRate]','')            #优惠的钱
        car_info['highest_price']=req.POST.get('price[carPrice]','')                   #最高报价
        #car_info['price'] = price

        car_info['discount_rate']=req.POST.get('price[discountRate]','')             #优惠点数

        car_info['introduction']=req.POST.get('comment','')             #备注说明

        #contact = {}
        #contact['name'] = req.POST.get('contact[name]','')[0]                 #联系人姓名
        #contact['phone_number'] = req.POST.get('contact[phoneNumber]','')[0]

        #contact['name'] = req.POST.get('contact[name]','xxx')                 #联系人姓名
        #contact['phone_number'] = req.POST.get('contact[phoneNumber]','xxxxxxxxxxx')

        #car_info['contact'] = contact

        car_info['user_names']=req.POST.get('contact[name]','xxx')                 #联系人姓名
        car_info['phone_numbers']=req.POST.get('contact[phoneNumber]','xxxxxxxxxxx')           #联系人电话

        return car_info

#-------------------------------------------------------------------------
@csrf_exempt
def list_modify(req,operation_id):
    ###########
    #有效期 --- 修改发布
    ############
    mTools = Tools()
    user_id = mTools.getSession(req,'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if user_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'GET':
        modify_info = mPublish_car.modifyPublish(operation_id) #调用这个函数来获取修改发布的信息
        if modify_info == 0:
            return handler500(req) #修改有效期的车失败
        car_info = mPublish_car.getPublishInfo(user_id, modify_info) #存储和获取发布的车的信息
        req.session['operation_id_modify'] = operation_id
        context = {"is_login": True, 'car_info': car_info}
        return render(req, "publish.html", context)
    else:
        return handler404(req)  #404 请求错误


@csrf_exempt
def list_again_publish(req,operation_id):
    #过期 --- 重新发布
    mTools = Tools()
    user_id = mTools.getSession(req,'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if user_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'GET':
        modify_info = mPublish_car.againPublish(operation_id) #调用这个函数来获取重新发布的信息
        if modify_info == 0:
            return handler500(req) #修改有效期的车失败
        car_info = mPublish_car.getPublishInfo(user_id, modify_info) #存储和获取发布的车的信息
        req.session['operation_id_againPublish'] = operation_id
        context = {"is_login": True, 'car_info': car_info}
        return render(req, "publish.html", context)
    else:
        return handler404(req)  #404 请求错误
