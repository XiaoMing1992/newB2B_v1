#coding=utf-8
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "B2B_v1.settings")

from account.my_friends.inviteFriend import Invite_friends
mInvite_friends = Invite_friends()

def insert_inviteCode():
        current_user_phone_number = 'system'
        mobiles = ['13631257723']

        result = mInvite_friends.inviteFriend(current_user_phone_number, mobiles) #调用这个函数处理当前用户输入的电话号码
        if result == 0:
            print('Fail to insert')   #更新或者插入邀请码出错
        else:
            print('Ok')

if __name__ == '__main__':
    insert_inviteCode()