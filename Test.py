# -*- coding: utf-8 -*-
import WebCrawler,re
url = raw_input('设置入口url(例-->http://www.baidu.com): \n')
thNumber = int(raw_input('设置线程数:'))  # 之前类型未转换出bug
Maxdepth = int(raw_input('最大搜索深度：'))

wc = WebCrawler.WebCrawler(thNumber, Maxdepth)
wc.Craw(url)

title_file=open(r'titles/title_and_link.txt','w')
for key,value in WebCrawler.title_link.items():
    if len(key)>1 and len(value)>1:
        # key = re.sub('\n+', ' ', key)
        # key = re.sub('\n', ' ', key)
        title_file.write(key)
        title_file.write(value+"\n")
    # print type(key),type(value),"\n"
# print title_file
title_file.close()

title_filename=open(r'titles/title_and_file.txt','w')
for key,value in WebCrawler.title_file.items():
    if len(key)>1 and len(value)>1:
        # key = re.sub('\n+', ' ', key)
        # key = re.sub('\n', ' ', key)
        title_filename.write(key)
        title_filename.write(value+"\n")
    # print type(key),type(value),"\n"
# print title_file
title_filename.close()

# contents.eachFile('./')