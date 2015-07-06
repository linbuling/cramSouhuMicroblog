#!/usr/bin/python
# -*- coding: gbk -*-
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

#update mode
def updateData(sql, param):
    n = 0
    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='cramsouhu', port=3306)
    cursor = conn.cursor()
    try:
        n = cursor.execute(sql, param)
        conn.commit()
    except MySQLdb.Error, e:
        conn.rollback()
        print 'Mysql Error %d: %s' % (e.args[0], e.args[1])
    conn.close()
    return n

#query mode
def queryData(sql):
    query_data = []
    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='cramsouhu', port=3306)
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        data = cursor.fetchone()
        while data != None:
            query_data.append(data[0])
            data = cursor.fetchone()
        conn.commit()
    except MySQLdb.Error, e:
        conn.rollback()
        print 'Mysql Error %d: %s' % (e.args[0], e.args[1])
    conn.close()
    return query_data

#cram user's information from main page
def get_mainInfo(soup):
    info = []
    try:
        #div of three main infomations
        ul = soup.find('div', {'class': "nexus"}).find('ul')
        if ul is None:
            #cram twice
            return 'repeat'
        else:
            print 'ul right'
        follow_num = ul.find('li', id="liFollowing").q.string
        fan_num = ul.find('li', {'data-tab-context': 'followedcategory'}).q.string
        twis_num = ul.find('li', {'class': 't3 on'}).q.string
        if twis_num is None:
            return 'repeat'
        elif int(twis_num) == 0:
            #if this user has no twis, mark the user 'isvalid=0'
            return 'unValid'
        else:
            print 'twis_num right'
        #div of user's attributes
        user_div = soup.find('div', {'class': "aps usrStat"})
        user_info_div = user_div.find('div', {'class': "usr"})
        local = user_info_div.find('q', {'class': 'local'}).string
        bio = user_div.find('p', {'class': 'bio'}).string
        labels = ''
        labels_div = user_div.find('dl', {'class': 'usrInf'})
        if labels_div is not None:
            labels_a = labels_div.find('dd').find('div', {'class': 'label'}).findAll('a')
            for label_a in labels_a:
                label_str = label_a.string
                labels = labels + label_str + ','
        info.append(int(follow_num))
        info.append(int(fan_num))
        info.append(int(twis_num))
        info.append(str(local))
        info.append(str(bio))
        info.append(str(labels))
    except:
        print 'cram error'
        return 'repeat'
    return info

def main_present(uid):
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    loginURL = 'https://passport.sohu.com/sso/login.jsp?userid=cramsohu%40sohu.com&password=3dc03c908ff00e47d9813e84b5de0c91&appid=1073&persistentcookie=1&s=1409711232023&b=2&w=1152&pwdtype=1&v=26'
    req = urllib2.Request(loginURL)
    result = opener.open(req)
    main_url = 'http://t.sohu.com/people?uid=' + uid
    req = urllib2.Request(main_url)
    result = opener.open(req)
    main_path = 'E:\\project\\cramPage\\mainPage\\' + uid + '.html'
    downPage(result, main_path)
    soup = BeautifulSoup(result)
    mainInfo = get_mainInfo(soup)
    if isinstance(mainInfo, basestring):
        if mainInfo.find('unValid') != -1:
            sql_del = "update users set isValid=0 where uid=%s"
            param_del = str(uid)
            n1 = updateData(sql_del, param_del)
            return 'continue'
        if mainInfo.find('repeat') != -1:
            return 'repeat'
    else:
        sql_update = "update users set follow_num=%s,fan_num=%s,twis_num=%s,local=%s,bio=%s,label=%s where uid=%s"
        param_update = (mainInfo[0], mainInfo[1], mainInfo[2], mainInfo[3], mainInfo[4],mainInfo[5], str(uid))
        n2 = updateData(sql_update, param_update)
        if n2 > 0:
            print 'update', uid, 'info success'
        sql_mark = "update users set cramMainPage=1 where uid=%s"
        param_mark = str(uid)
        n3 = updateData(sql_mark, param_mark)
        print 'down and mark', uid, 'success'
        return 'true'

def cramStep3_1():
    sql1 = "select uid from users where round=1 and isValid=1 and cramThreePage=1 and cramMainPage=0 LIMIT 0,600"
    data = queryData(sql1)
    if len(data) > 0:
        for user in data:
            uid = str(user)
            print uid
            count = 1
            while count < 4:
                main_result = main_present(uid)
                if main_result.find('repeat') == -1:
                    break
                time.sleep(5)
                count = count + 1

#主函数，OK
if __name__ == '__main__':
    cramStep3_1()
