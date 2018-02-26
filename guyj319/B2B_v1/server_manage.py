# coding=utf-8
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "B2B_v1.settings")

from car.models import car_table,invalid_time_car_table
from account.models import user_more_table,inviteCode_table
from account.models import record_table,message_table,user_info_table
import datetime
import time
from user.models import activity_table


class My_manage(object):
    def manage_car_time(self):
        pass
    def manage_invite_code(self):
        pass
    def mangage_my_message(self):
        pass

def server_manage():
  while True:
      time.sleep(10) #睡眠多久后，再次执行下面操作
      manage_car_time()
      mangage_my_message()

def manage_car_time():
   #定时更新存储发布才车的数据库的表，把过期的放到存放过期的车的表里面，并且从原数据库中删除

  #while True:
  #  time.sleep(10) #睡眠多久后，再次执行下面操作

    try:
       print('car_time')
       all_car=car_table.objects.all().order_by("date_valid")   #根据有效期来 升序 排序，这样可以把前面的车进行一次检查
       today_time=datetime.datetime.now().strftime("%Y-%m-%d")

       for i in range(len(all_car)):
          if all_car[i].date_valid< today_time: #过期了
              try:
                 invalid_time_car_table.objects.create(user_phone=all_car[i].user_phone,car_type=all_car[i].car_type, car_brand=all_car[i].car_brand,car_series=all_car[i].car_series,car_model=all_car[i].car_model,color=all_car[i].color,color_hex=all_car[i].color_hex,delivery_time=all_car[i].delivery_time,delivery_type=all_car[i].delivery_type,pay_method=all_car[i].pay_method,sell_area=all_car[i].sell_area,method_logistics=all_car[i].method_logistics,lowest_price=all_car[i].lowest_price,highest_price=all_car[i].highest_price,discount_rate=all_car[i].discount_rate,introduction=all_car[i].introduction,date_publish=all_car[i].date_publish,date_valid=all_car[i].date_valid,read_num=all_car[i].read_num)

                 user=user_more_table.objects.get(user_phone = all_car[i].user_phone)
                 temp=user.user_more_table-1  #有效发布次数-1
                 user.user_more_table=temp
                 user.save() #更新有效发布次数
              except:
                 print('定时任务---数据库更新出错')
                 continue
          elif all_car[i].date_valid>=today_time: #因为是升序排序，如果i这个车没有过期，那么后面的也不会过期，所以直接跳出
              break

          for i in range(len(all_car)):#在存放发布的车的表里面，把过期的车给删除掉
              if all_car[i].date_valid>=today_time: #因为是升序排序，如果i这个车没有过期，那么后面的也不会过期，所以直接跳出
                  break
              else:     #过期了
                 try:
                    car_table.objects.get(id=all_car[i].id).delete() #根据有效期来删除过期的车
                 except:
                    print('定时任务---数据库删除失败')
                    continue
    except:
          print('定时任务---数据库操作失败')

def manage_invite_code():
    #定时更新存储发布才车的数据库的表，把过期的放到存放过期的车的表里面，并且从原数据库中删除

    while True:
        time.sleep(10) #睡眠多久后，再次执行下面操作

        try:
           all_invite_code=inviteCode_table.objects.all().order_by("validity_time")   #根据有效期来 升序 排序，这样可以把前面的邀请码进行一次检查
           today_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
           print(today_time)
           for i in range(len(all_invite_code)):#在存放邀请码的表里面，把过期的邀请码给删除掉
               print(all_invite_code[i].validity_time)
               if all_invite_code[i].validity_time>=today_time: #因为是升序排序，如果i这个邀请码没有过期，那么后面的也不会过期，所以直接跳出
                  break
               else:     #过期了
                  try:
                      print(all_invite_code[i].id)
                      inviteCode_table.objects.get(id=all_invite_code[i].id).delete() #根据有效期来删除过期的邀请码
                  except:
                      print('定时任务---数据库删除失败')
                      continue
        except:
           print('定时任务---数据库操作失败')

def mangage_my_message():
   #定时更新存储发布才车的数据库的表，把过期的放到存放过期的车的表里面，并且从原数据库中删除

  #while True:
  #  time.sleep(10) #睡眠多久后，再次执行下面操作

    try:
       print('my_message')
       all_records=record_table.objects.all()   #根据有效期来 升序 排序，这样可以把前面的车进行一次检查
       today_time=datetime.datetime.now().strftime("%Y-%m-%d")

       for i in range(len(all_records)):
          #if all_records[i].time_valid> today_time: #没有过期
              try:
                 cars=car_table.objects.filter(car_trademark = all_records[i].car_trademark,car_car=all_records[i].car_car,car_model=all_records[i].car_model)
                 for j in range(len(cars)):
                     try:
                         user=user_info_table.objects.get(user_phone_id=cars[j].user_phone)
                         company_name=user.user_company_name
                         try:
                              message_table.objects.create(seller_phone=cars[j].user_phone,buyer_phone=all_records[i].user_phone,buyer_search_record_id=all_records[i].id,company_name=company_name,car_id=cars[j].id,car_model=cars[j].car_model,message_time=cars[j].date_publish,order_type=True,sell_type=True)
                         except:
                             print('定时任务---message_table数据库更新出错')
                             continue
                     except:
                        print('定时任务---user_info_table数据库查询出错')
                        continue
              except:
                 print('定时任务---car_table数据库更新出错')
                 continue
    except:
          print('定时任务---数据库操作失败')

if __name__ == '__main__':
     #manage_invite_code()
     server_manage()
     #my_manage=My_manage()
     #my_manage.manage_car_time=manage_car_time
     #my_manage.manage_invite_code=manage_invite_code
     #my_manage.mangage_my_message=mangage_my_message

     #运行
     #my_manage.manage_car_time()      #将car_table中的过期的车放到存放过期的车的表invalid_time_car_table里面
     #my_manage.manage_invite_code()   #删除过期邀请码
     #my_manage.mangage_my_message()   #处理需求
     #force_to_exit()

