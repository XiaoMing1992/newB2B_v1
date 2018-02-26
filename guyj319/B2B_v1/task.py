import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "B2B_v1.settings")

import time
from car.models import car_table

def do_task2():
   while True:
      time.sleep(10)
      try:
        all_car=car_table.objects.all().order_by("date_valid")   #根据有效期来 升序 排序
        for i in range(len(all_car)):
            print(all_car[i].id)
      except:
          print('Error')


from PIL import Image

PicPathNameList = []
PicWidthList = []
PicHeightList = []

def GetPicInfo(file):

    global PicPathNameList
    global PicWidthList
    global PicHeightList

    try:
        image = Image.open(file)
        PicPathNameList.append(file)
        PicWidthList.append(image.size[0])
        PicHeightList.append(image.size[1])
    except IOError:
        pass

import os


def getAllImages(folder):
    assert os.path.exists(folder)
    assert os.path.isdir(folder)
    imageList = os.listdir(folder)
    return imageList



if __name__ == '__main__':
    #do_task2()
    print(getAllImages(r"I:\DjangoProject\B2B_v1\user_picture\13631257799"))