#coding=utf-8
import os
import re

def eachFile(filepath):
    pathDir =  os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))
        # child=allDir
        if child.split('.')[-1]=='htm':
            readFile(child)
            print child.decode('gbk') # .decode('gbk')是解决中文显示乱码问题


    # 逐行读取之后的正则匹配笨方法删除javascript内容
    # contents=fopen.readlines()
    # temp=""
    # for eachline in contents:
    #     temp+=eachline.strip('\n')
    # contents=temp
    # # 去掉script的内容
    # subs=re.findall(r"<script(.*?)>(.*?)</script>",contents,re.M|re.S)
    # for sub in subs:
    #     for sub_sub in sub:
    #         if len(sub_sub)>0:
    #             # print contents.find(sub_sub),"\n\n"
    #             contents=contents.replace(sub_sub,str(""))
def readFile(filename):
    fopen = open(filename, 'r')  # r 代表read
    fout = open('../content_each/'+filename[filename.find('/',7,len(filename))+1:filename.find('.',1,len(filename))]+'.txt','w')
    # print './contents/'+filename[filename.find('/')+1:filename.find('.',1,len(filename))]+'.txt'
    contents=fopen.read()
    # 去掉文本中的javascript内容
    rule1=re.compile(r"<script(.*?)>(.*?)</script>",re.S|re.M)
    contents=rule1.sub('',contents)
    # 去掉文本中的css内容
    rule1 = re.compile(r"<style(.*?)>(.*?)</style>", re.S | re.M)
    contents = rule1.sub('', contents)
    # 去掉文本中的标签
    rule2=re.compile(r'<[^>]+>',re.S)
    contents=rule2.sub('',contents)
    # print contents.splitlines(),'\n==================================\n'
    temp_con=""
    for line in contents.splitlines(): # 把多余的空格和空行去掉
        line=re.sub('\t+',' ',line)
        line = re.sub(' +', ' ', line)
        if len(line)>0 and line!=" ":
            temp_con+=line+'\n'
            fout.write(line+'\n')
    contents=temp_con
    # print contents
    # print contents.find("(function"),"\n"
    # print len(contents)
    fopen.close()
    fout.close()

def writeFile(filename):
    fopen = open(filename, 'w')
    print "\r请任意输入多行文字"," ( 输入 .号回车保存)"
    while True:
        aLine = raw_input()
        if aLine != ".":
            fopen.write('%s%s' % (aLine, os.linesep))
        else:
            print "文件已保存!"
            break
    fopen.close()



eachFile('./')
# readFile('./pages/3.htm')
