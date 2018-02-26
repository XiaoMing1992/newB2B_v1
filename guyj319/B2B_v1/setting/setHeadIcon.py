#coding=utf-8
from account.models import user_info_table

from django.views.decorators.cache import cache_control,cache_page

#指定缓存是否需要总是检查新版本, 如果没有变化则仅传送缓存版本. (某些缓存即使服务器端页面变化也仅传递缓存版本--仅仅因为缓存拷贝尚未到期).
# 在这个例子里 cache_control 通知缓存每次检验缓存版本, 直到 600 秒到期:
#private=True声明该页面的缓存是 "私密的"
#@cache_control(private=True,must_revalidate=True, max_age=600)
#@cache_page(60 * 1)

class Set_head_icon(object):
    def setHeadIcon(self,current_user_phone_number,head_icon_path):
         '''
         :param current_user_phone_number:
         :param head_icon_path:
         :return: 正常返回666；数据库更新出错，返回0
         '''
         try:
             user = user_info_table.objects.get(user_phone_id=current_user_phone_number)
             user.head_icon_path = head_icon_path
             user.save()
             return 666
         except:
             return 0
