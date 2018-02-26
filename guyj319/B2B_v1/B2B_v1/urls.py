"""B2B_v1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from captcha.views import captcha_refresh
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^myVerifyLogin/$', 'user.views.mylogin'),

    url(r'^$', 'first_page.views.index'),
    url(r'^issue/', 'first_page.views.issue'),

    url(r'^verifyInvitationCode/$', 'user.views.verify_invitation_code'),
    url(r'^verifyRegister/$', 'user.views.verify_register'),
    url(r'^sendPhoneVerifyCode/$', 'user.views.send_phone_verify_code_post'),
    url(r'^verifyLogin/$', 'user.views.verify_login'),
    url(r'^logout/$', 'user.views.my_logout'),
    url(r'^sessionExceedTime/$', 'user.views.session_exceed_time'),

    url(r'^completeMaterial/$', 'account.views.complete_material'),
    url(r'^findPasswordByPhone/$', 'finding.views.find_password_by_phone'),
    url(r'^findPasswordByEmail/$', 'finding.views.find_password_by_email'),
    url(r'^sendInvitationCode/$', 'account.views.send_invitation_code'),

    url(r'^forgetPassword/', 'finding.views.forget_password'),
    url(r'^forgetPasswordPost/', 'finding.views.forget_password_post'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^captcha/refresh/$', captcha_refresh, name='captcha-refresh'),
    #商家主页
    url(r'^merchant/$', 'account.views.merchant'),
    url(r'^merchantPost/$', 'account.views.homepage_seller_collection'),

    #收藏
    url(r'^collection/$','collection.views.collection'),
    url(r'^collectionPost/', 'collection.views.collection_post'),

    #我的消息
    url(r'^myMessage/$', 'message.views.my_message'),
    url(r'^myMessagePost/$', 'message.views.delete_message'),
    #我的需求
    url(r'^myDemand/$', 'demand.views.my_demand'),
    url(r'^myDemandPost/$', 'demand.views.my_demand'),

    #发布
    url(r'^publish/$', 'publish_car.views.publish'),
    url(r'^surePublish/$', 'publish_car.views.sure_publish'),
    url(r'^goBack/$', 'publish_car.views.go_back'),

    #url(r'^publish/', 'publish_car.views.publish'),
    #url(r'^publishSuccess/', 'publish_car.views.publish_success'),
    url(r'^publishPost/', 'publish_car.views.sure_publish'),
    #url(r'^preview/', 'publish_car.views.preview'),

    #搜索
    url(r'^search/$', 'search.views.search'),
    url(r'^searchFromFirstPage/$', 'search.views.get_data_from_first_page'), #从首页进来
    #url(r'^keyWordSort/$', 'search.views.get_data_by_one_word_sort'), #在结果列表，按照除了价格外的关键词搜索
    url(r'^priceSort/$', 'search.views.get_data_by_rice_sort'),     #在结果列表，价格关键词搜索
    url(r'^searchFromMyDemand/$', 'search.views.search_from_my_demand'), #从“我的需求”进来
    url(r'^saveSearchRecord/$', 'search.views.save_search_record'),      #保存需求
    url(r'^fuzzySearch/$', 'search.views.fuzzy_search'),                 #模糊搜索

    url(r'^keyWordSort/$', 'search.views.key_word_sort'), #在结果列表，按照除了价格外的关键词搜索


    #车源详情
    url(r'^detailPost/$', 'car.views.detail_post', name='detailPost'),
    url(r'^detail/$', 'car.views.detail', name='detail'),
    #设置
    url(r'^setting/$', 'setting.views.setting'),
    url(r'^settingPost/$', 'setting.views.setting_post'),
    url(r'^sendVerifyCode/', 'setting.views.send_phone_verify_code_post'),
    url(r'^verifyCodePost/$', 'setting.views.verify_code_post'),

    url(r'^setHeadIcon/$', 'setting.views.set_head_icon'),
    url(r'^upload_pic/$', 'setting.views.upload_pic',name='upload_pic'),

    #个人中心---有效发布
    url(r'^homePage/$', 'personal_center.views.personal_center'),
    url(r'^homePagePost/', 'personal_center.views.home_page_post'),

    #个人中心---编辑资料
    url(r'^editMaterial/$', 'account.views.edit_material'),
    url(r'^completeMaterialPost/$', 'account.views.complete_material'),
    url(r'^completeMaterial/$', 'account.views.complete_material'),

    #======邮件=======
    url(r'^sendEmail/$', 'finding.sendEmail.sendEmail'),
    url(r'^send/$', 'finding.sendEmail.send'),
    url(r'^mysend/$', 'finding.sendEmail.contacts'),
    url(r'^findPW_email_2/$', 'finding.sendEmail.smtpSendEmail'),
    url(r'^sendHtmlEmail/$', 'finding.sendEmail.sendHtmlMail'),

    #微信
    url(r'^weixin$', 'weixin.views.handleRequest'),
    url(r'^login/$', 'weixin.views.login'),
    url(r'^loginPost/$', 'weixin.views.login'),

    url(r'^personalCenter/$', 'weixin.views.personal_center'),

    url(r'^register/$', 'weixin.views.register'),
    url(r'^pushMsg/$', 'weixin.views.handPushMessage'),
    #授权获取openid的相关url：
    url(r'^oauth2/$', 'weixin.views.getOpenidByOauth2'),

    #后台管理模块
    #登录和退出
    url(r'^adminLogin/$', 'myadmin.views.admin_login'),
    url(r'^adminLoginPost/$', 'myadmin.views.admin_login'),
    url(r'^adminLogout/$', 'myadmin.views.admin_logout'),
    #主页
    url(r'^adminHome/$', 'myadmin.views.admin_home'),
    #账号设置
    url(r'^accountSetting/$', 'myadmin.admin_setAccount_view.set_account'), #---
    url(r'^adminAccountSettingPost/$', 'myadmin.admin_setAccount_view.set_account'), #---
    #url(r'^setAccount/$', 'myadmin.admin_setAccount_view.set_account'),

    #管理员设置
    url(r'^administratorSetting/$', 'myadmin.admin_set_view.set_admin_home'), #---
    url(r'^adminAddAdministratorPost/$', 'myadmin.admin_set_view.add_admin'), #---
    url(r'^adminDeleteAdministratorPost/$', 'myadmin.admin_set_view.delete_admin'), #---

    #url(r'^setAdminHome/$', 'myadmin.admin_set_view.set_admin_home'),
    #url(r'^addAdmin/$', 'myadmin.admin_set_view.add_admin'),
    #url(r'^deleteAdmin/$', 'myadmin.admin_set_view.delete_admin'),
    url(r'^modifyAdmin/$', 'myadmin.admin_set_view.modify_admin'),
    #超级管理员设置
    url(r'^setSuperAdminHome/$', 'myadmin.admin_set_view.set_super_admin_home'),
    url(r'^setSuperAdmin/$', 'myadmin.admin_set_view.set_super_admin'),
    #黑名单
    url(r'^backlist/$', 'myadmin.blackList_view.black_list_home'), #---
    #url(r'^blackList/$', 'myadmin.blackList_view.black_list_home'),
    url(r'^deleteFromBlackList/$', 'myadmin.blackList_view.delete_black'),
    #会员审核
    url(r'^memberAudit/$', 'myadmin.allVIP_view.vip_check_home'),#---
    #url(r'^vipCheckHome/$', 'myadmin.allVIP_view.vip_check_home'),
    url(r'^previewVIP/$', 'myadmin.allVIP_view.preview_vip'),
    #内容管理
    url(r'^contentList/$', 'myadmin.allContent_view.content_home'),#---
    #url(r'^contentHome/$', 'myadmin.allContent_view.content_home'),
    url(r'^modifyVIP/$', 'myadmin.allContent_view.modify_vip_in_content'),
    url(r'^deleteVipFromContentHome/$', 'myadmin.allContent_view.delete_vip_in_content'),
    #全部会员
    url(r'^memberList/$', 'myadmin.allVIP_view.all_vip_home'), #---
    #url(r'^allVipHome/$', 'myadmin.allVIP_view.all_vip_home'),
    url(r'^editVIP/$', 'myadmin.allVIP_view.edit_vip_in_all_vip'),
    url(r'^deleteVipFromAllVip/$', 'myadmin.allVIP_view.delete_vip_in_all_vip'),
    url(r'^blackVIP/$', 'myadmin.allVIP_view.black_vip_in_all_vip'),

    url(r'^manageDeal/$', 'myadmin.manage_deal_view.manage_deal'),
    url(r'^selectUser/$', 'myadmin.manage_deal_view.manage_deal'),
    url(r'^dealRecordHome/$', 'myadmin.manage_deal_view.deal_records'),

    #邀请好友
    url(r'^adminInviteFriend/$', 'myadmin.views.admin_invite_friend'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

