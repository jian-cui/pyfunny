from HTMLParser import HTMLParser
import urllib
import re
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        url = []
        try:
            if tag=='a' and attrs['class']=='title':
                print attrs['title']
                # url.append(attrs['title'])
                reply_comment() !!!!!!!!!!!!!!!!!!!!!!!!
        except:
            pass
    def handle_endtag(self, tag):
        if tag=='html':
            self.close()
    def handle_data(self, data):
        pass
class Autoreply:
    def __init(self):
        pass
    def reply(self, text):
        

while i:
    parser = MyHTMLParser()
    parser.feed(htmlthing)
