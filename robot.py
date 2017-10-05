
import itchat
from itchat.content import *
import re
import os, sqlite3
import datetime
import requests

def store(received_date=None, title=None,
          url=None, sharer=None,
          text=None):
    #save into glinks.db
    db_file = os.path.join(os.path.dirname(__file__), 'glinks.db')
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(r"insert into glinks values ('%s', '%s', '%s', '%s', '%s')" % (title, text, url, sharer, received_date))
    except sqlite3.OperationalError:
        print('creating table glinks')
        cursor.execute('create table glinks(title text, text text,url text, sharer varchar(20), received_date text primary key )')
        cursor.execute(r"insert into glinks values ('%s', '%s', '%s', '%s', '%s')" % (title, text, url, sharer, received_date))
    try:  
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)

def query_all():

  conn = sqlite3.connect('glinks.db')
  cursor = conn.cursor()
  cursor.execute('select * from glinks')
  values = cursor.fetchall()
  print(values)
  cursor.close()
  conn.close()



def find_text(content):
    #不想用xml模块提取信息直接正则匹配出来
    content = content.replace(' ','A').replace('\n', 'A').replace('\t','A')
    pattern = r"<des>(.*?)</des>"
    r = re.compile(pattern)
    result = r.findall(content)[0]
    return result

def note():
    @itchat.msg_register(NOTE, isGroupChat=True)
    def deal_note(msg):
        try:
            pattern = r'邀请"(.*?)"加入了群聊'
            r = re.compile(pattern)
            result = r.findall(msg['Content'])[0]
            return(u"""
                    @%s
                    欢迎新同学，
                    为了便于交流
                    麻烦你动动小手修改一下备注,
                    格式：姓名 入学年份 学历 专业 
                    比如：凯伦 14级 硕士 计算机技术
                    ps: 群文件链接：sharing.zhuojiayuan.com""" % result)
        except Exception as e:
            print(e)

      
    @itchat.msg_register(['Sharing'],isGroupChat=True)
    def collect_links(msg):
        try:

            received_date = datetime.datetime.now()
            title = msg['FileName']
            url = msg['Url']
            sharer = msg['ActualNickName']
            text = find_text(content=msg['Content'])
            print(title, sharer, text, url, received_date)
            store(received_date=received_date,
                title=title,
                url=url,
                sharer=sharer,
                text=text)
            print('data stored done')

            #利用请求事件促发flask处理函数将以上的信息保存入flask应用数据库
            #可以查看controller/glinks.py的new函数
            r = requests.get('http://localhost:2333/glinks/new')
            print(r.status_code)
        except Exception as e:
            print(e)

def robot_run():
    print('runing')
    note()
    itchat.auto_login(hotReload=True)
    itchat.run()




if __name__ == '__main__':
    print('runing')
    note()
    itchat.auto_login(hotReload=True)
    itchat.run()
    # query_all()

