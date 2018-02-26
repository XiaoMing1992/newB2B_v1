#coding=utf-8
from django import forms
from captcha.fields import CaptchaField

class CaptachaTestForm(forms.Form):
    captcha = CaptchaField()
