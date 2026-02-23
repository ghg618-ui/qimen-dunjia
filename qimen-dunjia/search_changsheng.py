import urllib.request
import urllib.parse
from html.parser import HTMLParser

class SimpleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
    def handle_data(self, data):
        self.text.append(data)

url = "https://www.baidu.com/s?wd=" + urllib.parse.quote("奇门遁甲 十二长生 宫位 状态")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    parser = SimpleParser()
    parser.feed(html)
    text = "".join(parser.text)
    # just print some text around '长生'
    import re
    matches = re.findall(r'.{0,50}长生.{0,50}', text)
    for m in set(matches):
        print(m)
except Exception as e:
    print(e)
