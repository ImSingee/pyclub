#coding=utf-8

import itchat
from itchat.content import *
import requests
import re


def find_text(content):
    #不想用xml模块提取信息直接正则匹配出来
    content = content.replace(' ','A').replace('\n', 'A').replace('\t','A')
    pattern = r"<des>(.*?)</des>"
    r = re.compile(pattern)
    result = r.findall(content)[0]
    return result

def run():
    @itchat.msg_register(['Text'])
    def reply(msg):
        print(msg)
    @itchat.msg_register(itchat.content.SHARING)
    def collect_links(msg):
        # print(msg)
        try:
            title = msg['FileName']
            url = msg['Url']
            # sharer = msg['ActualNickName']
            # sharer = msg['UserName']
            text = find_text(content=msg['Content'])
            sharer = "路人甲"
            data = {"title":title,
                    "text":text,
                    "url":url,
                    "sharer":sharer,
                    "token":"5201314666"}
            print(data)

            r = requests.post(url="http://localhost:2333/sharing/new",data=data)
            print(r.text)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    print('runing')
    run()
    itchat.auto_login(hotReload=True)
    itchat.run()