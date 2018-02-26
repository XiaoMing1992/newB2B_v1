#coding=utf-8
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "B2B_v1.settings")

from user.register.registerHome import Register
mRegister = Register()

def auto_register():
        user_name = 'guyuanjun02'
        phone = '13631257724'
        password = '1234567890'
        user_ip = 'xxx'

        result = mRegister.register(user_name, phone, password, user_ip) #调用该函数处理这个url.数据库出错，返回0；用户已经存在，返回1；成功则返回666
        if result == 0:
            print('Fail to insert')
        elif result == -1:
            print('Exist')
        else:
            print('Ok')

if __name__ == '__main__':
    auto_register()