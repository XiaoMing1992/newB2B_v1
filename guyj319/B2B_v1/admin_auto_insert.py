#coding=utf-8
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "B2B_v1.settings")

from myadmin.admin_set import Set_admin
mSet_admin = Set_admin()

def insert_admin():
        user_name = 'admin05'
        #name = '顾远均05'
        name = 'guyuanjun05'
        password = 'admin05'
        is_super_admin = 0

        result = mSet_admin.add_admin(user_name, name, password, is_super_admin)
        if result == 0:
            print('Fail to insert')
        elif result == 1:
            print('Exist')
        elif result == 666:
            print('Ok')

if __name__ == '__main__':
    insert_admin()