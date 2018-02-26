from django.db import models

# Create your models here.
class weiXinUser(models.Model):
    openid = models.CharField(max_length=100, db_index=True)  #用户的微信openID
    phone = models.CharField(max_length=15, default='10086', db_index=True) #phone_number
    state = models.IntegerField(default=0)