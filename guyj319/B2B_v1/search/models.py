#coding=utf-8
from django.db import models

# Create your models here.
class test(models.Model):
    name = models.CharField(max_length=20, default='None')
    age = models.IntegerField(default=0)
    sex = models.CharField(max_length=10, default='None')
