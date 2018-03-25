#coding=utf-8
import re
from bs4 import BeautifulSoup

# temp_title = re.sub('\n+', ' ', temp_title)
# temp_title=re.sub('\n',' ',temp_title)

tag = 0
contents=open('title_and_file.txt','r')
infile=open('title_and_file_new.txt','w')
# print contents.read()
for line in contents.readlines():
    inner_lines=line.split('</title>')
    for inner in inner_lines:
        if len(inner)==0:
            tag=1
    if tag==0:
        line=re.sub('\n',' ',line)
        line = re.sub('\r+',' ',line)
        line = re.sub('\t+',' ',line)
        line = re.sub(' +', ' ', line)
        infile.write(line+'\n')
# lines=contents.read().split('</title>')
# print lines