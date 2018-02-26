#! -*- coding:utf-8 -*-
import jieba
seg_list = jieba.cut("我来到北京清华大学", cut_all = True)
print("Full Mode:", ' '.join(seg_list))

seg_list = jieba.cut("我来到北京清华大学")
print("Default Mode:", ' '.join(seg_list))

seg_list = jieba.cut("宝马奔驰8万")
print("Default Mode:", ' '.join(seg_list))

str="工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作辛苦了她"
seg_list = list(jieba.cut(str))
print(seg_list)
print(len(seg_list))

def lazyproperty(func):
    name = '_lazy_'+func.__name__
    @property
    def lazy(self):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            value = func(self)
            setattr(self, name, value)
            return value
    return lazy

#使用abc模块可以很轻松的定义抽象基类
from abc import ABCMeta, abstractclassmethod

class IStream(metaclass=ABCMeta):
    @abstractclassmethod
    def read(self, maxbytes=-1):
        '''
        抽象方法
        :param maxbytes:
        :return:
        '''
        pass

    @abstractclassmethod
    def write(self, data):
        '''
        抽象方法
        :param data:
        :return:
        '''
        pass

class SocketStream(IStream):
    def read(self, maxbytes=-1):
        pass

    def write(self, data):
        pass

def serialize( stream):
    if not isinstance(stream, IStream):
        raise TypeError('Expected an IStream')
    pass

if __name__ == '__main__':
    a = SocketStream()
    serialize(a)























