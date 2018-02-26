#coding=utf-8
from account.models import inviteCode_table
from account.my_friends.sendInviteCode import Send_invite_code
import datetime

mSend_invite_code = Send_invite_code()

class Invite_friends(object):

    def inviteFriend(self, user_id, mobiles):
        '''
        :param user_id:
        :param mobiles:
        :return: 正常，返回成功发送的电话号码和失败发送的电话号码；插入数据库出错，返回0
        '''


        send_time = datetime.datetime.now()   #发送的时间
        validityTime = datetime.datetime.now()+datetime.timedelta(days=180) #邀请码的有效时间，现在假设为180天

        success=[]  #保存成功发送的电话号码
        fail=[]    #保存失败发送的电话号码
        for mobile in mobiles:
            try:
               #发送邀请码给该手机号码
               inviteCode = mSend_invite_code.getInviteCode()
               result = mSend_invite_code.sendInviteCode(mobile, inviteCode)
               if result == True:#发送成功
                   #添加一条新记录到数据库里面
                   inviteCode_table.objects.create(user_id=user_id,
                                                   receive_phone=mobile,
                                                   inviteCode=inviteCode,
                                                   validity_time=validityTime,
                                                   send_time=send_time)
                   #保存成功发送的电话号码
                   success.append(mobile)
               else:
                   #保存失败发送的电话号码
                   fail.append(mobile)
            except:
               return 0

        dict={}
        dict['success'] = success
        dict['fail'] = fail
        return dict  #返回成功发送的电话号码和失败发送的电话号码



