#coding=utf-8
from account.account_manage import Tools
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from search.dealKeySearch import Keyword_search
from search.dealFuzzySearch import Fuzzy_search
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from first_page.views import handler500
from first_page.views import handler404
from first_page import const
import datetime
from django.views.decorators.cache import cache_control,cache_page

#指定缓存是否需要总是检查新版本, 如果没有变化则仅传送缓存版本. (某些缓存即使服务器端页面变化也仅传递缓存版本--仅仅因为缓存拷贝尚未到期).
# 在这个例子里 cache_control 通知缓存每次检验缓存版本, 直到 600 秒到期:
#@cache_page(60*1)

mKeyword_search = Keyword_search()
mFuzzy_search = Fuzzy_search()

@csrf_exempt
def search_from_my_demand(req):
    #从‘我的需求’那里传递过来的（也就是说从记录我的需求的记录表里面获取的）
    mTools = Tools()
    user_id = mTools.getSession(req,'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
    if user_id is None:
       return HttpResponseRedirect('/sessionExceedTime/')

    if req.method == 'GET':
        operation_id = req.GET.get('operation_id',0)
        result = mKeyword_search.getDataFromMyDemands(operation_id, user_id) #根据用户的需求的记录id和其电话号码来查询
        if result == 0:
           return handler500(req)
        else:
           condition = result

        cars_infos = mKeyword_search.OneWordGetData(condition)
        if cars_infos == 0:
            return handler500(req)
        else:
            deleteAllSession(req)
            length_cars_infos = len(cars_infos)
            req.session['search_datas'] = cars_infos
            req.session['length_search_datas'] = length_cars_infos
        return HttpResponseRedirect("/search/")
    else:
        return handler404(req)

@csrf_exempt
def save_search_record(req):
    mTools = Tools()
    if req.method == 'POST':
       user_id = mTools.getSession(req,'user_id')#调用account.account_manage模块的类Tools的getSession（）函数来获取当前会话的id
       if user_id is None:
           return HttpResponseRedirect('/sessionExceedTime/')

       condition = postMethodGetParams(req) #获取post请求的用户保存的数据
       result_code = mKeyword_search.saveSearchRecord(user_id, condition) #调用这个函数来处理用户保存的需求
       if result_code == 666: #保存搜索条件成功
           return HttpResponse('1')
       elif result_code == 0:
           return HttpResponse('0')
    else:
       return handler404(req) #404 请求错误

@csrf_exempt
def fuzzy_search(req):
    if req.method == 'GET':
        content = req.GET.get('fuzzyContent', '')

        list_content = mFuzzy_search.divideWords(content) #获取分词结果
        length_list_content = len(list_content)
        cars_infos = mFuzzy_search.fuzzyFinderGetData(req, list_content, length_list_content,0)  ##############################

        if cars_infos == 0:
            return handler500(req)
        else:
            return HttpResponseRedirect("/search/")
    else:
        return handler404(req)

def get_data_from_first_page(req):
    """
    如果有GET请求，返回搜索结果。
    """
    if req.method == "GET":
        car_brand = req.GET.get("brandSelector", '')     #品牌
        car_series = req.GET.get("seriesSelector", '')   #车系

        car_brand = const.brand_list.get(car_brand, '')
        car_series = const.car_series_list.get(car_series, '')
        result_list = mKeyword_search.firstPageSort(car_brand, car_series)

        if result_list == 0:
            return handler500(req)
        else:
            deleteAllSession(req)
            req.session['search_datas'] = result_list
            req.session['length_search_datas'] = len(result_list)
        return HttpResponseRedirect("/search/")
    else:
        return handler404(req)

def search(req):
    """
    如果有GET请求，返回搜索结果。
    """
    if req.method == "GET":
        flag = False
        mTools=Tools()
        user_id = mTools.getSession(req,'user_id')
        if user_id is not None:
            flag = True

        final = get_result_search(req)
        data = final.get('data','')
        time_sorting_type = final.get('time_sorting_type','up')
        price_sorting_type = final.get('price_sorting_type','up')

        result_list_piece = data.get('results','')
        allPage = data.get('allPage','1') #总页数
        curPage = data.get('curPage','1')  #获取处理后的当前页数

        cars_infos_piece = mKeyword_search.getCarDataInArray(result_list_piece) #查询车的信息
        search_conditions = returnConditionsFromSession(req) #返回用户的搜索条件
        context = {"is_login": flag,
                "allPage":allPage,
                "curPage":curPage,
                "time_sorting_type":time_sorting_type,
                "price_sorting_type":price_sorting_type,
               "result_list": cars_infos_piece,
               "search_conditions":search_conditions}
        return render(req, "search.html", context)
    else:
        return handler404(req)

def get_result_search(req):
    mTools = Tools()
    if req.method == 'GET':
       pageType = req.GET.get('pageType', '')
       curPage = int(req.GET.get('curPage', '1'))
       allPage = int(req.GET.get('allPage','1'))

       sort_by_time = req.GET.get('timeSortingType', None)
       sort_by_price = req.GET.get('priceSortingType', None)

       cars_infos = mTools.getSession(req,'search_datas')
       length_cars_infos = mTools.getSession(req,'length_search_datas')

       final = {}

       if sort_by_time is not None:
          if sort_by_time == 'up': #升序
             cars_infos.sort(key=lambda x:x[17],reverse=False) #按照发布日期来排序，发布日期的字段号是13（字段号从0开始算）。reverse=False为升序排序
             final['time_sorting_type'] = 'down'
          elif sort_by_time == 'down': #降序
             cars_infos.sort(key=lambda x:x[17],reverse=True) #按照发布日期来排序，发布日期的字段号是13（字段号从0开始算）。reverse=False为升序排序
             final['time_sorting_type'] = 'up'

       if sort_by_price is not None:
           if sort_by_price == 'up': #升序
              cars_infos.sort(key=lambda x:x[14],reverse=False)
              final['price_sorting_type'] = 'down'
           elif sort_by_price == 'down': #降序
              cars_infos.sort(key=lambda x:x[14],reverse=True)
              final['price_sorting_type'] = 'up'

       if sort_by_price is not None or sort_by_time is not None: #数据已经改变，需要更改会话内容
            req.session['search_datas'] = cars_infos
            req.session['length_search_datas'] = len(cars_infos)

       data = mKeyword_search.searchPaging(cars_infos,length_cars_infos,curPage,allPage,pageType)

       final['data'] = data
       return final

def get_data_by_one_word_sort(req):
  if req.method == "GET":
        condition = getMethodGetParams(req)

        result_list = mKeyword_search.OneWordGetData(condition)
        if result_list == 0:
            return handler500(req)
        else:
            req.session['search_datas'] = result_list
            req.session['length_search_datas'] = len(result_list)
        return HttpResponseRedirect("/search/")

def get_data_by_rice_sort(req):
    """
    如果有GET请求，返回搜索结果。
    """
    if req.method == "GET":
        lowest_price = req.GET.get("lowest_price",'')
        highest_price = req.GET.get("highest_price",'')

        result_list = mKeyword_search.keyWordGetDataOederByPrice(lowest_price,highest_price)
        if result_list == 0:
            return handler500(req)
        else:
            req.session['search_datas'] = result_list
            req.session['length_search_datas'] = len(result_list)
        return HttpResponseRedirect("/search/")

def getMethodGetParams(req):
        condition = {}
        condition['car_type'] = req.GET.get("carType",'')     #车辆类型

        condition['car_brand'] = req.GET.get("brand",'')    #品牌
        condition['car_series'] = req.GET.get("series",'')  #车系
        condition['car_model'] = req.GET.get("carModel",'')    #车款

        condition['sell_area'] = req.GET.get("province",'') + ' '+req.GET.get("city",'')
        condition['province'] = req.GET.get("province",'')
        condition['city'] = req.GET.get("city",'')

        condition['pay_method'] = req.GET.get("payment",'')
        condition['delivery_type'] = req.GET.get("shipType",'')
        condition['color'] = req.GET.get("color",'')
        condition['method_logistics'] = req.GET.get("logistics",'')

        condition['lowest_price'] = int(req.GET.get("lowest_price",'0'))
        condition['highest_price'] = int(req.GET.get("highest_price",'0'))

        return condition

def postMethodGetParams(req):

        condition = {}
        condition['car_type'] = req.POST.get("carType",'')   #车辆类型

        condition['car_brand'] = req.POST.get("brand",'')    #品牌
        condition['car_series'] = req.POST.get("series",'')  #车系
        condition['car_model'] = req.POST.get("carModel",'')    #车款

        condition['sell_area'] = req.POST.get("province",'') + ' '+req.POST.get("city",'')
        condition['province'] = req.POST.get("province",'')
        condition['city'] = req.POST.get("city",'')

        condition['pay_method'] = req.POST.get("payment",'')
        condition['delivery_type'] = req.POST.get("shipType",'')
        condition['color'] = req.POST.get("color",'')
        condition['method_logistics'] = req.POST.get("logistics",'')
        return condition

#================= 搜索面板的关键词搜索，除了价格

def key_word_sort(req):
  if req.method == "GET":
        createSession(req)
        condition = getDataFromSession(req)

        #result_list = mKeyword_search.OneWordGetData(condition)
        result_list = mKeyword_search.keyWordIntersection(condition)
        if result_list == 0:
            return handler500(req)
        else:
            req.session['search_datas'] = result_list
            req.session['length_search_datas'] = len(result_list)
        return HttpResponseRedirect("/search/")

def getDataFromSession(req):
        mTools = Tools()
        condition = {}
        condition['car_type'] = mTools.getSession(req,'car_type')     #车辆类型

        condition['car_brand'] = mTools.getSession(req,'car_brand')    #品牌
        condition['car_series'] = mTools.getSession(req,'car_series')  #车系
        condition['car_model'] = mTools.getSession(req,'car_model')    #车款

        condition['province'] = mTools.getSession(req,'province')
        condition['city'] = mTools.getSession(req,'city')
        condition['sell_area'] = mTools.getSession(req,'sell_area')

        condition['pay_method'] = mTools.getSession(req,'pay_method')
        condition['delivery_type'] = mTools.getSession(req,'delivery_type')
        condition['color'] = mTools.getSession(req,'color')
        condition['method_logistics'] = mTools.getSession(req,'method_logistics')

        condition['lowest_price'] = mTools.getSession(req,'lowest_price')
        condition['highest_price'] = mTools.getSession(req,'highest_price')

        return condition

def createSession(req):
        my_file = open("out.txt", 'a+')
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #时间
        print('[search.views.createSession][%s]:%s'%(now_time,req.GET),file=my_file)
        my_file.close()

        car_type = req.GET.get("carType",None)        #车辆类型

        car_brand = req.GET.get("brand",None)     #品牌
        car_series = req.GET.get("series",None)   #车系
        car_model = req.GET.get("carModel",None)     #车款

        province = req.GET.get("province",None)     #省份
        city = req.GET.get("city",None)     #城市
        #sell_area = province + ' '+city     #销售区域

        pay_method = req.GET.get("payment",None)   #付款方式
        delivery_type = req.GET.get("shipType",None)        #期货类型
        color = req.GET.get("color",None)                        #颜色
        method_logistics = req.GET.get("logistics",None)  #物流方式

        lowest_price = int(req.GET.get("lowest_price",'0'))
        highest_price = int(req.GET.get("highest_price",'0'))


        if car_type is not None:
           req.session['car_type'] = car_type

        if car_brand is not None:
           req.session['car_brand'] = car_brand
        if car_series is not None:
           req.session['car_series'] = car_series
        if car_model is not None:
           req.session['car_model'] = car_model

        if province is not None:
           req.session['province'] = province
        if city is not None:
           req.session['city'] = city
        #if sell_area is not None:
        #   req.session['sell_area'] = sell_area

        if pay_method is not None:
           req.session['pay_method'] = pay_method
        if delivery_type is not None:
           req.session['delivery_type'] = delivery_type
        if color is not None:
           req.session['color'] = color
        if method_logistics is not None:
           req.session['method_logistics'] = method_logistics

        if lowest_price <= highest_price and highest_price!=0:
           req.session['lowest_price'] = lowest_price
           req.session['highest_price'] = highest_price

def deleteSession(req,what):
        mTools = Tools()
        mTools.delSession(req,what)

        car_type = req.GET.get("carType",None)        #车辆类型

        car_brand = req.GET.get("brand",None)     #品牌
        car_series = req.GET.get("series",None)   #车系
        car_model = req.GET.get("carModel",None)     #车款

        city = req.GET.get("city",None)             #城市
        province = req.GET.get("province",None)     #省份
        #sell_area = req.GET.get("sell_area",None)     #销售区域

        pay_method = req.GET.get("payment",None)   #付款方式
        delivery_type = req.GET.get("shipType",None)        #期货类型
        color = req.GET.get("color",None)                        #颜色
        method_logistics = req.GET.get("logistics",None)  #物流方式

        if car_type is not None:
           mTools.delSession(req,'car_type')

        if car_brand is not None:
           mTools.delSession(req,'car_brand')

        if car_series is not None:
           mTools.delSession(req,'car_series')

        if car_model is not None:
           mTools.delSession(req,'car_model')

        if province is not None:
           mTools.delSession(req,'province')

        if city is not None:
           mTools.delSession(req,'city')

        #if sell_area is not None:
        #   mTools.delSession(req,'sell_area')

        if pay_method is not None:
           mTools.delSession(req,'pay_method')

        if delivery_type is not None:
           mTools.delSession(req,'delivery_type')

        if color is not None:
           mTools.delSession(req,'color')

        if method_logistics is not None:
           mTools.delSession(req,'method_logistics')

def returnConditionsFromSession(req):
        mTools = Tools()
        condition = {}
        condition['carType'] = mTools.newGetSession(req,'car_type')     #车辆类型

        condition['brand'] = mTools.newGetSession(req,'car_brand')    #品牌
        condition['series'] = mTools.newGetSession(req,'car_series')  #车系
        condition['carModel'] = mTools.newGetSession(req,'car_model')    #车款

        condition['province'] = mTools.newGetSession(req,'province')
        condition['city'] = mTools.newGetSession(req,'city')
        condition['sell_area'] = mTools.newGetSession(req,'sell_area')

        condition['payment'] = mTools.newGetSession(req,'pay_method')
        condition['shipType'] = mTools.newGetSession(req,'delivery_type')
        condition['color'] = mTools.newGetSession(req,'color')
        condition['logistics'] = mTools.newGetSession(req,'method_logistics')

        return condition

def deleteAllSession(req):
        mTools = Tools()
        mTools.delSession(req,'car_type')
        mTools.delSession(req,'car_brand')
        mTools.delSession(req,'car_series')
        mTools.delSession(req,'car_model')
        mTools.delSession(req,'province')
        mTools.delSession(req,'city')
        #mTools.delSession(req,'sell_area')
        mTools.delSession(req,'pay_method')
        mTools.delSession(req,'delivery_type')
        mTools.delSession(req,'color')
        mTools.delSession(req,'method_logistics')
