#! -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET

def aaa():
    str_xml = "<xml>" \
               "<ToUserName><![CDATA[ddd]]></ToUserName>" \
               "<FromUserName><![CDATA[sss]]></FromUserName>" \
               "<CreateTime>1234567</CreateTime>" \
               "<MsgType><![CDATA[dd]]></MsgType>" \
               "<Content><![CDATA[vv]]></Content>" \
               "<FuncFlag>0</FuncFlag>" \
               "</xml>"
    xml = ET.fromstring(str_xml)
    print(xml)
    #xml = parseString(str_xml)
    #for node in xml.getElementsByTagName("ToUserName"):
    #    print (node.text)

    to_user = xml.find('ToUserName').text       #开发者微信号
    from_user = xml.find('FromUserName').text   #发送方帐号（一个OpenID）
    msg_type = xml.find('MsgType').text         #消息类型，event
    #event_name = xml.find('Event').text         #事件类型，CLICK
    #event_key = xml.find('EventKey').text       #事件KEY值，与自定义菜单接口中KEY值对应

    print(to_user)
    print(from_user)
    print(msg_type)
    #print(event_name)
    #print(event_key)

if __name__ == '__main__':
    aaa()


