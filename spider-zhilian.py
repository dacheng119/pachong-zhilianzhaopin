#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#本程序是以"java工程师"为关键字，在www.zhaopin.com上进行搜索。对搜索的结果，把"岗位职责"和"任职要求"提取出来。

from urllib import request
from urllib import parse
from urllib.request import HTTPCookieProcessor
import http.cookiejar
import re
import csv

opener=request.build_opener(HTTPCookieProcessor)
request.install_opener(opener)
header={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    # 'Accept-Encoding':'gzip, deflate',  加上这行会出错
    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'DNT':'1',
    'Host':'sou.zhaopin.com',
    # 'Referer':'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%e7%9f%b3%e5%ae%b6%e5%ba%84&kw=java%e5%b7%a5%e7%a8%8b%e5%b8%88&sm=0&sg=41cbf4be4dc242a4b9fd69486d0b779d&p=9',
    # 'Upgrade-Insecure-Requests':'1',  加上会出错
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
values={
    'jl':'石家庄',
    'kw':'java工程师',
    'sm':0,
    'p':1
}
url_values=parse.urlencode(values)
url=r'http://sou.zhaopin.com/jobs/searchresult.ashx?'+url_values
req=request.Request(url,headers=header)
respone=request.urlopen(req)
page=respone.read()
html=page.decode('utf-8')

patturl=re.compile(r'(http://jobs.zhaopin.com/\d{15}.htm).*?java.*?</a>',re.I)
urls=re.findall(patturl,html)
pattcont=re.compile(r'(?<=<div class="tab-inner-cont">)(.+?)(?=</div>)',re.S) #re.S很重要
pattgwzz=re.compile(r'((岗位职责|岗位描述)?.*?((\d.+\n)+))') #,re.S)
pattzwyq=re.compile(r'((任职要求|职位要求)?.*?((\d.+\n)+))') #,re.S)


csvfile=open(r'java.csv','w')
writer=csv.writer(csvfile)
writer.writerow(['序号','岗位职责','职位要求'])
i=1
for url in urls:
    req=request.Request(url)
    respone=request.urlopen(req)
    page=respone.read()
    html=page.decode('utf-8')
    match=re.search(pattcont,html)
    if match:
        content=(match.group(1))
        content=content.strip()
        content=re.sub(r'&nbsp;','',content)
        content=re.sub(r'<[^>]+>','',content)
        content=re.sub(r'\r','\\n',content)
        content=re.sub(r'(\d)、',r'\1.',content)
        content=re.sub(r'(\d+.)',r'\n\1',content)
        content=re.sub(r'(HTML)\s+(5)',r'\1\2',content)
        content=re.sub(r'(B)\s+(2B|2C)',r'\1\2',content)
        content=re.sub(r'J\s2EE','J2EE',content)
        content=re.sub(r'\s*(\d+)\s*(年|c|C|个|点|号|室|天|P|等|岁|:|-|K|,|，|\d+| |：|元|k)',r'\1\2',content)
        content=re.sub(r'(任职要求|职位要求|工作时间|福利待遇|公司优势|上班时间)',r'\n\1',content)
        
        gwzzText=re.search(pattgwzz,content)
        if gwzzText:
            gwzz=gwzzText.group(3)

        zwyqText=re.search(pattzwyq,content)
        if zwyqText:
            zwyq=zwyqText.group(3)
        l=[]
        l.append(i)
        l.append(gwzz)
        l.append(zwyq)
        writer.writerow(l)
        i+=1
csvfile.close()


        # content=re.sub(r'(任职要求：|职位要求：|职位要求：|岗位职责：|工作时间：|岗位描述：|福利待遇：|公司优势：|上班时间：)(?!=\n)',r'\1\n',content)
        # content=re.sub(r'(任职要求|职位要求|岗位职责|工作时间|岗位描述|福利待遇|公司优势|上班时间)(?!=：)',r'\1：',content)
        # content=re.sub(r'：：',':',content)
        # content=re.sub(r'(Struts)\s+(2|1)',r'\1\2',content)
        # content=re.sub(r'(db)\s+(2)',r'\1\2',content)
        # content=re.sub(r'\n\n+',r'\n\n',content)
        # content=re.sub(r'(：)\s+(1\.)',r'\1\2',content)
#        print(content)
#    else:
 #       print("not found")

