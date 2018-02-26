#coding=utf-8
from account.account_manage import LoginBackend
from user.models import user_table

class Change_phone(object):
    def changePhone(self, user_id, new_phone):
        '''
        :param user_id:
        :param new_phone:
        :return: 修改密码成功返回666；更新数据库出错，返回0；用户不存在，返回1
        '''
        try:
            #获取的表单数据与数据库进行比较
            user = user_table.objects.get(id=user_id) #一个电话号码的记录只有一条，所以用get()
            #下面是更新一条记录的
            try:
                user.phone = new_phone
                user.save()#保存到数据库里面
                return 666
            except:
                return 0
        except:
            return 0

    def newPhoneIsExist(self, new_phone):
        '''
        :param new_phone:
        :return: 如果新电话号码存在，返回0；否则，返回666
        '''
        try:
            #获取的表单数据与数据库进行比较
            user_table.objects.get(phone=new_phone) #一个电话号码的记录只有一条，所以用get()
            return 666 #已经存在
        except:
            return 0 #不存在

    def checkPhone(self, old_phone):
           try:
                #获取的表单数据与数据库进行比较
               user = user_table.objects.get(phone=old_phone) #一个电话号码的记录只有一条，所以用get()
               return 666
           except:
                return 0

    def changePhone2(self, old_phone, password, new_phone):
        '''
        :param old_phone:
        :param password:
        :param new_phone:
        :return: 修改密码成功返回666；更新数据库出错，返回0；用户不存在，返回1
        '''

        checkUser = LoginBackend() #实例化
        user = checkUser.authenticate(old_phone,password) #将手机号和旧密码进行检查，如果是对的，就把旧手机号进行替换
        if user is not None:
           #下面是更新一条记录的
           try:
              user.phone = new_phone
              user.save()#保存到数据库里面
              return 666
           except:
              return 0
        return 1
