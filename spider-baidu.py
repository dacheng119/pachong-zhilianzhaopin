#!/usr/bin/env python3
#-*- coding:cp936 -*-
#本程序可以根据用户提供的关键字，在www.baidu.com上进行搜索。对搜索的结果，把超链接的caption、abstract和url提取出来。

from urllib import request
from urllib import parse
from urllib import error
from urllib.request import HTTPCookieProcessor
import http.cookiejar
import sys
import re
import csv
import time
import random
import colorama
from colorama import Fore
colorama.init(autoreset=True)

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
        print (Fore.LIGHTRED_EX+"现在网络异常，请排除网络故障后再次重试！")
        sys.exit()
    html=page.decode('utf-8')
    return html

def getCaptions(html):
    '''从指定的html文件中提取Caption'''
    captions=[]
    pattCaption=re.compile(r'<h3[^>]+><a[^>]+>(.+?)</a></h3>',re.S|re.I)
    match=re.findall(pattCaption,html)
    if match:
        match=match[0:5]
        for caption in match:
            caption=re.sub(r'&amp;','&',caption)
            caption=re.sub(r'&nbsp;','',caption)
            caption=re.sub(r'&lt;','<',caption)
            caption=re.sub(r'&gt;','>',caption)            
            caption=re.sub(r'</?[^>]+>','',caption)
            captions.append(caption)
    else:
        captions=[]
    return captions
    
def getAbstract(html):
    """从指定的网页中提取摘要信息"""
    abstracts=[]
    pattAbstract=re.compile(r'<div class="c-abstract[^>]+>(.+?)</div>',re.S|re.I)
    match=re.findall(pattAbstract,html)
    if match:
        match=match[0:5]
        for abstract in match:
            abstract=re.sub(r'&amp;','&',abstract)
            abstract=re.sub(r'&nbsp;','',abstract)
            abstract=re.sub(r'&lt;','<',abstract)
            abstract=re.sub(r'&gt;','>',abstract)            
            abstract=re.sub(r'</?[^>]+>','',abstract)
            abstracts.append(abstract)
    else:
        abstracts=[]
    return abstracts

def getUrl(html):
    """从指定的网页中提取url"""
    urls=[]
    pattUrl=re.compile(r'<div class="f13"><a[^>]+>(.+?)</a>',re.S|re.I)
    match=re.findall(pattUrl,html)
    if match:
        match=match[0:5]
        for url in match:
            url=re.sub(r'&amp;','&',url)
            url=re.sub(r'&nbsp;','',url)
            url=re.sub(r'&lt;','<',url)
            url=re.sub(r'&gt;','>',url)            
            url=re.sub(r'</?[^>]+>','',url)
            urls.append(url)
    else:
        urls=[]
    return urls

def main():
    installNewOpener()
    content=[]
    try:
        keywords=open(r'c:/keywords.txt','r',encoding='cp936')
    except:
        print(Fore.LIGHTRED_EX+r'读取"c:\keywords.txt"文件失败，程序异常退出!')
        print(Fore.LIGHTRED_EX+r'请确认"c:\keywords.txt"文件正常!\n')
        sys.exit()
    with open(r'c:/baidu.csv','w',encoding='cp936',newline='') as f: # newline极重要，否则会多出一个空白行
        writer=csv.writer(f)
        title=["关键词","标题","摘要","网址","排序"]
        writer.writerow(title)
        for k in keywords:              #第一重循环：按关键字循环
            keyword=k.strip()
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
            captions=getCaptions(result)
            abstracts=getAbstract(result)
            urls=getUrl(result)
            contents=zip(captions,abstracts,urls)
            for content in contents:
                content=list(content)
                content.insert(0,keyword)
                content.append(i)
                try:
                    writer.writerow(content)
                except UnicodeEncodeError:
                    print(Fore.LIGHTYELLOW_EX+'********关键字 "%s" 出错，请手工处理********' %keyword)
                    continue
                i += 1
            j=round(random.random(),2)
            time.sleep(j)
    print("\n")
    print(Fore.LIGHTGREEN_EX+r"所有关键字处理完毕，结果保存在c:\baidu.csv中")

if __name__=='__main__':
    main()
