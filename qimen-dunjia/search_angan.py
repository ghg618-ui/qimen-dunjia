import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re

url = "https://www.baidu.com/s?wd=" + urllib.parse.quote("奇门 暗干 值使宫起")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    for h3 in soup.find_all('h3'):
        print(h3.text)
        a = h3.find('a')
        if a:
            print(a.get('href'))
except Exception as e:
    print(e)
