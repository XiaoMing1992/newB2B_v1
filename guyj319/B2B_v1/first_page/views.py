# -*- coding:utf-8 -*-
from account.account_manage import Tools
from first_page.firstPage import First_page

from django.shortcuts import render
from django.views.decorators.cache import cache_control

from first_page import const

#指定缓存是否需要总是检查新版本, 如果没有变化则仅传送缓存版本. (某些缓存即使服务器端页面变化也仅传递缓存版本--仅仅因为缓存拷贝尚未到期).
# 在这个例子里 cache_control 通知缓存每次检验缓存版本, 直到 600 秒到期:
#@cache_control(must_revalidate=True, max_age=600)
mFirst_page = First_page()

def index(req):
        """
        is_login: 判断用户是否已经登陆
        brand_list: 汽车品牌列表
        car_series_list: 车系
        info_total: 当天发布的车源信息记录总数
        matched_total: 找到车源的客户总数
        """
        # get请求
        if req.method == 'GET':
              publish_num = mFirst_page.getPublishNum() #返回今天发布的车的数量
              if publish_num == -1:
                  return handler500(req)
              deal_num = mFirst_page.getDealNum() #返回成交量
              if deal_num == -1:
                  return handler500(req)

              mTools = Tools()
              user_id = mTools.getSession(req, 'user_id')
              if user_id is None:
                  flag = False
                  #req.session['login_from'] = req.META.get('HTTP_REFERER', '/') #记住来源的url，如果没有则设置为首页('/')
              else:
                  flag = True

              context = {"is_login": flag,
                  "brand_list": const.brand_list,
                  "car_series_list": const.car_series_list,
                  "info_total": publish_num,
                  "matched_total": deal_num}
              return render(req, "index.html", context)
        else:
            return handler404(req)

def handler404(request):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

import re
import urllib
import urllib.request
from django.shortcuts import render,render_to_response

def getImg(url, imgType):
  page = urllib.request.urlopen(url)
  #html = page.read().decode('utf-8')
  html = page.read().decode('gbk')
  #reg = r'src="(.*?\.+'+imgType+')"' #这个正则表达式是最关键的，取得图片链接就靠它了
  reg = r'src="(.*?\.+'+imgType+')"' #这个正则表达式是最关键的，取得图片链接就靠它了
  imgre = re.compile(reg)
  imgList = re.findall(imgre, html)
  return imgList

def getImgNmae(url):
  page = urllib.request.urlopen(url)
  #html = page.read().decode('utf-8')
  html = page.read().decode('gbk')
  reg = r'<img alt="(.*?)标志"' #这个正则表达式是最关键的，取得图片链接就靠它了
  imgre = re.compile(reg)
  imgList = re.findall(imgre, html)
  return imgList

def issue(request):
  query = request.GET.get('q','')
  if query:
    imglist = getImg(query, 'jpg')
    imgName = getImgNmae(query)
    final_img_list = []
    j = 0
    for i in range(len(imglist)):
        if imglist[i].find("new_brand_logo") != -1:
            img_dirct = {}
            img_dirct['imgSrc'] = 'http://car.qi-che.com/'+ imglist[i]
            img_dirct['imgName'] = imgName[j]
            final_img_list.append( img_dirct)
            j = j+1
  else:
    final_img_list = []
  return render_to_response('crawler.html', {'query': query, 'results': final_img_list})