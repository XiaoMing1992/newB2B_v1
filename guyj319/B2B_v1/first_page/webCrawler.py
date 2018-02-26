# -*- coding:utf-8 -*-
from html.parser import HTMLParser
import urllib
import urllib.request
from selenium import webdriver

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.a_text = False
        self.content = []
    def handle_starttag(self,tag,attr):
        if tag == 'option':
            self.a_text = True
    def handle_endtag(self,tag):
        if tag == 'option':
            self.a_text = False
    def handle_data(self,data):
        if self.a_text:
            print(data)
            self.content.append(data)

if __name__ == "__main__":
    url = "http://www.pcauto.com.cn/"
    #url = "file:///C:/Users/lenovo/Desktop/%E5%A4%AA%E5%B9%B3%E6%B4%8B%E6%B1%BD%E8%BD%A6%E7%BD%91_%E7%B2%BE%E5%87%86%E6%8A%A5%E4%BB%B7_%E6%9D%83%E5%A8%81%E8%AF%84%E6%B5%8B_%E6%B1%BD%E8%BD%A6%E4%B8%96%E7%95%8C,%E7%94%B1%E6%AD%A4%E7%B2%BE%E5%BD%A9.htm"
    page = urllib.request.urlopen(url)
    html = page.read().decode('gbk')

    yk = MyHTMLParser()
    yk.feed(html)
    filter_content = []
    letter = []  #字母
    car_brand = [] #品牌名称
    a = {}
    b = []

    #for item in yk.content:
    #    if item[0] !='请' :
           #filter_content.append(item)
           #print(item)
    #print(filter_content)

    my_file = open("out.txt", 'a+')
    a = str("中国")
    #my_file.write(a.encode('utf-8'))
    #print(filter_content,file=my_file)
    my_file.close()

    for i in range(len(filter_content)):
        temp_item = filter_content[i].split(' ')
        car_brand.append(temp_item[1])
        if i != len(filter_content)-1:
            if filter_content[i][0] != filter_content[i+1][0]:
               a['letter'] = filter_content[i][0]
               a['car_brand_list'] = car_brand
               b.append(a)
               a = {}
               car_brand = []
        else:
            if i == len(filter_content)-1:
               a['letter'] = filter_content[i][0]
               a['car_brand_list'] = car_brand
               b.append(a)
               a = {}
               car_brand = []

    #for item in b:
    #    print(item)
    yk.close()