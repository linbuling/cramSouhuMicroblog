#!/usr/bin/python
# -*- coding:utf8 -*-
import sys
import MySQLdb
from bs4 import BeautifulSoup
import os
import urllib2
import cookielib
import time

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

#获取最大页数
def get_page_num(soup):
    div = soup.find('div', {'class': 'ap stream'}).find('div', id="t-groupbys")
    p = div.find('p', {'class': 'page'})
    page_num = 1
    if p is not None:
        alist = p.findAll('a',  {'class': 'pg crjs_pg'})
        a_href = alist[len(alist) - 1].get('href')
        page_num = (int)(a_href.split('pageNo=')[1])
    return page_num

#将在当前关注页面上爬到的用户信息存入数据库
def store(informations):
    # 打开数据库连接
    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='cramsouhu', port=3306)
    # 使用cursor()方法获取操作游标
    cursor = conn.cursor()
    for info in informations:
        uid = str(info[0])
        title = str(info[1])
        sql = "insert into users(uid,title) values('" + uid + "','" + title + "')"
        try:
            cursor.execute(sql)
            conn.commit()
            print 'insert', uid, 'success'
        except:
            conn.rollback()
            print 'insert', uid, 'faild'
    # 关闭数据库连接
    conn.close()

#爬取当前页面，从每个usr_div中提取出需要的信息，将得到的uid和title存入数据库
def get_users(user_id, soup):
    div = soup.find('div', {'class': 'usrLis'})
    usrs_div = div.findAll('div', {'class': 'usr'})
    infos = []
    for usr_div in usrs_div:
        info = []
        a = usr_div.find('p', {'class': 'avt'}).find('a')
        uid = a.get('href').split('uid=')[1]
        title = a.get('title')
        info.append(uid)
        info.append(title)
        infos.append(info)
    store(infos)

def get_page(dir):
    html = get_text_file(dir)
    soup = BeautifulSoup(html)
    return  soup

def mark(uid1):
    uid = str(uid1)
    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='cramsouhu', port=3306)
    cursor = conn.cursor()
    sql = "update users set cramFollows_3=1 where uid='" + uid + "'"
    try:
        cursor.execute(sql)
        conn.commit()
        print 'update', uid, 'OK'
    except:
        conn.rollback()
        print 'update faild'
    conn.close()

def main_present(uid1):
    uid = str(uid1)
    user_dir = 'E:\\project\\cramPage\\followPage\\' + uid + '.html'
    soup = get_page(user_dir)
    page_num = get_page_num(soup)
    if page_num > 1:
        page_dir = 'E:\\project\\cramPage\\followPage\\' + uid + '_2.html'
        cookie = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        loginURL = 'https://passport.sohu.com/sso/login.jsp?userid=cramsohu%40sohu.com&password=3dc03c908ff00e47d9813e84b5de0c91&appid=1073&persistentcookie=1&s=1409711232023&b=2&w=1152&pwdtype=1&v=26'
        req = urllib2.Request(loginURL)
        result = opener.open(req)
        page_url = 'http://t.sohu.com/follow/following?uid=' + uid + '&pageNo=2'
        page_dir = 'E:\\project\\cramPage\\followPage\\' + uid + '_2.html'
        req = urllib2.Request(page_url)
        time.sleep(5)
        result = opener.open(req)
        downPage(result, page_dir)
        soup = get_page(page_dir)
        get_users(uid, soup)
    mark(uid)

def cramStep2_2():
    conn1 = MySQLdb.connect(host='localhost', user='root', passwd='', db='cramsouhu', port=3306)
    cursor1 = conn1.cursor()
    sql1 = "select uid from users where round in (1,2,3) and cramFollows_3=0"
    try:
        cursor1.execute(sql1)
        data = cursor1.fetchone()
        while data!=None:
            uid = data[0]
            print uid
            main_present(uid)
            data = cursor1.fetchone()
        conn1.commit()
    except:
        conn1.rollback()
        print 'select faild'
    conn1.close()

if __name__ == '__main__':
    #cramStep2_2()
    main_present(1000016)
