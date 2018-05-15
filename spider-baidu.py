#!/usr/bin/env python3
#-*- coding:cp936 -*-
#本程序是专门为清美教育市场部编写的，可以根据用户提供的关键字，在www.baidu.com上进行搜索。对搜索结果的前5项，把超链接的caption、abstract和url提取出来。关键字保存在c:\keywords.txt，要求每行一个关键字，可以加空格。结果保存在c:\baidu.csv中，可以直接用excel打开。

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
    '''根据指定的关键字打开百度并返回打开的html文件'''
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

def getContent(patt,htmlFile):
    """从指定的文件中提取和正则相匹配的内容"""
    l=[]
    match=re.findall(patt,htmlFile)
    if match:
        match=match[0:5]
        for m in match:
            m=re.sub(r'&amp;','&',m)
            m=re.sub(r'&nbsp;','',m)
            m=re.sub(r'</?[^>]+>','',m)
            l.append(m)                 # 字符串是不可变的，所以使用了新的变量
    return l

            
def main():
    installNewOpener()
    content=[]
    try:
        keywords=open(r'c:/keywords.txt','r',encoding='cp936')
    except:
        print(Fore.LIGHTRED_EX+r'读取"c:\keywords.txt"文件失败，程序异常退出!')
        print(Fore.LIGHTRED_EX+r'请确认"c:\keywords.txt"文件存在并且没有被其它程序使用!\n')
        sys.exit()

    pattCaption=re.compile(r'<h3[^>]+><a[^>]+>(.+?)</a></h3>',re.S|re.I)
    pattAbstract=re.compile(r'<div class="c-abstract[^>]+>(.+?)</div>',re.S|re.I)
    pattUrl=re.compile(r'<div class="f13"><a[^>]+>(.+?)</a>',re.S|re.I)
    
    with open(r'c:/baidu.csv','w',encoding='cp936',newline='') as f: # newline极重要，否则会多出一个空白行
        writer=csv.writer(f)
        title=["关键词","标题","摘要","网址","排名"]
        writer.writerow(title)
        
        for k in keywords:              #按关键字循环
            keyword=k.strip()
            i=1                         #设置每个关键字的计数器
            print(Fore.LIGHTWHITE_EX+'正在处理关键字',Fore.LIGHTWHITE_EX+keyword,Fore.LIGHTWHITE_EX+'......') # 白色高亮输出
            query={                     # 百度的这些值仍然不太清楚是什么意思，怀疑有些是随机的，有时间再测试
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
            captions=getContent(pattCaption,result)
            abstracts=getContent(pattAbstract,result)
            urls=getContent(pattUrl,result)
            
            contents=zip(captions,abstracts,urls) # python3.6中zip返回的是一个类型为zip的迭代器
            for content in contents:
                content=list(content)
                content.insert(0,keyword)
                content.append(i)
                try:
                    writer.writerow(content)
                except UnicodeEncodeError:
                    print(Fore.LIGHTYELLOW_EX+'********关键字 "%s" 出错，请手工处理********' %keyword) # 黄色高亮输出
                    continue
                i += 1
            j=round(random.random(),2)
            time.sleep(j)               # 随机等待若干毫秒
    print("\n")
    print(Fore.LIGHTGREEN_EX+r"所有关键字处理完毕，结果保存在c:\baidu.csv中") # 绿色高亮输出

if __name__=='__main__':
    main()
