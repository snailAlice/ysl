#-*- coding : utf -8 -*-
import requests;
import json;
import os
import re
import pymysql

def dbHandle():
    conn = pymysql.connect(
        host='localhost',
        user='wxy',
        passwd='wxy@2017',
        charset='utf8',
        use_unicode=False
    )
    return conn

headersParameters = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'Mozilla/6.1 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }
page = 0
while page<99:
    page += 1
    urlparams = {'itemId':'43487174504','sellerId':'2298016439','currentPage':str(page)}
    repones = requests.get('https://rate.tmall.com/list_detail_rate.htm',params=urlparams,headers=headersParameters)

    jsondata = repones.text[15:]
    data = json.loads(jsondata)
    for list in data['rateList']:
        pics_url = ''
        for pics in list['pics']:
            pics_url = pics_url + "http:" + str(pics)+ " "
        pics_urls = pics_url
        #print(pics_urls)
        #print list['displayUserNick']
        #print list['auctionSku']
        #print list['cmsSource']
        #print list['rateDate']
        #print list['sellerId']
        #print list['rateContent']

        dbObject = dbHandle()
        cursor = dbObject.cursor()
        cursor.execute("USE ysl")
        sql = 'insert into ysl_tab(displayUserNick,auctionSku,cmsSource,rateDate,sellerId,rateContent,pics_urls) values (%s,%s,%s,%s,%s,%s,%s)'
        try:
            cursor.execute(sql, (list['displayUserNick'],list['auctionSku'], list['cmsSource'], list['rateDate'],list['sellerId'],list['rateContent'],pics_urls))
            dbObject.commit()
        except Exception, e:
            print (">>>>>>>>>>",e,"<<<<<<<<<<<<<<<<<<")
            dbObject.rollback()
