import requests
from lxml import etree

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
        }


class Spider():
    def __init__(self, url):
        self.url = url

    def setUrl(self, url):
        self.url = url

    def getJson(self):
        page_text = requests.get(url=self.url, headers=headers)
        if page_text:
            page_text = page_text.json()
            return page_text

    def getPostjson(self, postdata):
        page_text = requests.post(url=self.url, headers=headers, data=postdata)
        if page_text:
            page_text = page_text.json()
            return page_text

    def getHtml(self):
        # page_text = requests.post(url=self.url, headers=headers).text
        # print(page_text)
        #
        # tree = etree.HTML(page_text)
        # return 1
        pass



if __name__ == '__main':
    myspider = Spider("https://xuangubao.cn/dingpan")
    # print(myspider)