__author__ = 'lailing'
#!/usr/bin/python
# -*- coding:utf8 -*-
import sys
from bs4 import BeautifulSoup
import MySQLdb
import os
reload(sys)
sys.setdefaultencoding('utf8')

def store(uid, info):
    conn = MySQLdb.connect(host='localhost', user='root', passwd='1234', db='cramsouhu',port=3316,charset='utf8')
    cursor = conn.cursor()
    follow_num = int(info[0])
    fan_num = int(info[1])
    twis_num = int(info[2])
    sql = "update users set fan_num=%s,follow_num=%s,twis_num=%s where uid=%s"
    param = (fan_num, follow_num, twis_num, str(uid))
    try:
        n = cursor.execute(sql, param)
        conn.commit()
        print n
    except MySQLdb.Error, e:
        conn.rollback()
        print 'Mysql Error %d: %s' % (e.args[0], e.args[1])
    conn.close()

def get_text_file(filename):
    if not os.path.exists(filename):
        print("ERROR: file not exit: %s" % (filename))
        return None
    if not os.path.isfile(filename):
        print("ERROR: %s not a filename." % (filename))
        return None
    f = open(filename, "r")
    content = f.read()
    f.close()
    return content

def get_souhu(soup):
    info = []
    ul = soup.find('div', {'class': "nexus"}).find('ul')
    if ul is not None:
        follow_num = ul.find('li', id="liFollowing").q.string
        fan_num = ul.find('li', {'data-tab-context': 'followedcategory'}).q.string
        twis_num = ul.find('li', {'class': 't3 on'}).q.string
        info.append(follow_num)
        info.append(fan_num)
        info.append(twis_num)
    else:
        print 'model is None'
    return info

def main_present(uid):
    user_dir = 'E:\\project\\cramPage\\mainPage\\' + str(uid) + '.html'
    html = get_text_file(user_dir)
    soup = BeautifulSoup(html)
    info = get_souhu(soup)
    print info
    # store(uid, info)

# def cramStep0():
#     conn1 = MySQLdb.connect(host='localhost', user='root', passwd='1234', db='cramsouhu', port=3316, charset='utf8')
#     cursor1 = conn1.cursor()
#     sql1 = "select uid from users where round=1"
#     try:
#         cursor1.execute(sql1)
#         data = cursor1.fetchone()
#         while data!=None:
#             uid = data[0]
#             print uid
#             i = 1
#             while (i<4):
#                 try:
#                     main_present(uid)
#                     break
#                 except:
#                     print 'main Deal', uid, 'faild', i
#                 i = i + 1
#             data = cursor1.fetchone()
#         conn1.commit()
#     except:
#         conn1.rollback()
#         print 'select faild'
#     conn1.close()

if __name__ == '__main__':
    # cramStep0()
    uid = '552658274'
    main_present(uid)


