# coding=utf-8
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from account.account_manage import Tools
from car.car_info import Car_detail
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from first_page.views import handler500
from first_page.views import handler404
from django.views.decorators.cache import cache_control

#指定缓存是否需要总是检查新版本, 如果没有变化则仅传送缓存版本. (某些缓存即使服务器端页面变化也仅传递缓存版本--仅仅因为缓存拷贝尚未到期).
# 在这个例子里 cache_control 通知缓存每次检验缓存版本, 直到 600 秒到期:
#@cache_control(must_revalidate=True, max_age=600)

mCar_detail = Car_detail()

@csrf_exempt
def detail(req):
    mTools = Tools()
    user_id = mTools.getSession(req,'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if user_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'GET':
        operation_id = req.GET.get('operation_id',0)

        source_detail_list = mCar_detail.getCarInfo(operation_id) #获取车源信息
        if source_detail_list == 0:
            return handler500(req)
        seller_info = mCar_detail.getSellerInfo(operation_id) #获取卖家信息
        if seller_info == 0:
            return handler500(req)

        current_seller_id = seller_info.get('id') #当前查看的车的卖家的id

        # 如果该卖家的电话号码与当前用户的电话号码同样，即他们是同一个人，则不显示；否则，显示
        if user_id != current_seller_id:  #同一个人，不显示,所以show_current_seller为 False
            show_current_seller = False
        else:#不是同一个人，显示
            show_current_seller = True

            #把浏览该卖家的买家信息写进 message_table 里面，显示到“我的消息”那里
            series_detail = source_detail_list.get('series_detail','')       #获取该卖家的车的车型,配置,其他
            car_brand = series_detail.get('brand','')                            #品牌
            car_series = series_detail.get('displacement','')                    #车系
            car_model = series_detail.get('other','')                            #车款

            result_code = mCar_detail.insertMessageTable(user_id, current_seller_id, operation_id,car_brand, car_series,car_model,1,0) #调用该函数来把当前浏览信息以及有关内容写进MessageTable中
            #print('result_code1')
            if result_code == 0:
                return handler500(req)
            #print('result_code2')

        code_collect_merchant = mCar_detail.isMerchantCollected(user_id, current_seller_id) #判断该商家是否已经被收藏过
        #print('result_code3')
        if code_collect_merchant == 2 : #注意：True是1，False是0，数据库查询出错如果返回0和查询结果为空集返回False相同，会出错，所以此处定义数据库查询出错如果返回2
            return handler500(req)
            #print(code_collect_merchant)
        else:
            is_merchant_collected = code_collect_merchant
        #print('result_code4')

        code_collect_info = mCar_detail.isInfoCollected(user_id, operation_id)
        #print('result_code5')
        if code_collect_info == 2 : #注意：True是1，False是0，数据库查询出错如果返回0和查询结果为空集返回False相同，会出错，所以此处定义数据库查询出错如果返回2
            return handler500(req)
        else:
            is_info_collected = code_collect_info
        #print('result_code6')

        merchant_material = seller_info.get('merchant_material','')
        context = {"is_login": True,
               "show_current_seller":show_current_seller,
               "is_merchant_collected": is_merchant_collected,
               "is_info_collected": is_info_collected,
               "merchant_material": merchant_material,
               "source_detail_list": source_detail_list}

        return render(req, "detail.html", context)
    else:
        return handler404(req)

#收藏请求
@csrf_exempt
def detail_post(req):
    mTools = Tools()
    user_id = mTools.getSession(req,'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if user_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')


    if req.method == 'POST':
        merchant_id = req.POST.get("merchantId",None)
        detail_id = req.POST.get("infoId",None)
        #print(merchant_id)
        #print(detail_id)
        if merchant_id is not None:
            return seller_collection(user_id, merchant_id)
        if detail_id is not None:
            return car_collection(user_id, detail_id)
    else:
        return handler404(req)

#车源收藏
@csrf_exempt
def car_collection(user_id, car_id):
    result_code = mCar_detail.collectCar(user_id, car_id) #调用这个函数来处理收藏车源信息操作
    if result_code == 0:
        return HttpResponse("0")
    elif result_code == 666:
        return HttpResponse("1")

#商家收藏
@csrf_exempt
def seller_collection(user_id, seller_id):
    result_code = mCar_detail.collectSeller(user_id, seller_id)#调用这个函数来处理收藏商家操作
    if result_code == 0:
        return HttpResponse("0")
    elif result_code == 666:
        return HttpResponse("1")
