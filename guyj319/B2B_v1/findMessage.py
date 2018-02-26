# coding=utf-8
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "B2B_v1.settings")

from car.models import car_table
from account.models import record_table,message_table,user_info_table
import datetime
import time

def mangage_my_message():
   #定时更新存储发布才车的数据库的表，把过期的放到存放过期的车的表里面，并且从原数据库中删除

  while True:
    time.sleep(10) #睡眠多久后，再次执行下面操作

    try:
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
     mangage_my_message()

