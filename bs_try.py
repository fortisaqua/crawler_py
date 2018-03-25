from bs4 import BeautifulSoup
import WebCrawler
print WebCrawler.title_link

link_file=open('links/link_in_'+str(1234)+'.txt','w')
link_file.write("hello world\n")
link_file.close()