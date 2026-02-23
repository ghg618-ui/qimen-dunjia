import urllib.request
import json
import urllib.parse
url = "https://www.baidu.com/s?wd=" + urllib.parse.quote("热卜奇门遁甲 隐干 排法")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    for h3 in soup.find_all('h3'):
        print(h3.text)
except Exception as e:
    print(e)
