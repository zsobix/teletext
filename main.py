# ummm

import requests
from bs4 import BeautifulSoup



class TeletextReader:
    def __init__(self):
        self.pagenum = "100"
        self.subpage = "01"
        self.getPage()

    def getPage(self):
        url = f"https://teletext.hu/mtv1/{self.pagenum}-{self.subpage}.HTM"

        kwargs = {
            #"data": f"page={pagenum}-{subpage}&ch=1&mode=graph",
            #"headers": {"Referer": "https://teletext.hu/"}
        }

        rq=requests.post(url, **kwargs)
        self.soup = BeautifulSoup(rq.text, 'html.parser')
    
    @property
    def getPageGif(self):
        try:
            return f"https://teletext.hu/mtv1/{self.soup.img['src']}"
        except TypeError:
            return "https://teletext.hu/mtv1/images/100-01.gif"

    @property
    def prevPage(self):
        value = self.soup.find(id="prev")['value'].split("-")
        if value[0] == '':
            return None
        else:
            return value

    @property
    def prevSubpage(self):
        value = self.soup.find(id="prevSub")['value'].split("-")
        if value[0] == '':
            return None
        else:
            return value

    @property
    def nextPage(self):
        value = self.soup.find(id="next")['value'].split("-")
        if value[0] == '':
            return None
        else:
            return value

    @property
    def nextSubpage(self):
        value = self.soup.find(id="nextSub")['value'].split("-")
        if value[0] == '':
            return None
        else:
            return value
