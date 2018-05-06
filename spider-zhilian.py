#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#本程序是以"java工程师"为关键字，在www.zhaopin.com上进行搜索。对搜索的结果，把"岗位职责"和"任职要求"提取出来。

from urllib import request
from urllib import parse
from urllib import error
from urllib.request import HTTPCookieProcessor
import http.cookiejar
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
        'DNT':'1',
        'Host':'sou.zhaopin.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
    url_values=parse.urlencode(query)
    url=r'https://sou.zhaopin.com/jobs/searchresult.ashx?'+url_values
    req=request.Request(url,headers=header)
    respone=request.urlopen(req)
    page=respone.read()
    html=page.decode('utf-8')
    return html

def findUrls(html):
    '''从指定的html文件中提取出正在招聘的职位的url'''
    patturl=re.compile(r'(http://(?:jobs|xiaoyuan).zhaopin.com/(?:job/)?(?:\d{20}|\d{15}|\w{23})(?:.htm)?)',re.I) #验证：每页最多60个职位
    urls=re.findall(patturl,html)
    return urls

def getHtml(url):
    '''根据指定的url得到相应的html文件'''
    req=request.Request(url)
    respone=request.urlopen(req)
    page=respone.read()
    html=page.decode('utf-8')
    return html
    
def getZhiWei(html):
    pattZhiWei=re.compile(r'<h1[^>]*?>(.*)</h1>',re.I|re.S)
    match=re.search(pattZhiWei,html)
    if match:
        zhiWei=match.group(1)        
        zhiWei=re.sub(r'</?[^>]*?>','',zhiWei)
        zhiWei=zhiWei.strip()
    else:
        zhiWei=''
    return zhiWei

def getCompany(html):
    '''从指定的html文件中抽取发布招聘信息的企业的名字'''
    pattCompany1=re.compile(r'</h1>\s+<h2>(.*?)</h2>',re.I|re.S)
    pattCompany2=re.compile(r'<a.*?/subcompany/.*?>(.*?)</a>',re.I|re.S)
    match1=re.search(pattCompany1,html)
    match2=re.search(pattCompany2,html)
    if match1:
        company=match1.group(1)
        company=re.sub(r'</?[^>]*>','',company)
    elif match2:
        company=match2.group(1)
        company=re.sub(r'</?[^>]*?>','',company)
    else:
        company=''
    return company

def getRenShu(html):
    '''从指定的html文件中抽取招聘的人数'''
    pattRenShu=re.compile(r'招聘人数.*?(\d+|若干)人?',re.S)
    match=re.search(pattRenShu,html)
    if match:
        renShu=match.group(1)
    else:
        renShu=''
    return renShu

def getPageNumber(html):
    '''从搜索的第1页结果中提取共有多少个职位满足条件'''
    pattNumber=re.compile(r'共<em>(\d+)</em>个职位满足条件')
    match=re.search(pattNumber,html)
    if match:
        numbers=match.group(1)
        number=int(numbers)
        pageNumber=math.ceil(number / 60)   #math.ceil()用于向上取整
    else:
        pageNumber=0
    return pageNumber

def getContent(html):
    '''从指定的html中提取岗位职责和职位要求和具体内容'''
    patt1=re.compile(r'<div class="tab-inner-cont">(.+?)</div>',re.S) #针对形如http://jobs.zhaopin.com/216380732279322.htm的URL
    patt2=re.compile(r'<p class="mt20">(.+?)</p>',re.S)   #针对形如http://xiaoyuan.zhaopin.com/的URL

    match1=re.search(patt1,html)
    match2=re.search(patt2,html)
    if match1:
        content=match1.group(1)
    elif match2:
        content=match2.group(1)
    else:
        content=None
    return content

def getGwzzAndRzyq(content):
    if content:
        content=re.sub(r'</?[^>]*>','',content)       #删除所有html标记
        content=re.sub(r'、','.',content)             #顿号的匹配总不正常，索性换成点号了
        content=re.sub(r'：',':',content)             #中文冒号替换为英文冒号
        content=re.sub(r'\r',r'\n',content)
        content=re.sub(r'（','(',content)
        content=re.sub(r'）',')',content)
        content=re.sub(r'&nbsp;','',content)
        content=re.sub(r'((?:岗位职责|岗位描述|岗位说明|工作职责|工作内容|任职要求|职位要求|职位描述|技术要求|要求\b|岗位要求|任职资格|优选条件|工作地址|\b待遇|\b福利待遇|招聘|薪资待遇|工作时间|上班时间|公司优势|应聘条件):?)',r'\n\1\n',content)
        content=re.sub(r'(\d+\.)',r'\n\1',content)   #把1.或12.修整为\n1.或\n12.
        content=re.sub('(\([一二三四五六七八九]\))',r'\n\1',content) #把(一)替换为\n(一)的形式
        content=re.sub(r'(\(\d+(\.)?\))',r'\n\1',content)   #把(1)修整为\n(1)的形式
        content=re.sub(r'(\s)+',r'\1',content)              #把多个换行或空白整理为一个
        content=re.sub(r'((?:岗位职责|岗位描述|岗位说明|工作职责|工作内容|任职要求|职位要求|职位描述|技术要求|要求\b|岗位要求|任职资格|优选条件|工作地址|\b待遇|\b福利待遇|招聘|薪资待遇|工作时间|上班时间|公司优势|应聘条件):?)',r'\n\n\1',content)

        pattgwzz=re.compile(r'(?:岗位职责|职位描述|岗位描述|工作职责|工作内容|岗位说明|岗位要求):?(.+?)\n\n',re.S)
        matchgwzz=re.search(pattgwzz,content)
        if matchgwzz:
            gwzz=matchgwzz.group(1)
        else:
            gwzz='无'

        pattrzyq=re.compile(r'(?:任职要求|职位要求|技术要求|要求|岗位要求|应聘条件|应聘要求|任职资格|优选条件):?(.+?)\n\n',re.S)
        matchrzyq=re.search(pattrzyq,content)
        if matchrzyq:
            rzyq=matchrzyq.group(1)
        else:
            rzyq='无'
    else:
        gwzz='无'
        rzyq='无'
    return(gwzz,rzyq)

def main():
    installNewOpener()
    keywords=['linux运维','安全工程师']#,'系统工程师','系统集成工程师','网络管理员','云计算工程师'] #系统集成工程师、系统工程师的职位很多
    for keyword in keywords:              #第一重循环：按关键字循环
        n=1                           #设置职位的计数器
        print('正在处理关键字',keyword,'......')
        filename='%s-zhilian.csv' %keyword
        with open(filename,'w') as f:
            writer=csv.writer(f)
            caption=['序号','网址','公司名称','招聘岗位','招聘人数','岗位职责','职位要求']
            writer.writerow(caption)
            query={
                'jl':'石家庄+北京',
                'kw':keyword,
                'sm':0,
                'p':1,
                'sf':0,
                'st':99999,
                'isadv':1
                }
            result=getResult(**query)             #得到html文件
            pageNumber=getPageNumber(result)
            pages=pageNumber+1
            for page in range(1,pages):              #第二重循环：按页数循环
                print("\t共%d页，正在处理第%d页 ......" %(pageNumber,page))
                query={
                'jl':'石家庄+北京',
                'kw':keyword,
                'sm':0,
                'p':page,
                'sf':0,
                'st':99999,
                'isadv':1
                }
    #            print(query)
                url_values=parse.urlencode(query)
                url=r'https://sou.zhaopin.com/jobs/searchresult.ashx?'+url_values
                html=getHtml(url)
                urls=findUrls(html)
                total=len(urls)
                i=1                       #定义本页的计数器
                for url in urls:              #第三重循环：按url循环
                    print("\t\t第%d页共%d个职位，正在处理%d个 ......" %(page,total,i))
                    l=[]                          #定义空列表，保存内容，以便写入csv文件
                    try:
                        html=getHtml(url)
                    except error.HTTPError:
                        print('HTTPError错误',url)
                    companyName=getCompany(html)
                    zhaopingangwei=getZhiWei(html)
                    zhaopinrenshu=getRenShu(html)
                    content=getContent(html)
                    gangweizhize,renzhiyaoqiu=getGwzzAndRzyq(content)
                    l.append(n)
                    l.append(url)
                    l.append(companyName)
                    l.append(zhaopingangwei)
                    l.append(zhaopinrenshu)
                    l.append(gangweizhize)
                    l.append(renzhiyaoqiu)
                    writer.writerow(l)
                    n +=1
                    i +=1
                    j=round(random.random(),2)   #随机等待若干毫秒
                    time.sleep(j)
                
if __name__=='__main__':
    main()

    

