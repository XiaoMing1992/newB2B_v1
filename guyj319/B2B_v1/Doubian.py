# coding utf-8
import requests
from time import sleep
#from pymongo import MongoClient

#client = MongoClient('localhost', 27017)
#db = client.movie_test
#collection = db.top_api

url = 'http://api.douban.com/v2/movie/top250'
for start in range(0, 250, 25):
    r = requests.get(url, params={'start': start, 'count': 25})
    print('processing %s' % r.url)
    res = r.json()  # return dict
    for movie in res['subjects']:
        #collection.insert_one(movie)
        print(movie['title'], 'saved')
    sleep(0.1)
