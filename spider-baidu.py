#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#本程序可以根据用户输入的关键字，在www.baidu.com上进行搜索。对搜索的结果，把url、keywords和describe提取出来。

from urllib import request
from urllib import parse
from urllib import error
from urllib.request import HTTPCookieProcessor
import http.cookiejar
import sys
import re
import math
import csv
import time
import random

def installNewOpener():
    '''安装新的opener，以便正确的处理Cookie'''
    opener=request.build_opener(HTTPCookieProcessor)
    request.install_opener(opener)
    
def getResult(**query):
    header={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'DNT':1,
        'Host':'www.baidu.com',
        'Upgrade-Insecure-Request':1,
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
    url_values=parse.urlencode(query)
    url=r'https://www.baidu.com/s?'+url_values
    req=request.Request(url,headers=header)
    try:
        respone=request.urlopen(req)
        page=respone.read()
    except (error.HTTPError,error.URLError):
        print ("网络异常，无法正常访问，程序自动退出")
        sys.exit()
    html=page.decode('utf-8')
    return html

def findUrls(html):
    '''从指定的html文件中提取出需要的url'''
    patturl=re.compile(r'<h3.*?href="(http://www.baidu.com/link\?url=[-\w]+)"',re.S|re.I)
    urls=re.findall(patturl,html)
    return urls

def getHtml(url):
    '''根据指定的url得到相应的html文件，同时返回打开的url'''
    req=request.Request(url)
    respone=request.urlopen(req)
    page=respone.read()
    try:
        html=page.decode('utf-8')
    except UnicodeDecodeError:
        html=page.decode('gb2312')
    except (error.HTTPError,error.URLError):
        print ("网络异常，无法正常访问，程序自动退出")
        sys.exit()
    return html

def getCaption(html):
    '''从指定的html文件中提取Caption'''
    pattCaption=re.compile(r'<h3 class="t.*">(.+?)</h3>',re.S|re.I)
    match=re.search(pattCaption,html)
    if match:
        caption=match.group(1)
        caption=re.sub(r'</?[^>]+>','',caption)
    else:
        print("内容为空，出现异常,程序自动退出")
        sys.exit()
    return caption
    
def main():
    installNewOpener()
    keywords=['abc','linux']
    for keyword in keywords:              #第一重循环：按关键字循环
        i=1                               #设置每个关键字的计数器
        print('正在处理关键字',keyword,'......')
        query={
            'ie':'utf-8',
            'f':8,
            'rsv_bp':0,
            'rsv_idx':1,
            'tn':'baidu',
            'wd':keyword,
            'rsv_pq':'fa37d4ff0000d1ed',
            'rsv_t':'7007O530L3w5bUBIauNrU7vgY9Le/bGc/tHMpPMsWore7vJKF8o1HDPvUmg',
            'rqlang':"cn",
            'rsv_enter':1,
            'rsv_sug3':12,
            'rsv_sug1':15,
            'rsv_sug7':100
            }
        result=getResult(**query)             #得到html文件
        urls=findUrls(result)[0:5]
        for url in urls:
            html=getHtml(url)
            caption=getCaption(html)
            print(i,u,caption)
            i += 1
            

if __name__=='__main__':
    main()

    

