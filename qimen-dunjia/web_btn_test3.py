import urllib.request
import urllib.parse
from html.parser import HTMLParser
import re

class SimpleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
    def handle_data(self, data):
        self.text.append(data)

url = 'https://www.baidu.com/s?wd=' + urllib.parse.quote('热卜奇门 长生状态 怎么显示')
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    parser = SimpleParser()
    parser.feed(html)
    t = "".join(parser.text).replace("\n", "")
    for m in set(re.findall(r'.{0,40}长生.{0,40}', t)):
        print(m.strip())
except Exception as e:
    print(e)
