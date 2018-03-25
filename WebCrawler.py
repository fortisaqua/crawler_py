# -*- coding: utf-8 -*-
import threading
import GetUrl
import urllib
from bs4 import BeautifulSoup
import re

g_mutex = threading.Lock()
g_pages = []  # 线程下载页面后，将页面内容添加到这个list中
g_dledUrl = []  # 所有下载过的url
g_toDlUrl = []  # 当前要下载的url
g_failedUrl = []  # 下载失败的url
title_link={} #下载下来的网页标题与超链接的键值对
title_file={} #下载下来的网页标题与文件位置的键值对
g_totalcount = 0  # 下载过的页面数

# FILENUM规定爬下来的页面的数量
FILENUM=5000
class WebCrawler:
    def __init__(self, threadNumber, Maxdepth):
        self.threadNumber = threadNumber
        self.threadPool = []
        self.Maxdepth = Maxdepth
        self.logfile = file('#log.txt', 'w')  ##
    def download(self, url, fileName):
        Cth = CrawlerThread(url, fileName)
        self.threadPool.append(Cth)
        Cth.start()

    def downloadAll(self):
        global g_toDlUrl
        global g_totalcount
        if g_totalcount > FILENUM:
            return
        i = 0
        while i < len(g_toDlUrl):
            j = 0
            while j < self.threadNumber and i + j < len(g_toDlUrl):
                g_totalcount += 1  # 进入循环则下载页面数加1
                if g_totalcount > FILENUM:
                    return
                self.download(g_toDlUrl[i + j], str(g_totalcount) + '.htm')
                print 'Thread started:', i + j, '--File number = ', g_totalcount
                j += 1
            i += j
            for th in self.threadPool:
                th.join(30)  # 等待线程结束，30秒超时
            self.threadPool = []  # 清空线程池
        g_toDlUrl = []  # 清空列表

    def updateToDl(self):
        global g_toDlUrl
        global g_dledUrl
        newUrlList = []
        for s in g_pages:
            newUrlList += GetUrl.GetUrl(s)  #######GetUrl要具体实现
        g_toDlUrl = list(set(newUrlList) - set(g_dledUrl))  # 提示unhashable

    def Craw(self, entryUrl):  # 这是一个深度搜索，到g_toDlUrl为空时结束
        g_toDlUrl.append(entryUrl)
        self.logfile.write('>>>Entry:\n')  ##
        self.logfile.write(entryUrl)  ##
        depth = 0
        if g_totalcount > FILENUM:
            return
        while len(g_toDlUrl) != 0 and depth <= self.Maxdepth:
            depth += 1
            print 'Searching depth ', depth, '...\n\n'
            if g_totalcount > FILENUM:
                return
            self.downloadAll()
            self.updateToDl()
            content = '\n>>>Depth ' + str(depth) + ':\n'  ##
            self.logfile.write(content)  ##
            i = 0  ##
            while i < len(g_toDlUrl):  ##
                content = str(g_totalcount + i + 1) + '->' + g_toDlUrl[i] + '\n'  # ##
                self.logfile.write(content)  ##
                i += 1  ##

class CrawlerThread(threading.Thread):
    def __init__(self, url, fileName):
        threading.Thread.__init__(self)
        self.url = url  # 本线程下载的url
        self.fileName = fileName

    def run(self):  # 线程工作-->下载html页面
        global g_mutex
        global g_failedUrl
        global g_dledUrl
        try:
            f = urllib.urlopen(self.url)
            s = f.read()
            soup = BeautifulSoup(s)
            # print soup.find('title'),self.url
            if soup.find('title')!=None:
                title_string=str(soup.find('title'))
                if not "orbidden" in title_string and not "Internal Server Error" in title_string and not "not found" in title_string:
                    numberstr=self.fileName[:str(self.fileName).find('.',1,len(str(self.fileName)))]
                    print numberstr
                    link_file=open('links/link_in_'+str(numberstr)+'.txt','w')
                    temp_s=s
                    # 去掉文本中的js内容
                    rule1 = re.compile(r"<script(.*?)>(.*?)</script>", re.S | re.M)
                    temp_s = rule1.sub('', temp_s)
                    # 去掉文本中的css内容
                    rule1 = re.compile(r"<style(.*?)>(.*?)</style>", re.S | re.M)
                    temp_s = rule1.sub('', temp_s)
                    urls=GetUrl.GetUrl(temp_s)
                    print urls
                    for url in urls:
                        link_file.write(url+"\n")
                    link_file.close()
                    temp_title=str(soup.find('title'))[7:]
                    temp_title = re.sub('\n+', ' ', temp_title)
                    temp_title = re.sub('\r+', ' ', temp_title)
                    temp_title = re.sub('\t+', ' ', temp_title)
                    temp_title = re.sub(' +', ' ', temp_title)
                    # temp_title=re.sub('\n',' ',temp_title)
                    title_link[temp_title]=self.url
                    title_file[temp_title] = self.fileName
            # else:
            #     title_link[str(soup.find('title'))] = self.url
            fout = file(self.fileName, 'w')
            fout.write(s)
            fout.close()
        except:
            g_mutex.acquire()  # 线程锁-->锁上
            g_dledUrl.append(self.url)
            g_failedUrl.append(self.url)
            g_mutex.release()  # 线程锁-->释放
            print 'Failed downloading and saving', self.url
            return None  # 记着返回!

        g_mutex.acquire()  # 线程锁-->锁上
        g_pages.append(s)
        g_dledUrl.append(self.url)
        g_mutex.release()  # 线程锁-->释放