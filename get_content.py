#coding=utf-8
import os
def eachFile(filepath):
    pathDir =  os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))
        child=allDir
        print child.decode('gbk') # .decode('gbk')是解决中文显示乱码问题
    openfile=open('./titles/title_and_link.txt','r')
    for eachline in openfile.readlines():
        print eachline.split(' '),"\n\n"


eachFile('./')