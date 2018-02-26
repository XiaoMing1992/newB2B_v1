# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
from django.shortcuts import render

def home(request):
    List = ['自强学堂', '渲染Json到模板']
    Dict = {'site': '自强学堂', 'author': '涂伟忠'}
    return render(request, 'home_test.html', {
            'List': json.dumps(List),
            'Dict': json.dumps(Dict)
        })

from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'index_test.html')

def add(request):
    a = request.GET['a']
    b = request.GET['b']
    a = int(a)
    b = int(b)
    return HttpResponse(str(a+b))