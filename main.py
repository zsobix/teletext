# ummm

import requests
from bs4 import BeautifulSoup
import json


class hunTeletextReader:
    def __init__(self):
        self.pagenum = "100"
        self.subpage = "01"
        self.stationid = "mtva"
        self.getPage()
        self.colorbuttonsInit()

    def getPage(self):
        url = f"https://teletext.hu/mtv1/{self.pagenum}-{self.subpage}.HTM"

        kwargs = {
            #"data": f"page={pagenum}-{subpage}&ch=1&mode=graph",
            #"headers": {"Referer": "https://teletext.hu/"}
        }

        rq=requests.get(url, **kwargs)
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
    
    @property
    def subpages(self):
        if self.subpage == "01":
            kwargs = {
                "headers": {"Referer": "https://teletext.hu/", "Origin": "https://teletext.hu"},
                "data": {"page": self.pagenum,
                "ch": 1,
                "mode": "graph"}

            }
        else:
            kwargs = {
                "headers": {"Referer": "https://teletext.hu/", "Origin": "https://teletext.hu"},
                "data": {"page": f"{self.pagenum}-{self.subpage}",
                "ch": 1,
                "mode": "graph"}

            }
        soup = BeautifulSoup(requests.post("https://teletext.hu/main.php", **kwargs).text, 'html.parser')
        value = soup.find_all('td')[-1].string.split("/")[1]
        if value == '0' or value == 0:
            return None
        else:
            return int(value)
    
    def checkpageNum(self, pageNum):
        try:
            kwargs = {
            "headers": {"Referer": "https://teletext.hu/", "Origin": "https://teletext.hu"},
            "data": f"page={self.pagenum}&ch=1&mode=graph"

            }
            soup = BeautifulSoup(requests.post("https://teletext.hu/main.php", **kwargs).text, 'html.parser')
            value = int(soup.find_all('td')[-1].string.split("/")[1])
            return True
        except:
            return False

    def colorbuttonsInit(self):
        try:
            buttons = []
            for button in self.soup.find_all('area'):
                buttons.append(button.get('href').replace('.HTM', '').split('-'))
            self.colorbuttons = [buttons[0], buttons[1], buttons[2], buttons[3]]
            return self.colorbuttons
        except:
            return self.colorbuttons

class atTeletextReader:
    def __init__(self, *args, **kwargs):
        self.pagenum = "100"
        self.subpage = "01"
        #orf1, orf2, orfiii, or sportplus
        self.stationid = "orf1"
    
    def getPage(self):
        url = f"https://afeeds.orf.at/teletext/api/v2/mobile/channels/{self.stationid}/pages/{self.pagenum}"
        rq=requests.get(url)
        self.json = json.loads(rq.text)
    
    @property
    def getPageGif(self):
        #test rq
        url = f"https://appmeta.orf.at/teletext/{self.stationid}/{self.pagenum}_00{self.subpage}.png"
        return url
    
    @property
    def prevPage(self):
        value = self.json["previousPage"]
        if value == '0' or value == 0:
            return None
        else:
            return str(value)

    @property
    def nextPage(self):
        value = self.json["nextPage"]
        if value == '0' or value == 0:
            return None
        else:
            return str(value)

    @property
    def subpages(self):
        value = len(self.json["subpages"])
        if value == '0' or value == 0:
            return None
        else:
            return value
    
    def checkpageNum(self, pageNum):
        try:
            url = f"https://afeeds.orf.at/teletext/api/v2/mobile/channels/{self.stationid}/pages/{pageNum}"
            rq=requests.get(url)
            json.loads(rq.text)
            return True
        except:
            return False

class gerTeletextReader:
    def __init__(self, *args, **kwargs):
        self.pagenum = "100"
        self.subpage = "1"
        # zdf, zdfneo, zdfinfo, or 3sat
        self.stationid = "zdf"
    
    def getPage(self):
        if self.subpage == "1":
            url = f"https://teletext.zdf.de/teletext/{self.stationid}/seiten/klassisch/{self.pagenum}.html"
        else:
            url = f"https://teletext.zdf.de/teletext/{self.stationid}/seiten/klassisch/{self.pagenum}_{int(self.subpage)-1}.html"
        
        rq = requests.get(url)
        self.soup = BeautifulSoup(rq.text, 'html.parser')
    
    @property
    def prevPage(self):
        value = self.soup.body.get('prevpg')
        if value == '0':
            return None
        else:
            return value

    @property
    def nextPage(self):
        value = self.soup.body.get('nextpg')
        if value == '0':
            return None
        else:
            return value

    @property
    def subpages(self):
        value = self.soup.body.get('subpages')
        if value == '0' or value == 0:
            return None
        else:
            return int(value)
    
    def checkpageNum(self, pageNum):
        try:
            url = f"https://teletext.zdf.de/teletext/{self.stationid}/seiten/klassisch/{pageNum}.html"
            rq=requests.get(url)
            soup = BeautifulSoup(rq.text, 'html.parser')
            test = int(soup.body.get('subpages'))
            return True
        except:
            return False