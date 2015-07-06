#!/usr/bin/python
# -*- coding:utf8 -*-
import sys
import MySQLdb
from bs4 import BeautifulSoup
import os
import urllib2
import cookielib
import time
reload(sys)
sys.setdefaultencoding('utf8')

def downPage(page, dir):
    fileHandle = open(dir, 'w')
    html = page.read()
    fileHandle.write(html)
    fileHandle.close()

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

def get_page_num(soup):
    div = soup.find('div', {'class': 'stream'})
    p = div.find('p', {'class': 'page'})
    page_max = 1
    if p is not None:
        alist = p.findAll('a',  {'class': 'pg crjs_pg'})
        a_href = alist[len(alist) - 1].get('href')
        page_max = (int)(a_href.split('pageNo=')[1])
    return page_max

def intoFile(uid, infos):
    file_path = 'E:\\cramPage\\mainPage\\fans\\' + str(uid) + '_fans.txt'
    fileHandle = open(file_path, 'a')
    for info in infos:
        fileHandle.write(info[0] + ',')
    fileHandle.close()

def get_page(dir):
    html = get_text_file(dir)
    soup = BeautifulSoup(html)
    return  soup

def mark(uid):
    uid = str(uid)
    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='cramsouhu',port=3306,charset='gbk')
    cursor = conn.cursor()
    sql = "update users set cramAll=1 where uid='" + uid + "'"
    try:
        cursor.execute(sql)
        conn.commit()
        print 'mark', uid, 'OK'
    except:
        conn.rollback()
        print 'mark', uid, 'faild'
    conn.close()

def main_present(uid):
    first_page_dir = 'E:\\project\\cramPage\\mainPage\\' + str(uid) + '_twis_1.html'
    soup = get_page(first_page_dir)
    page_num = get_page_num(soup)
    print page_num
    if page_num > 1:
        count = 2
        while (page_num >= count and count<=10):
            page_dir = 'E:\\project\\cramPage\\mainPage\\' + str(uid) + '_twis_' + str(count) + '.html'
            soup = get_page(page_dir)
            count = count + 1
    mark(uid)

def cramStep():
    conn1 = MySQLdb.connect(host='localhost', user='root', passwd='', db='cramsouhu', port=3306, charset='gbk')
    cursor1 = conn1.cursor()
    sql1 = "select uid from users where round=3 and isValid=1 and cramMainPage=1 and cramAll=0"
    try:
        cursor1.execute(sql1)
        data = cursor1.fetchone()
        while data!=None:
            uid = str(data[0])
            print uid
            try:
                main_present(uid)
                time.sleep(1)
            except:
                'main deal', uid, 'faild'
            data = cursor1.fetchone()
        conn1.commit()
    except:
        conn1.rollback()
        print 'select faild'
    conn1.close()

if __name__ == '__main__':
    cramStep()
