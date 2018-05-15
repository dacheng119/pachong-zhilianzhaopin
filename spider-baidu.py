#!/usr/bin/env python3
#-*- coding:cp936 -*-
#��������ר��Ϊ���������г�����д�ģ����Ը����û��ṩ�Ĺؼ��֣���www.baidu.com�Ͻ��������������������ǰ5��ѳ����ӵ�caption��abstract��url��ȡ�������ؼ��ֱ�����c:\keywords.txt��Ҫ��ÿ��һ���ؼ��֣����Լӿո񡣽��������c:\baidu.csv�У�����ֱ����excel�򿪡�

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
    '''��װ�µ�opener���Ա���ȷ�Ĵ���Cookie'''
    opener=request.build_opener(HTTPCookieProcessor)
    request.install_opener(opener)
    
def getResult(**query):
    '''����ָ���Ĺؼ��ִ򿪰ٶȲ����ش򿪵�html�ļ�'''
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
        print (Fore.LIGHTRED_EX+"���������쳣�����ų�������Ϻ��ٴ����ԣ�")
        sys.exit()
    html=page.decode('utf-8')
    return html

def getContent(patt,htmlFile):
    """��ָ�����ļ�����ȡ��������ƥ�������"""
    l=[]
    match=re.findall(patt,htmlFile)
    if match:
        match=match[0:5]
        for m in match:
            m=re.sub(r'&amp;','&',m)
            m=re.sub(r'&nbsp;','',m)
            m=re.sub(r'</?[^>]+>','',m)
            l.append(m)                 # �ַ����ǲ��ɱ�ģ�����ʹ�����µı���
    return l

            
def main():
    installNewOpener()
    content=[]
    try:
        keywords=open(r'c:/keywords.txt','r',encoding='cp936')
    except:
        print(Fore.LIGHTRED_EX+r'��ȡ"c:\keywords.txt"�ļ�ʧ�ܣ������쳣�˳�!')
        print(Fore.LIGHTRED_EX+r'��ȷ��"c:\keywords.txt"�ļ����ڲ���û�б���������ʹ��!\n')
        sys.exit()

    pattCaption=re.compile(r'<h3[^>]+><a[^>]+>(.+?)</a></h3>',re.S|re.I)
    pattAbstract=re.compile(r'<div class="c-abstract[^>]+>(.+?)</div>',re.S|re.I)
    pattUrl=re.compile(r'<div class="f13"><a[^>]+>(.+?)</a>',re.S|re.I)
    
    with open(r'c:/baidu.csv','w',encoding='cp936',newline='') as f: # newline����Ҫ���������һ���հ���
        writer=csv.writer(f)
        title=["�ؼ���","����","ժҪ","��ַ","����"]
        writer.writerow(title)
        
        for k in keywords:              #���ؼ���ѭ��
            keyword=k.strip()
            i=1                         #����ÿ���ؼ��ֵļ�����
            print(Fore.LIGHTWHITE_EX+'���ڴ���ؼ���',Fore.LIGHTWHITE_EX+keyword,Fore.LIGHTWHITE_EX+'......') # ��ɫ�������
            query={                     # �ٶȵ���Щֵ��Ȼ��̫�����ʲô��˼��������Щ������ģ���ʱ���ٲ���
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
            result=getResult(**query)             #�õ�html�ļ�
            captions=getContent(pattCaption,result)
            abstracts=getContent(pattAbstract,result)
            urls=getContent(pattUrl,result)
            
            contents=zip(captions,abstracts,urls) # python3.6��zip���ص���һ������Ϊzip�ĵ�����
            for content in contents:
                content=list(content)
                content.insert(0,keyword)
                content.append(i)
                try:
                    writer.writerow(content)
                except UnicodeEncodeError:
                    print(Fore.LIGHTYELLOW_EX+'********�ؼ��� "%s" �������ֹ�����********' %keyword) # ��ɫ�������
                    continue
                i += 1
            j=round(random.random(),2)
            time.sleep(j)               # ����ȴ����ɺ���
    print("\n")
    print(Fore.LIGHTGREEN_EX+r"���йؼ��ִ�����ϣ����������c:\baidu.csv��") # ��ɫ�������

if __name__=='__main__':
    main()
