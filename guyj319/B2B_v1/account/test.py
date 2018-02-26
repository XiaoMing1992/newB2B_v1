#coding=utf-8
from django.http import HttpResponse

def uploadPic(rq):
  file = rq.FILES['photo']
  oldFileName = file.name
  fileExt = oldFileName.split('.')[-1]
  if fileExt != 'jpg' and fileExt != 'jpeg' and fileExt != 'png':  #标记1
    response = HttpResponse()
    response['Content-Type'] = "application/json"
    imgurl = "http://127.0.0.1:8000/static/images/temp/5.jpg"
    json = "{\"status\":\"fail\", \"imgurl\":\"" + imgurl + "\"}"  #标记2
    response.write(json)
    return response

  saveFileName = str('/images/'  + oldFileName) #标记4
  
  response = HttpResponse()
  response['Content-Type'] = "application/json"
  imgurl = "http://127.0.0.1:8000/static"+ saveFileName
  json = "{\"status\":\"success\", \"imgurl\":\"" + imgurl + "\"}"
  response.write(json)

  return response