# ummm

import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
from urllib.parse import parse_qs
import base64

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
            "data": {"page": pageNum,
                    "ch":1,
                    "mode":"graph"}

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
        self.getPage()
    
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
            jason = json.loads(rq.text)['subpages']
            return True
        except:
            return False

class gerTeletextReader:
    def __init__(self, *args, **kwargs):
        self.pagenum = "100"
        self.subpage = "1"
        # zdf, zdfneo, zdfinfo, or 3sat
        self.stationid = "zdf"
        self.getPage()
    
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
            return 1
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

class itTeletextReader:
    def __init__(self, *args, **kwargs):
        self.pagenum = "100"
        self.subpage = "1"
        self.stationid = "rai"
        self.region = "Nazionale"
        self.getPage()

    def getPage(self):
        url = f"https://www.servizitelevideo.rai.it/televideo/pub/popupTelevideo.jsp?p={self.pagenum}&s={int(self.subpage)}&r={self.region}&pagetocall=popupTelevideo.jsp"

        rq = requests.get(url)

        self.soup = BeautifulSoup(rq.text, 'html.parser')
    
    @property
    def getPageGif(self):
        try:
            url = self.soup.find(id="schermata").find_all("img")[0]['src']
            return f"https://www.servizitelevideo.rai.it{url}"
        except:
            return f"https://www.servizitelevideo.rai.it/televideo/pub/tt4web/{self.region}/16_9_page-100.png"
        

    @property
    def prevPage(self):
        url = self.soup.find_all("div", {"class": "txtBtn"})[0].find_all("a")[0]['href']
        parsed_url = urlparse(url)
        captured_value = parse_qs(parsed_url.query)
        value = captured_value['p'][0]

        while True:
            if int(value) < 100:
                return 100
            if self.checkpageNum(value):
                return value
            value = int(value)-1

    @property
    def nextPage(self):
        url = self.soup.find_all("div", {"class": "txtBtn"})[0].find_all("a")[4]['href']
        parsed_url = urlparse(url)
        captured_value = parse_qs(parsed_url.query)
        value = captured_value['p'][0]

        while True:
            if int(value) > 999:
                return None
            if self.checkpageNum(value):
                return value
            value = int(value)+1

    @property
    def subpages(self):
        try:
            value = self.soup.find_all("div", {"class": "txtNum"})[0].find_all("span")[0].string.strip(' / ')
        except:
            return 1
        if value == '0' or value == 0:
            return None
        else:
            return int(value)
    
    def checkpageNum(self, pageNum):
        url = f"https://www.servizitelevideo.rai.it/televideo/pub/tt4web/{self.region}/16_9_page-{pageNum}.png"
        rq = requests.get(url).status_code
        if rq == 404:
            return False
        else:
            return True
    
    @property
    def regions(self):
        try:
            value = self.soup.find(id="regioni").find_all("option")
            regions = []
            for region in value:
                if region.string != "Scegli la regione":
                    regions.append(region['value'])
            return regions
        except:
            regions = ["Nazionale"]
            return regions

class seTeletextReader:
    def __init__(self, *args, **kwargs):
        self.pagenum = "100"
        self.subpage = "01"
        self.stationid = "svt"
        self.getPage()
    
    def getPage(self):
        url = f"https://www.svt.se/text-tv/api/{self.pagenum}"

        rq = requests.get(url)

        self.json = json.loads(rq.text)
    
    @property
    def getPageGif(self):
        try:
            value = self.json["data"]["subPages"][int(self.subpage)-1]["gifAsBase64"]
            return base64.b64decode(value)
        except:
            pagenum = self.pagenum
            subpage = self.subpage
            self.pagenum = "100"
            self.subpage = "01"
            self.getPage()
            value = self.json["data"]["subPages"][int(self.subpage)-1]["gifAsBase64"]
            self.pagenum = pagenum
            self.subpage = subpage
            self.getPage()
            return base64.b64decode(value)
    
    @property
    def prevPage(self):
        value = self.json["data"]["prevPage"]
        if value == "":
            return None
        else:
            return value

    @property
    def nextPage(self):
        value = self.json["data"]["nextPage"]
        if value == "":
            return None
        else:
            return value

    @property
    def subpages(self):
        value = len(self.json["data"]["subPages"])
        return value
    
    def checkpageNum(self, pageNum):
        try:
            url = f"https://www.svt.se/text-tv/api/{pageNum}"

            rq = requests.get(url)

            self.json = json.loads(rq.text)

            value = self.json["data"]["subPages"][int(self.subpage)-1]["gifAsBase64"]
            return True
        except:
            return False

class chTeletextReader:
    def __init__(self, *args, **kwargs):
        self.pagenum = "100"
        self.subpage = "01"
        self.stationid = "SRF1"
        self.getPage()
    
    def getPage(self):
        url = f"https://api.teletext.ch/channels/{self.stationid}/pages/{self.pagenum}"

        rq = requests.get(url)

        self.json = json.loads(rq.text)
    
    @property
    def getPageGif(self):
        try:
            value = f"https://api.teletext.ch/online/pics/large/{self.stationid}_{self.pagenum}-{int(self.subpage)-1}.gif"
            return value
        except:
            return f"https://api.teletext.ch/online/pics/large/{self.stationid}_100-0.gif"
    
    @property
    def prevPage(self):
        try:
            value = self.json["previousPage"]
            return value
        except:
            return None

    @property
    def nextPage(self):
        try:
            value = self.json["nextPage"]
            return value
        except:
            return None

    @property
    def subpages(self):
        value = len(self.json["subpages"])
        return value
    
    def checkpageNum(self, pageNum):
        try:
            url = f"https://api.teletext.ch/channels/{self.stationid}/pages/{pageNum}"

            rq = requests.get(url).json()

            value = rq["subpages"]
            return True
        except:
            return False

class czTeletextReader:
    def __init__(self, *args, **kwargs):
        self.pagenum = "100"
        self.subpage = "01"
        self.stationid = "ČT"
        self.getPage()
    
    def getPage(self):
        url = f"https://api-teletext.ceskatelevize.cz/pages"

        rq = requests.get(url)

        self.json = json.loads(rq.text)
    
    @property
    def subpageletter(self):
        value = self.json["data"][str(self.pagenum)]["subpages"][int(self.subpage)-1]
        return value

    @property
    def getPageGif(self):
        try:
            if self.subpages > 1:
                value = f"https://api-teletext.ceskatelevize.cz/pages/{self.pagenum}{self.subpageletter}/image.webp"
            else:
                value = f"https://api-teletext.ceskatelevize.cz/pages/{self.pagenum}/image.webp"
            return value
        except:
            return f"https://api-teletext.ceskatelevize.cz/pages/100A/image.webp"
    
    @property
    def prevPage(self):
        value = int(self.pagenum)-1

        while True:
            if int(value) < 100:
                return 100
            if self.checkpageNum(value):
                return value
            value = int(value)-1

    @property
    def nextPage(self):
        value = int(self.pagenum)+1

        while True:
            if int(value) > 999:
                return None
            if self.checkpageNum(value):
                return value
            value = int(value)+1

    @property
    def subpages(self):
        try:
            value = len(self.json["data"][str(self.pagenum)]["subpages"])
            if value < 1:
                return 1
            return value
        except:
            return 1
    
    def checkpageNum(self, pageNum):
        try:
            value = self.json["data"][str(pageNum)]["subpages"]
            return True
        except:
            return False

class fiTeletextReader:
    def __init__(self, *args, **kwargs):
        self.pagenum = "100"
        self.subpage = "01"
        self.stationid = "yle"
        self.getPage()
        
    def getPage(self):
        url = f"https://yle.fi/aihe/tekstitv?P={self.pagenum}#{int(self.subpage)}"

        rq = requests.get(url)

        self.soup = BeautifulSoup(rq.text, 'html.parser')

    @property
    def getPageGif(self):
        try:
            url = f"https://yle.fi/aihe/yle-ttv/json?P={self.pagenum}_00{self.subpage}"

            rq = requests.get(url)

            son = json.loads(rq.text)
            value = son["data"][0]["content"]["image"]
            value = BeautifulSoup(value, 'html.parser').img["src"].replace("data:image/png;base64,", "")
            return base64.b64decode(value)
        except:
            url = f"https://yle.fi/aihe/yle-ttv/json?P=100_0001"

            rq = requests.get(url)

            son = json.loads(rq.text)
            value = son["data"][0]["content"]["image"]
            value = BeautifulSoup(value, 'html.parser').img["src"].replace("data:image/png;base64,", "")
            return base64.b64decode(value)
    
    @property
    def prevPage(self):
        try:
            value = self.soup.find_all("div", {"class": "yle-ttv__pagination"})[0].find_all('a', {"class": "yle-ttv__button"})[0]["href"].replace("?P=", "")
            return value
        except:
            return None

    @property
    def nextPage(self):
        try:
            value = self.soup.find_all("div", {"class": "yle-ttv__pagination"})[0].find_all('a', {"class": "yle-ttv__button"})[-1]["href"].replace("?P=", "")
            return value
        except:
            return None

    @property
    def subpages(self):
        try:
            url = f"https://yle.fi/aihe/yle-ttv/json?P={self.pagenum}_0001"

            rq = requests.get(url)

            son = json.loads(rq.text)
            value = son["data"][0]["info"]["page"]["subpages"]
            return int(value)
        except:
            return 1
    
    def checkpageNum(self, pageNum):
        try:
            url = f"https://yle.fi/aihe/yle-ttv/json?P={pageNum}_0001"

            rq = requests.get(url)

            son = json.loads(rq.text)
            value = son["data"][0]["page"]["page"]
            return True
        except:
            return False

class otherTeletextReader:
    def __init__(self, *args, **kwargs):
        self.pagenum = "100"
        self.subpage = "01"
        self.stationid = "s1de"
        self.getPage()
        
    def getPage(self):
        url = f"https://som-teletextviewer.sim-technik.de/api/page?ttx_select={self.stationid}&pagnr={self.pagenum}_{self.subpage}"

        rq = requests.get(url)

        self.json = json.loads(rq.text)

    @property
    def getPageGif(self):
        try:
            url = f"https://som-teletextviewer.sim-technik.de/api/page/png?ttx_select={self.stationid}&pagnr={self.pagenum}_{self.subpage}"

            rq = requests.get(url).status_code
            if rq == 404:
                raise Exception
            return url
        except:
            return "https://som-teletextviewer.sim-technik.de/api/page/png?ttx_select=s1de&pagnr=100_01"
    
    @property
    def prevPage(self):
        value = int(self.pagenum)-1

        while True:
            if int(value) < 100:
                return 100
            if self.checkpageNum(value):
                return value
            value = int(value)-1

    @property
    def nextPage(self):
        value = int(self.pagenum)+1

        while True:
            if int(value) > 900:
                return None
            if self.checkpageNum(value):
                return value
            value = int(value)+1

    @property
    def subpages(self):
        value = int(self.subpage)

        while True:
            if int(value) > 50:
                return 1
            if not self.checksubpageNum(value):
                return int(value)-1
            value = int(value)+1
    
    def checkpageNum(self, pageNum):
        try:
            url = f"https://som-teletextviewer.sim-technik.de/api/page?ttx_select={self.stationid}&pagnr={pageNum}_01"

            rq = requests.get(url)

            son = json.loads(rq.text)
            if son["pagnr"] != f"{pageNum}_01":
                raise Exception
            else:
                return True
        except:
            return False
    
    def checksubpageNum(self, subpageNum):
        try:
            url = f"https://som-teletextviewer.sim-technik.de/api/page?ttx_select={self.stationid}&pagnr={self.pagenum}_{subpageNum:02d}"

            rq = requests.get(url)

            son = json.loads(rq.text)
            return son["pagnr"]==f"{self.pagenum}_{subpageNum:02d}"
        except:
            return False

    @property
    def stations(self):
        url = "https://som-teletextviewer.sim-technik.de/api/stations"

        rq = requests.get(url)

        son = json.loads(rq.text)

        stations = []
        for station in son["stations"]:
            if station["label"].startswith("AT-"):
                stations.append(f"Austria {station["label"].replace("AT-", "")} ({station["key"]})")
            elif station["label"].startswith("CH-"):
                stations.append(f"Switzerland {station["label"].replace("CH-", "")} ({station["key"]})")
            else:
                stations.append(f"{station["label"]} ({station["key"]})")
        
        return stations

    @property
    def stationsid(self):
        url = "https://som-teletextviewer.sim-technik.de/api/stations"

        rq = requests.get(url)

        son = json.loads(rq.text)

        stations = []
        for station in son["stations"]:
            stations.append(station["key"])
        
        return stations

class dkTeletextReader:
    def __init__(self, *args, **kwargs):
        self.pagenum = "100"
        self.subpage = "01"
        self.stationid = "dr"
        self.getPage()
        
    def getPage(self):
        url = f"https://www.dr.dk/cgi-bin/fttv1.exe/{self.pagenum}/{int(self.subpage)}"

        rq = requests.get(url)

        self.soup = BeautifulSoup(rq.text, 'html.parser')

    @property
    def getPageGif(self):
        try:
            value = self.soup.find_all('a')[0].find_all('img')[0]["src"]
            return f"https://www.dr.dk{value}"
        except:
            pagenum = self.pagenum
            subpage = self.subpage
            self.pagenum = "100"
            self.subpage = "01"
            self.getPage()
            value = self.soup.find_all('a')[0].find_all('img')[0]["src"]
            self.pagenum = pagenum
            self.subpage = subpage
            self.getPage()
            return f"https://www.dr.dk{value}"
    
    @property
    def prevPage(self):
        value = int(self.pagenum)-1

        while True:
            if int(value) < 100:
                return 100
            if self.checkpageNum(value):
                return value
            value = int(value)-1

    @property
    def nextPage(self):
        value = int(self.pagenum)+1

        while True:
            if int(value) > 900:
                return None
            if self.checkpageNum(value):
                return value
            value = int(value)+1

    @property
    def subpages(self):
        # return 1
        
        value = int(self.subpage)

        while True:
            if int(value) > 50:
                return 1
            if not self.checksubpageNum(value):
                return int(value)-1
            value = int(value)+1
    
    def checkpageNum(self, pageNum):
        try:
            url = f"https://www.dr.dk/cgi-bin/fttv1.exe/{pageNum}"

            rq = requests.get(url)

            self.soup = BeautifulSoup(rq.text, 'html.parser')
            value = self.soup.find_all('a')[0].find_all('img')[0]["src"]
            return True
        except:
            return False
    
    def checksubpageNum(self, subpageNum):
        try:
            url = f"https://www.dr.dk/cgi-bin/fttv1.exe/{self.pagenum}/{subpageNum}"

            rq = requests.get(url)

            self.soup = BeautifulSoup(rq.text, 'html.parser')

            value = self.soup.find_all('a')[0].find_all('img')[0]["src"]
            return True
        except:
            return False
    
class other2TeletextReader:
    def __init__(self, *args, **kwargs):
        self.pagenum = "100"
        self.subpage = "01"
        self.stationid = "br-alpha" #or DE_arte
        self.getPage()
        
    def getPage(self):
        url = f"https://zapi.zattoo.com/teletext/{self.stationid}/hd/{self.pagenum}/1.html"

        rq = requests.get(url)

        self.soup = BeautifulSoup(rq.text, 'html.parser')

    @property
    def getPageGif(self):
        try:
            value = self.soup.find_all('img')[0]["src"].replace('data:image/png;base64,', '')
            return base64.b64decode(value)
        except:
            pagenum = self.pagenum
            self.pagenum = "100"
            self.getPage()
            value = self.soup.find_all('img')[0]["src"].replace('data:image/png;base64,', '')
            self.pagenum = pagenum
            self.getPage()
            return base64.b64decode(value)
    
    @property
    def prevPage(self):
        value = int(self.pagenum)-1

        while True:
            if int(value) < 100:
                return 100
            if self.checkpageNum(value):
                return value
            value = int(value)-1

    @property
    def nextPage(self):
        value = int(self.pagenum)+1

        while True:
            if int(value) > 900:
                return None
            if self.checkpageNum(value):
                return value
            value = int(value)+1

    @property
    def subpages(self):
        return 1
    
    def checkpageNum(self, pageNum):
        try:
            url = f"https://zapi.zattoo.com/teletext/{self.stationid}/hd/{self.pagenum}/1.html"

            rq = requests.get(url)

            self.soup = BeautifulSoup(rq.text, 'html.parser')
            value = self.soup.find_all('img')[0]["src"].replace('data:image/png;base64,', '')
            return True
        except:
            return False

class kikaTeletextReader:
    def __init__(self, *args, **kwargs):
        self.pagenum = "100"
        self.subpage = "01"
        self.stationid = "kika"
        self.getPage()
        
    def getPage(self):
        url = f"https://www.kika.de/kikatextpages/{self.pagenum}_00{int(self.subpage):02d}.htm"

        rq = requests.get(url)

        self.soup = BeautifulSoup(rq.text, 'html.parser')

    @property
    def getPageGif(self):
        try:
            value = f"https://www.kika.de/kikatextpages/{self.pagenum}_00{int(self.subpage):02d}.png"
            return value
        except:
            value = "https://www.kika.de/kikatextpages/100_0001.png"
            return value
    
    @property
    def prevPage(self):
        value = json.loads(self.soup.find(id="kikatext-page-data")['data-kikatext-page'])
        prev = value["PREVPGNUM"]
        if prev == "":
            return None
        else:
            return int(prev)
    @property
    def nextPage(self):
        value = json.loads(self.soup.find(id="kikatext-page-data")['data-kikatext-page'])
        nextpg = value["NEXTPGNUM"]
        if nextpg == "":
            return None
        else:
            return int(nextpg)

    @property
    def subpages(self):
        try:
            value = len(self.soup.find_all("div", {"class": "SUBPGLIST"})[0].find_all('a'))+1
            return value
        except:
            return 1
    
    def checkpageNum(self, pageNum):
        try:
            url = f"https://www.kika.de/kikatextpages/{pageNum}_0001.png"

            rq = requests.get(url).status_code

            if rq == 302 or rq == 404:
                return False
            else:
                return True
        except:
            return False

class esTeletextReader:
    def __init__(self, *args, **kwargs):
        self.pagenum = "100"
        self.subpage = "01"
        self.stationid = "tve"
        self.getPage()
        
    def getPage(self):
        url = f"https://www.rtve.es/tve/teletexto/100/{self.pagenum}_00{int(self.subpage):02d}.htm"

        rq = requests.get(url)

        self.soup = BeautifulSoup(rq.text, 'html.parser')

    @property
    def getPageGif(self):
        try:
            value = f"https://img.rtve.es/tve/teletexto/100/{self.pagenum}_00{int(self.subpage):02d}.png"
            return value
        except:
            value = "https://img.rtve.es/tve/teletexto/100/100_0001.png"
            return value
    
    @property
    def prevPage(self):
        value = int(self.pagenum)-1

        while True:
            if int(value) < 100:
                return 100
            if self.checkpageNum(value):
                return value
            value = int(value)-1

    @property
    def nextPage(self):
        value = int(self.pagenum)+1

        while True:
            if int(value) > 900:
                return None
            if self.checkpageNum(value):
                return value
            value = int(value)+1

    @property
    def subpages(self):
        try:
            if int(self.subpage) > 1:
                value = len(self.soup.find_all("span", {"class": "LB"})[0].find_all('a'))-1
            else:
                value = len(self.soup.find_all("span", {"class": "LB"})[0].find_all('a'))
                if value == 0:
                    return 1
            return value
        except:
            return 1
    
    def checkpageNum(self, pageNum):
        try:
            url = f"https://img.rtve.es/tve/teletexto/100/{pageNum}_0001.png"

            rq = requests.get(url).status_code

            if rq == 302 or rq == 404:
                return False
            else:
                return True
        except:
            return False

class plTeletextReader:
    def __init__(self, *args, **kwargs):
        self.pagenum = "100"
        self.subpage = "01"
        self.stationid = "TG1"
        self.getPage()
    
    def getPage(self):
        url = f"https://www.telegazeta.pl/sync/ncexp/{self.stationid}/status.json"

        rq = requests.get(url)

        self.json = json.loads(rq.text)
    
    @property
    def getPageGif(self):
        try:
            value = f"https://www.telegazeta.pl/sync/ncexp/{self.stationid}/100/{self.pagenum}_00{int(self.subpage):02d}.png"
            return value
        except:
            value = f"https://www.telegazeta.pl/sync/ncexp/{self.stationid}/100/100_0001.png"
    
    @property
    def prevPage(self):
        value = self.json["teletext"]["pages"]
        prev = int(self.pagenum)-1
        while True:
            if prev < 100:
                return None
            try:
                if int(value[f"p{prev}"]["page"]["subpagecount"]) != 0:
                    return prev
            except:
                return None
            prev = int(prev)-1
    
    @property
    def nextPage(self):
        value = self.json["teletext"]["pages"]
        nextpg = int(self.pagenum)+1
        while True:
            if nextpg > 900:
                return None
            try:
                if int(value[f"p{nextpg}"]["page"]["subpagecount"]) != 0:
                    return nextpg
            except:
                return None
            nextpg = int(nextpg)+1
    
    @property
    def subpages(self):
        value = int(self.json["teletext"]["pages"][f"p{self.pagenum}"]["page"]["subpagecount"])
        return value
    
    def checkpageNum(self, pageNum):
        try:
            url = f"https://www.telegazeta.pl/sync/ncexp/{self.stationid}/100/{pageNum}_0001.png"

            rq = requests.get(url).status_code

            if rq == 302 or rq == 404:
                return False
            else:
                return True
        except:
            return False

class baTeletextReader:
    def __init__(self, *args, **kwargs):
        self.pagenum = "100"
        self.subpage = "01"
        self.stationid = "bhrt"
        self.getPage()

    def getPage(self):
        url = f"https://teletext.bhrt.ba/100/{self.pagenum}_00{int(self.subpage):02d}.htm"

        rq = requests.get(url)

        self.soup = BeautifulSoup(rq.text, 'html.parser')

    @property
    def getPageGif(self):
        try:
            value = f"https://teletext.bhrt.ba/100/{self.pagenum}_00{int(self.subpage):02d}.png"
            return value
        except:
            value = "https://teletext.bhrt.ba/100/100_0001.png"
            return value

    @property
    def prevPage(self):
        value = int(self.pagenum)-1

        while True:
            if int(value) < 100:
                return 100
            if self.checkpageNum(value):
                return value
            value = int(value)-1

    @property
    def nextPage(self):
        value = int(self.pagenum)+1

        while True:
            if int(value) > 900:
                return None
            if self.checkpageNum(value):
                return value
            value = int(value)+1

    @property
    def subpages(self):
        page = self.soup.find_all('p', {"class": "LB"})[0].find_all('a')

        subpages = 1
        for a in page:
            try:
                int(a.string)
                subpages = int(subpages)+1
            except:
                pass
        return subpages

    def checkpageNum(self, pageNum):
        try:
            url = f"https://teletext.bhrt.ba/100/{pageNum}_0001.png"

            rq = requests.get(url).status_code

            if rq == 404 or rq == 302:
                return False
            else:
                return True
        except:
            return False

class nlTeletextReader:
    def __init__(self, *args, **kwargs):
        self.pagenum = "100"
        self.subpage = "01"
        self.stationid = "nos"
        self.getPage()

    def getPage(self):
        url = f"https://teletekst-data.nos.nl/json/{self.pagenum}-{int(self.subpage)}"

        rq = requests.get(url)

        self.json = json.loads(rq.text)

    def writetempHTML(self):
        pre = """
        <html><head><style>html{line-height:1.15;-webkit-text-size-adjust:100%;}/*!sc*/
        body{margin:0;}/*!sc*/
        main{display:block;}/*!sc*/
        h1{font-size:2em;margin:0.67em 0;}/*!sc*/
        hr{box-sizing:content-box;height:0;overflow:visible;}/*!sc*/
        pre{font-family:monospace,monospace;font-size:1em;}/*!sc*/
        a{background-color:transparent;}/*!sc*/
        abbr[title]{border-bottom:none;text-decoration:underline;text-decoration:underline dotted;}/*!sc*/
        b,strong{font-weight:bolder;}/*!sc*/
        code,kbd,samp{font-family:monospace,monospace;font-size:1em;}/*!sc*/
        small{font-size:80%;}/*!sc*/
        sub,sup{font-size:75%;line-height:0;position:relative;vertical-align:baseline;}/*!sc*/
        sub{bottom:-0.25em;}/*!sc*/
        sup{top:-0.5em;}/*!sc*/
        img{border-style:none;}/*!sc*/
        button,input,optgroup,select,textarea{font-family:inherit;font-size:100%;line-height:1.15;margin:0;}/*!sc*/
        button,input{overflow:visible;}/*!sc*/
        button,select{text-transform:none;}/*!sc*/
        button,[type="button"],[type="reset"],[type="submit"]{-webkit-appearance:button;}/*!sc*/
        button::-moz-focus-inner,[type="button"]::-moz-focus-inner,[type="reset"]::-moz-focus-inner,[type="submit"]::-moz-focus-inner{border-style:none;padding:0;}/*!sc*/
        button:-moz-focusring,[type="button"]:-moz-focusring,[type="reset"]:-moz-focusring,[type="submit"]:-moz-focusring{outline:1px dotted ButtonText;}/*!sc*/
        fieldset{padding:0.35em 0.75em 0.625em;}/*!sc*/
        legend{box-sizing:border-box;color:inherit;display:table;max-width:100%;padding:0;white-space:normal;}/*!sc*/
        progress{vertical-align:baseline;}/*!sc*/
        textarea{overflow:auto;}/*!sc*/
        [type="checkbox"],[type="radio"]{box-sizing:border-box;padding:0;}/*!sc*/
        [type="number"]::-webkit-inner-spin-button,[type="number"]::-webkit-outer-spin-button{height:auto;}/*!sc*/
        [type="search"]{-webkit-appearance:textfield;outline-offset:-2px;}/*!sc*/
        [type="search"]::-webkit-search-decoration{-webkit-appearance:none;}/*!sc*/
        ::-webkit-file-upload-button{-webkit-appearance:button;font:inherit;}/*!sc*/
        details{display:block;}/*!sc*/
        summary{display:list-item;}/*!sc*/
        template{display:none;}/*!sc*/
        [hidden]{display:none;}/*!sc*/
        data-styled.g1[id="sc-global-ecVvVt"]{content:"sc-global-ecVvVt1,"}/*!sc*/
        .cdjoiX{font:bold 1rem/1.125 'Effra-Bold',Helvetica,Arial,sans-serif;padding:0.5rem;background:#ffffff;display:flex;justify-content:center;align-items:center;border-radius:0.25rem;transition:background-color 150ms ease-in-out,color 150ms ease-in-out;outline-offset:0.125rem;}/*!sc*/
        @media (min-width: 47.5rem){.cdjoiX{font:bold 1.125rem/1.11 'Effra-Bold',Helvetica,Arial,sans-serif;padding:0.75rem;}}/*!sc*/
        .cdjoiX >{transform:translateY(1px);}/*!sc*/
        data-styled.g2[id="MainNavItem-style__FocusBox-sc-a8dd054f-0"]{content:"cdjoiX,"}/*!sc*/
        .kLaGqK{text-decoration:unset;appearance:none;border:none;background:none;cursor:pointer;outline:none;position:relative;color:#202020;padding:0.25rem;display:flex;align-items:center;justify-content:center;height:100%;width:fit-content;white-space:nowrap;}/*!sc*/
        @media (min-width: 47.5rem){.kLaGqK{padding:0.5rem;}}/*!sc*/
        .kLaGqK::before{content:'';display:none;height:0.1875rem;transition:background-color 150ms ease-in-out;background:transparent;position:absolute;bottom:-0.0625rem;border-top-right-radius:0.1875rem;border-top-left-radius:0.1875rem;width:calc(100% - (2 * (0.5rem + 0.25rem)));}/*!sc*/
        @media (min-width: 47.5rem){.kLaGqK::before{width:calc(100% - (2 * (0.75rem + 0.5rem)));}}/*!sc*/
        .kLaGqK:focus-visible .MainNavItem-style__FocusBox-sc-a8dd054f-0{background:#f3f3f0;outline:0.125rem solid #e61e14;}/*!sc*/
        .kLaGqK:active .MainNavItem-style__FocusBox-sc-a8dd054f-0{background:#f3f3f0;outline:0.125rem solid #dddddd;}/*!sc*/
        .kLaGqK:hover{color:#202020;}/*!sc*/
        .kLaGqK:hover .MainNavItem-style__FocusBox-sc-a8dd054f-0{background:#f3f3f0;}/*!sc*/
        .kLaGqK[href*="teletekst"]{color:#888888;}/*!sc*/
        .kLaGqK[href*="teletekst"]:hover{color:#888888;}/*!sc*/
        .kLaGqK[href*="teletekst"]::before{background:transparent;}/*!sc*/
        data-styled.g3[id="MainNavItem-style__StyledLink-sc-a8dd054f-1"]{content:"kLaGqK,"}/*!sc*/
        .etgMaW{text-decoration:unset;appearance:none;border:none;background:none;cursor:pointer;outline:none;position:relative;color:#202020;padding:0.25rem;display:flex;align-items:center;justify-content:center;height:100%;width:fit-content;white-space:nowrap;}/*!sc*/
        @media (min-width: 47.5rem){.etgMaW{padding:0.5rem;}}/*!sc*/
        .etgMaW::before{content:'';display:none;height:0.1875rem;transition:background-color 150ms ease-in-out;background:transparent;position:absolute;bottom:-0.0625rem;border-top-right-radius:0.1875rem;border-top-left-radius:0.1875rem;width:calc(100% - (2 * (0.5rem + 0.25rem)));}/*!sc*/
        @media (min-width: 47.5rem){.etgMaW::before{width:calc(100% - (2 * (0.75rem + 0.5rem)));}}/*!sc*/
        .etgMaW:focus-visible .MainNavItem-style__FocusBox-sc-a8dd054f-0{background:#f3f3f0;outline:0.125rem solid #e61e14;}/*!sc*/
        .etgMaW:active .MainNavItem-style__FocusBox-sc-a8dd054f-0{background:#f3f3f0;outline:0.125rem solid #dddddd;}/*!sc*/
        .etgMaW:hover{color:#202020;}/*!sc*/
        .etgMaW:hover .MainNavItem-style__FocusBox-sc-a8dd054f-0{background:#f3f3f0;}/*!sc*/
        data-styled.g4[id="MainNavItem-style__StyledButton-sc-a8dd054f-2"]{content:"etgMaW,"}/*!sc*/
        .gAYkUZ{display:flex;justify-content:center;align-items:center;border-radius:0.25rem;outline-offset:0.25rem;transition:transform 150ms ease-in-out;}/*!sc*/
        data-styled.g5[id="MainNavItemLogo-style__FocusBox-sc-d4709398-0"]{content:"gAYkUZ,"}/*!sc*/
        .jCltNe{position:relative;padding:0.75rem;display:flex;align-items:center;justify-content:center;height:100%;width:fit-content;text-decoration:unset;border:none;cursor:pointer;transform:translateY(1px);}/*!sc*/
        @media (min-width: 47.5rem){.jCltNe{padding:1.25rem;}}/*!sc*/
        .jCltNe:focus-visible{outline:none;}/*!sc*/
        .jCltNe:focus-visible .MainNavItemLogo-style__FocusBox-sc-d4709398-0{outline:0.125rem solid #e61e14;}/*!sc*/
        .jCltNe:active .MainNavItemLogo-style__FocusBox-sc-d4709398-0{outline:0.125rem solid #dddddd;transform:scale(1.04);}/*!sc*/
        .jCltNe:hover .MainNavItemLogo-style__FocusBox-sc-d4709398-0{transform:scale(1.04);}/*!sc*/
        data-styled.g6[id="MainNavItemLogo-style__StyledLink-sc-d4709398-1"]{content:"jCltNe,"}/*!sc*/
        .dDYWoO{display:flex;justify-content:center;border-bottom:0.0625rem solid #dddddd;width:100%;background:#ffffff;z-index:var(--layer-navbar);position:relative;pointer-events:auto;}/*!sc*/
        data-styled.g7[id="MainNavBar-style__Bar-sc-1b875ba6-0"]{content:"dDYWoO,"}/*!sc*/
        .epCtBa{list-style:none;display:grid;grid-template-columns:auto minmax(auto, 75rem) auto;width:100%;height:3.5rem;}/*!sc*/
        @media (min-width: 47.5rem){.epCtBa{height:4.5rem;}}/*!sc*/
        @media (min-width: 90rem){.epCtBa{padding-left:1.5rem;padding-right:1.25rem;}}/*!sc*/
        .epCtBa >li:last-child{margin-left:auto;}/*!sc*/
        data-styled.g8[id="MainNavBar-style__List-sc-1b875ba6-1"]{content:"epCtBa,"}/*!sc*/
        .eNozMw{width:100%;display:flex;flex-wrap:nowrap;justify-content:space-between;height:3.5rem;list-style:none;}/*!sc*/
        @media (min-width: 47.5rem){.eNozMw{height:4.5rem;}}/*!sc*/
        .eNozMw ul,.eNozMw li{height:100%;}/*!sc*/
        data-styled.g9[id="MainNavBar-style__MainMenuItems-sc-1b875ba6-2"]{content:"eNozMw,"}/*!sc*/
        .eQtcgS{display:flex;list-style:none;}/*!sc*/
        @media (max-width: 21.25rem){.eQtcgS li:last-child{display:none;}}/*!sc*/
        @media (max-width: 17.625rem){.eQtcgS li:nth-last-child(2){display:none;}}/*!sc*/
        @media (max-width: 13.5625rem){.eQtcgS li:nth-last-child(3){display:none;}}/*!sc*/
        data-styled.g10[id="MainNavBar-style__NavigationItems-sc-1b875ba6-3"]{content:"eQtcgS,"}/*!sc*/
        .jyBsZM{display:flex;list-style:none;}/*!sc*/
        @media (max-width: 56.75rem){.jyBsZM li:last-child{display:none;}}/*!sc*/
        @media (max-width: 63.9375rem){.jyBsZM li:nth-last-child(2){display:none;}}/*!sc*/
        @media (max-width: 49.125rem){.jyBsZM li:nth-last-child(3){display:none;}}/*!sc*/
        @media (max-width: 24.1875rem){.jyBsZM li:nth-last-child(4){display:none;}}/*!sc*/
        data-styled.g11[id="MainNavBar-style__InteractionItems-sc-1b875ba6-4"]{content:"jyBsZM,"}/*!sc*/
        .fA-dKki{background:#ffffff;}/*!sc*/
        data-styled.g12[id="MainNavBar-style__StyledListItem-sc-1b875ba6-5"]{content:"fA-dKki,"}/*!sc*/
        .jaNChX{height:0.875rem;color:#949494;}/*!sc*/
        @media (min-width: 47.5rem){.jaNChX{height:1.5rem;}}/*!sc*/
        data-styled.g13[id="MainNavBar-style__StyledNosLogo-sc-1b875ba6-6"]{content:"jaNChX,"}/*!sc*/
        .debZPo{height:1.5rem;padding-left:0.25rem;}/*!sc*/
        data-styled.g14[id="MainNavBar-style__StyledNpoStartLogo-sc-1b875ba6-7"]{content:"debZPo,"}/*!sc*/
        .dIgtLP{height:1rem;}/*!sc*/
        data-styled.g15[id="MainNavBar-style__StyledTeletekstLogo-sc-1b875ba6-8"]{content:"dIgtLP,"}/*!sc*/
        .fmoENB{padding-left:1rem;}/*!sc*/
        data-styled.g16[id="MainNavBar-style__MainNavItemNosLogo-sc-1b875ba6-9"]{content:"fmoENB,"}/*!sc*/
        .bifiot{padding-right:0.5rem;}/*!sc*/
        @media (min-width: 47.5rem){.bifiot{padding-left:0.25rem;}}/*!sc*/
        data-styled.g17[id="MainNavBar-style__MainNavItemMenu-sc-1b875ba6-10"]{content:"bifiot,"}/*!sc*/
        .bwxyaU{overflow-wrap:anywhere;margin:0;padding:0;font-weight:700;font-size:2.125rem;line-height:1.2;}/*!sc*/
        data-styled.g29[id="Heading-style__Heading-sc-42f31abe-0"]{content:"bwxyaU,"}/*!sc*/
        .bSdYpN{display:flex;flex-flow:row nowrap;align-items:center;padding:1rem 1rem 1rem 0;}/*!sc*/
        .bSdYpN >svg:first-child{flex:0 0 auto;width:3rem;}/*!sc*/
        data-styled.g95[id="ExternalItem-style__ExternalItemContainer-sc-8eb7fb85-0"]{content:"bSdYpN,"}/*!sc*/
        .ghhIMc{flex:1 1 auto;margin-left:1rem;}/*!sc*/
        data-styled.g96[id="ExternalItem-style__ExternalItemContent-sc-8eb7fb85-1"]{content:"ghhIMc,"}/*!sc*/
        .KDfEy{display:flex;flex:0 0 3rem;justify-content:center;align-items:center;width:3rem;height:3rem;border-radius:50%;background-color:#ffffff;}/*!sc*/
        .KDfEy svg{color:#e61e14;}/*!sc*/
        data-styled.g97[id="ExternalItem-style__ExternalItemIcon-sc-8eb7fb85-2"]{content:"KDfEy,"}/*!sc*/
        .kReFRv{display:block;margin-bottom:0.25rem;color:#202020;transition:all 150ms ease-in-out;font:500 0.875rem/1.29 'Helvetica Neue',Helvetica,Arial,sans-serif;}/*!sc*/
        @media (min-width: 47.5rem){.kReFRv{font:500 1rem/1.375 'Helvetica Neue',Helvetica,Arial,sans-serif;}}/*!sc*/
        data-styled.g98[id="ExternalItem-style__ExternalItemTitle-sc-8eb7fb85-3"]{content:"kReFRv,"}/*!sc*/
        .bfuivs{display:block;color:#666666;font:500 0.75rem/1.1 'Helvetica Neue',Helvetica,Arial,sans-serif;}/*!sc*/
        @media (min-width: 47.5rem){.bfuivs{font:500 0.875rem/1.29 'Helvetica Neue',Helvetica,Arial,sans-serif;}}/*!sc*/
        data-styled.g99[id="ExternalItem-style__ExternalItemSubtitle-sc-8eb7fb85-4"]{content:"bfuivs,"}/*!sc*/
        .gNyNox{overflow-wrap:anywhere;word-break:normal;display:block;color:#202020;text-decoration:none;font-weight:500;line-height:1.14;transition:color 150ms ease-in-out;}/*!sc*/
        @media (hover: hover) and (pointer: fine),only screen and (-ms-high-contrast:active),(-ms-high-contrast:none){.gNyNox:hover{color:#e61e14;}.gNyNox:hover .ExternalItem-style__ExternalItemTitle-sc-8eb7fb85-3{text-decoration:underline;color:#e61e14;}.gNyNox:hover .ExternalItem-style__StyledArrow-sc-8eb7fb85-5{transform:translate(0.1em, -0.1em);}}/*!sc*/
        .gNyNox:focus-visible{outline:0.125rem solid #e61e14;outline-offset:0.125rem;border-radius:0.125rem;}/*!sc*/
        .gNyNox:active{color:#e61e14;transition:none;}/*!sc*/
        .gNyNox:active .ExternalItem-style__ExternalItemTitle-sc-8eb7fb85-3{color:inherit;}/*!sc*/
        data-styled.g101[id="ExternalLink-style__Anchor-sc-18fe297-0"]{content:"gNyNox,"}/*!sc*/
        .gtTESY{margin-top:2.5rem;border-top:0.0625rem solid #eeeeee;border-bottom:0.0625rem solid #eeeeee;background-color:#ffffff;color:#666666;}/*!sc*/
        @media print{.gtTESY{display:none;}}/*!sc*/
        data-styled.g102[id="Footer-style__StyledFooter-sc-b6185a4a-0"]{content:"gtTESY,"}/*!sc*/
        .csTCTF{display:flex;flex-direction:column;}/*!sc*/
        @media (min-width: 47.5rem){.csTCTF{flex-direction:row;max-width:75rem;margin:0 auto;padding:2rem 1rem 0;}}/*!sc*/
        data-styled.g103[id="Footer-style__FooterLinks-sc-b6185a4a-1"]{content:"csTCTF,"}/*!sc*/
        .ftSjfn{overflow-wrap:anywhere;margin:1rem 0;color:#e61e14;font:bold 1rem/1.125 'Effra-Bold',Helvetica,Arial,sans-serif;}/*!sc*/
        @media (min-width: 47.5rem){.ftSjfn{font:bold 1.125rem/1.11 'Effra-Bold',Helvetica,Arial,sans-serif;}}/*!sc*/
        data-styled.g104[id="Footer-style__Title-sc-b6185a4a-2"]{content:"ftSjfn,"}/*!sc*/
        .ifaeOo{margin:1rem 0 0;padding:0;list-style:none;}/*!sc*/
        data-styled.g105[id="Footer-style__StyledList-sc-b6185a4a-3"]{content:"ifaeOo,"}/*!sc*/
        .gBHipf{display:inline-block;margin-bottom:1rem;color:#666666;text-decoration:none;transition:color 150ms ease-in-out;font:500 0.875rem/1.29 'Helvetica Neue',Helvetica,Arial,sans-serif;}/*!sc*/
        @media (min-width: 47.5rem){.gBHipf{font:500 1rem/1.375 'Helvetica Neue',Helvetica,Arial,sans-serif;}}/*!sc*/
        @media (hover: hover) and (pointer: fine),only screen and (-ms-high-contrast:active),(-ms-high-contrast:none){.gBHipf:hover{text-decoration:underline;}}/*!sc*/
        .gBHipf:focus-visible{outline:0.125rem solid #e61e14;outline-offset:0.25rem;border-radius:0.0625rem;}/*!sc*/
        .gBHipf:active{color:#e61e14;text-decoration:none;}/*!sc*/
        data-styled.g106[id="Footer-style__ListLink-sc-b6185a4a-4"]{content:"gBHipf,"}/*!sc*/
        .hHrptY{flex-shrink:2;flex-basis:auto;flex-direction:column;display:flex;}/*!sc*/
        @media (min-width: 47.5rem){.hHrptY{padding-top:2rem;flex-shrink:0;flex-basis:18.75rem;display:none;}}/*!sc*/
        .jMGXaU{flex-shrink:2;flex-basis:auto;flex-direction:column;display:none;}/*!sc*/
        @media (min-width: 47.5rem){.jMGXaU{padding-top:2rem;flex-shrink:0;flex-basis:18.75rem;display:flex;}}/*!sc*/
        data-styled.g107[id="Footer-style__ExternalLinksContainer-sc-b6185a4a-5"]{content:"hHrptY,jMGXaU,"}/*!sc*/
        .cGpMdv{display:flex;padding:2rem 1rem 2rem;border-top:0.0625rem solid #eeeeee;}/*!sc*/
        @media (min-width: 47.5rem){.cGpMdv{width:100%;justify-content:space-between;padding:2rem 0;border-top:0;}}/*!sc*/
        @media (min-width: 56.25rem){.cGpMdv{padding:2rem 5rem 2rem 0;}}/*!sc*/
        data-styled.g108[id="Footer-style__LinksContainer-sc-b6185a4a-6"]{content:"cGpMdv,"}/*!sc*/
        .igHesw{display:none;margin-right:2.5rem;}/*!sc*/
        .igHesw:first-child{display:block;}/*!sc*/
        @media (min-width: 47.5rem){.igHesw{display:block;}}/*!sc*/
        data-styled.g109[id="Footer-style__LinksColumn-sc-b6185a4a-7"]{content:"igHesw,"}/*!sc*/
        .fzMeat{border-top:0.0625rem solid #eeeeee;}/*!sc*/
        data-styled.g110[id="Footer-style__FooterBox-sc-b6185a4a-8"]{content:"fzMeat,"}/*!sc*/
        .cyha-DY{display:flex;flex-direction:column;align-items:center;padding-top:2rem;}/*!sc*/
        @media (min-width: 47.5rem){.cyha-DY{flex-direction:row;justify-content:space-between;max-width:75rem;margin:0 auto;padding:0 1rem;}}/*!sc*/
        data-styled.g111[id="Footer-style__Wrapper-sc-b6185a4a-9"]{content:"cyha-DY,"}/*!sc*/
        .tUkWP{padding:1rem 1rem;border-bottom:0.0625rem solid #eeeeee;transition:none;}/*!sc*/
        @media (min-width: 47.5rem){.tUkWP{padding:1rem 1rem 1rem 0;}}/*!sc*/
        .tUkWP:last-child{border-bottom:0;}/*!sc*/
        .tUkWP .ExternalItem-style__ExternalItemIcon-sc-8eb7fb85-2{background-color:#f3f3f0;}/*!sc*/
        .tUkWP .ExternalItem-style__ExternalItemContainer-sc-8eb7fb85-0{padding:0;}/*!sc*/
        .tUkWP:hover .ExternalItem-style__ExternalItemTitle-sc-8eb7fb85-3{text-decoration:underline;}/*!sc*/
        .tUkWP:focus-visible{outline:0.125rem solid #e61e14;outline-offset:-0.125rem;border-radius:0.25rem;}/*!sc*/
        data-styled.g112[id="Footer-style__StyledExternalLink-sc-b6185a4a-10"]{content:"tUkWP,"}/*!sc*/
        .gIEUJf{transition:transform 150ms ease-in-out;}/*!sc*/
        .gIEUJf svg{height:1.75rem;color:#949494;}/*!sc*/
        .gIEUJf:hover{transform:scale(1.025);}/*!sc*/
        .gIEUJf:focus-visible{outline:0.125rem solid #e61e14;outline-offset:0.25rem;border-radius:0.0625rem;}/*!sc*/
        data-styled.g113[id="Footer-style__NosLogoLink-sc-b6185a4a-11"]{content:"gIEUJf,"}/*!sc*/
        .fgjjcd{display:flex;margin-top:1rem;padding:1.5rem 1rem 2.5rem;width:100%;border-top:0.0625rem solid #eeeeee;}/*!sc*/
        @media (min-width: 47.5rem){.fgjjcd{order:1;flex-grow:1;margin-left:3.125rem;margin-top:0;border-top:0;justify-content:flex-start;padding:2rem 0;}}/*!sc*/
        data-styled.g114[id="Footer-style__FooterDisclaimer-sc-b6185a4a-12"]{content:"fgjjcd,"}/*!sc*/
        .ezaFgp{font:500 0.875rem/1.29 'Helvetica Neue',Helvetica,Arial,sans-serif;margin-right:0.75rem;}/*!sc*/
        @media (min-width: 47.5rem){.ezaFgp{margin-right:2rem;font:500 1rem/1.375 'Helvetica Neue',Helvetica,Arial,sans-serif;}}/*!sc*/
        data-styled.g115[id="Footer-style__Copyright-sc-b6185a4a-13"]{content:"ezaFgp,"}/*!sc*/
        .jJMKll{margin-right:0.75rem;color:#666666;font:500 0.875rem/1.29 'Helvetica Neue',Helvetica,Arial,sans-serif;transition:color 150ms ease-in-out;}/*!sc*/
        .jJMKll:last-child{margin:0%;}/*!sc*/
        .jJMKll:hover{color:#e61e14;text-decoration:none;}/*!sc*/
        .jJMKll:focus-visible{outline:0.125rem solid #e61e14;outline-offset:0.25rem;border-radius:0.0625rem;}/*!sc*/
        @media (min-width: 47.5rem){.jJMKll{margin-right:2rem;font:500 1rem/1.375 'Helvetica Neue',Helvetica,Arial,sans-serif;}}/*!sc*/
        data-styled.g116[id="Footer-style__FooterLink-sc-b6185a4a-14"]{content:"jJMKll,"}/*!sc*/
        .bjApuE{display:flex;justify-content:center;align-items:center;width:2rem;height:2rem;border-radius:50%;background-color:#e61e14;color:#ffffff;opacity:1;transition:transform 150ms ease-in-out;}/*!sc*/
        .bjApuE svg{transform:scale(0.8);}/*!sc*/
        .bjApuE:hover{transform:scale(1.0625);background-color:#ca1a12;}/*!sc*/
        .bjApuE:focus-visible{outline:0.125rem solid #e61e14;outline-offset:0.125rem;}/*!sc*/
        data-styled.g117[id="SocialLink-style__Link-sc-9a17f2b-0"]{content:"bjApuE,"}/*!sc*/
        .fmOrDx{display:flex;margin-top:0.6875rem;}/*!sc*/
        @media (min-width: 47.5rem){.fmOrDx{order:3;margin-top:0;}}/*!sc*/
        data-styled.g118[id="Socials-style__SocialsContainer-sc-e4251391-0"]{content:"fmOrDx,"}/*!sc*/
        .gxxKrr{flex:0 0 auto;margin:0.625rem;background-color:#e61e14;color:distinct:#ffffff;}/*!sc*/
        @media (min-width: 47.5rem){.gxxKrr{margin-right:0;margin-left:1.25rem;}}/*!sc*/
        data-styled.g119[id="Socials-style__StyledSocialLink-sc-e4251391-1"]{content:"gxxKrr,"}/*!sc*/
        .fYmuQP{display:flex;gap:0.5rem;justify-content:center;align-items:center;font:500 0.875rem/1.29 'Helvetica Neue',Helvetica,Arial,sans-serif;}/*!sc*/
        .fYmuQP svg{height:1.25rem;}/*!sc*/
        @media (min-width: 47.5rem){.fYmuQP{font:500 1rem/1.375 'Helvetica Neue',Helvetica,Arial,sans-serif;}}/*!sc*/
        data-styled.g120[id="IconAndText-style__Container-sc-337c252c-0"]{content:"fYmuQP,"}/*!sc*/
        .fIUjgB{display:flex;justify-content:center;align-items:center;}/*!sc*/
        @media (width <= calc(47.5rem - 1px)){.fIUjgB{border:0;clip:rect(0 0 0 0);height:1px;margin:-1px;overflow:hidden;padding:0;position:absolute;white-space:nowrap;width:1px;}}/*!sc*/
        data-styled.g121[id="IconAndText-style__TextContainer-sc-337c252c-1"]{content:"fIUjgB,"}/*!sc*/
        .eHZevj{position:sticky;top:0;z-index:var(--layer-navbar);pointer-events:none;}/*!sc*/
        @media (min-width: 47.5rem){.eHZevj{margin-bottom:0;}}/*!sc*/
        data-styled.g188[id="Navigation-style__Nav-sc-ffa4dc74-0"]{content:"eHZevj,"}/*!sc*/
        .fzyInM{position:absolute;top:4rem;left:0;z-index:2;margin:0;padding:0;list-style:none;}/*!sc*/
        data-styled.g189[id="SkipLinkBase-style__SkipLinkContainer-sc-f50c595d-0"]{content:"fzyInM,"}/*!sc*/
        .hwdNBv{display:block;padding:1rem;background-color:#ffffff;color:#e61e14;text-decoration:none;}/*!sc*/
        .hwdNBv:not(:focus, :active){position:absolute;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);width:0.0625rem;height:0.0625rem;white-space:nowrap;}/*!sc*/
        .hwdNBv:focus-visible{outline:0.125rem solid #e61e14;outline-offset:0.125rem;border-radius:0.125rem;}/*!sc*/
        data-styled.g190[id="SkipLinkBase-style__BasicSkipLink-sc-f50c595d-1"]{content:"hwdNBv,"}/*!sc*/
        .izjfOm{top:1.25rem;left:2.25rem;}/*!sc*/
        @media (min-width: 56.25rem){.izjfOm{top:1.25rem;left:7.5rem;}}/*!sc*/
        .izjfOm .SkipLinkBase-style__BasicSkipLink-sc-f50c595d-1{border-radius:0.375rem;box-shadow:0 0.9375rem 1.875rem 0 rgb(0 0 0 / 15%);color:#e61e14;font-weight:700;}/*!sc*/
        .izjfOm .SkipLinkBase-style__BasicSkipLink-sc-f50c595d-1:focus-visible{outline:0.125rem solid #e61e14;outline-offset:0.125rem;border-radius:0.125rem;}/*!sc*/
        data-styled.g191[id="SkipLink-style__StyledSkipLink-sc-cd0483ef-0"]{content:"izjfOm,"}/*!sc*/
        .kIsSvQ{position:absolute;top:4rem;right:0;left:0;z-index:11;margin:0;padding:0;list-style:none;}/*!sc*/
        data-styled.g192[id="SkipLinks-style__List-sc-919f0216-0"]{content:"kIsSvQ,"}/*!sc*/
        .hKpJVl{width:100%;height:100%;}/*!sc*/
        data-styled.g193[id="SkipLinks-style__ListItem-sc-919f0216-1"]{content:"hKpJVl,"}/*!sc*/
        .ipqqEc{top:0;left:0.375rem;}/*!sc*/
        data-styled.g194[id="SkipLinks-style__StyledSkipLinkListItem-sc-919f0216-2"]{content:"ipqqEc,"}/*!sc*/
        .jHkfgD{position:absolute;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);width:1px;height:1px;white-space:nowrap;}/*!sc*/
        data-styled.g966[id="VisuallyHidden-style__VisuallyHidden-sc-dd39f67a-0"]{content:"jHkfgD,"}/*!sc*/
        .kovshg{padding:0.75rem;min-width:2.75rem;min-height:2.75rem;border:none;background:#333;color:white;text-decoration:unset;font-size:0.875rem;line-height:1;transition:background-color 0.3s ease-in-out;}/*!sc*/
        data-styled.g968[id="TeletekstButton-style__ButtonBase-sc-22c8f4a9-0"]{content:"kovshg,"}/*!sc*/
        .fDVDOE{display:flex;justify-content:center;align-items:center;text-align:center;opacity:1;cursor:pointer;pointer-events:initial;}/*!sc*/
        .fDVDOE:hover,.fDVDOE:active{background:#4d4d4d;}/*!sc*/
        .fDVDOE svg{aspect-ratio:1/1;fill:#999;width:1.25rem;pointer-events:none;}/*!sc*/
        .cDcDnP{display:flex;justify-content:center;align-items:center;text-align:center;opacity:0.3;cursor:not-allowed;pointer-events:none;}/*!sc*/
        .cDcDnP:hover,.cDcDnP:active{background:#4d4d4d;}/*!sc*/
        .cDcDnP svg{aspect-ratio:1/1;fill:#999;width:1.25rem;pointer-events:none;}/*!sc*/
        data-styled.g969[id="TeletekstButton-style__TeletekstButton-sc-22c8f4a9-1"]{content:"fDVDOE,cDcDnP,"}/*!sc*/
        .dA-DODa{gap:1rem;grid-template-areas:'.  pageSelector .' 'teletekstBlock teletekstBlock teletekstBlock' 'banner banner banner';grid-template-columns:auto 12.5rem auto;place-items:start center;display:grid;padding:1rem;background-color:#212121;}/*!sc*/
        @font-face{font-family:'veramonofont2web2';src:url('https://static.nos.nl/teletekst/Android_VeraMono.eot');src:url('https://static.nos.nl/teletekst/Android_VeraMono.eot?#iefix') format('embedded-opentype'),url('https://static.nos.nl/teletekst/Android_VeraMono.woff') format('woff'),url('https://static.nos.nl/teletekst/Android_VeraMono.ttf') format('truetype'),url('https://static.nos.nl/teletekst/Android_VeraMono.svg#font') format('svg');font-weight:normal;font-style:normal;}/*!sc*/
        @media (min-width: 47.5rem){.dA-DODa{grid-template-areas:'. teletekstBlock pageSelector .' '. banner banner .';grid-template-columns:minmax(auto, 1fr) minmax(29rem, 1fr) minmax(auto, 12.5rem) minmax(auto, 1fr);margin:0 auto;}}/*!sc*/
        @media (min-width: 68.75rem){.dA-DODa{padding:1.5rem 0;grid-template-areas:'. banner teletekstBlock pageSelector .';grid-template-columns:minmax(auto, 1fr) 18.75rem minmax(auto, 36.25rem) minmax(auto, 12.5rem) minmax(
                auto,
                1fr
            );}}/*!sc*/
        @media (min-width: 77.5rem){.dA-DODa{gap:4rem;}}/*!sc*/
        data-styled.g976[id="Teletekst-style__Container-sc-7ab8a5ca-0"]{content:"dA-DODa,"}/*!sc*/
        .cAmUer{grid-area:teletekstBlock;position:relative;display:flex;margin:0;}/*!sc*/
        @media print{.cAmUer{border:0.0625rem solid #ddd;}}/*!sc*/
        data-styled.g977[id="Teletekst-style__TeletekstWrapper-sc-7ab8a5ca-1"]{content:"cAmUer,"}/*!sc*/
        .cAJitG{gap:1.25rem;grid-area:pageSelector;display:grid;margin-bottom:1.25rem;}/*!sc*/
        @media (min-width: 77.5rem){.cAJitG{gap:5rem 1.25rem;}}/*!sc*/
        data-styled.g978[id="Teletekst-style__PageSelector-sc-7ab8a5ca-2"]{content:"cAJitG,"}/*!sc*/
        .jKjyU{position:absolute;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);width:1px;height:1px;white-space:nowrap;}/*!sc*/
        data-styled.g979[id="Teletekst-style__VisuallyHidden-sc-7ab8a5ca-3"]{content:"jKjyU,"}/*!sc*/
        .iATrSz{grid-template-columns:repeat(12, 1fr);gap:0.5rem;grid-row:2/3;grid-column:1/-1;display:grid;margin:0;padding:0;list-style:none;}/*!sc*/
        data-styled.g984[id="LinkList-style__NumpadList-sc-596ba299-0"]{content:"iATrSz,"}/*!sc*/
        .byWJiW{grid-column:span 3;}/*!sc*/
        data-styled.g985[id="LinkList-style__ListItem-sc-596ba299-1"]{content:"byWJiW,"}/*!sc*/
        .jLRYAS{display:block;opacity:1;}/*!sc*/
        .LinkList-style__NumpadList-sc-596ba299-0 .jLRYAS svg{fill:white;}/*!sc*/
        .kIbtGy{display:block;opacity:0.3;}/*!sc*/
        .LinkList-style__NumpadList-sc-596ba299-0 .kIbtGy svg{fill:white;}/*!sc*/
        data-styled.g986[id="PageLink-style__StyledAnchor-sc-8dd0aadd-0"]{content:"jLRYAS,kIbtGy,"}/*!sc*/
        .hKVIga{grid-column:span 4;}/*!sc*/
        .Teletekst-style__PageSelector-sc-7ab8a5ca-2 .hKVIga{display:none;}/*!sc*/
        @media (min-width: 47.5rem){.Teletekst-style__PageSelector-sc-7ab8a5ca-2 .hKVIga{display:block;}}/*!sc*/
        .hKVIga[type='submit']{grid-column:span 3;background:#297AC3;}/*!sc*/
        .hKVIga[type='submit']:hover{background:#4793d8;}/*!sc*/
        data-styled.g987[id="Numpad-style__Button-sc-4c11bbc4-0"]{content:"hKVIga,"}/*!sc*/
        .gYknna{gap:0.5rem;grid-template-columns:repeat(12, 1fr);grid-template-rows:repeat(2, auto);display:grid;}/*!sc*/
        @media (min-width: 47.5rem){.gYknna{grid-template-rows:repeat(6, auto);}}/*!sc*/
        @media print{.gYknna{display:none;}}/*!sc*/
        data-styled.g988[id="NumpadBlock-style__StyledNumpad-sc-9defed1a-0"]{content:"gYknna,"}/*!sc*/
        .fMtOke{grid-column:span 6;position:relative;height:100%;color:white;}/*!sc*/
        data-styled.g989[id="NumpadBlock-style__InputWrapper-sc-9defed1a-1"]{content:"fMtOke,"}/*!sc*/
        .cIJDjS{width:100%;height:100%;border:none;text-align:center;}/*!sc*/
        data-styled.g990[id="NumpadBlock-style__Input-sc-9defed1a-2"]{content:"cIJDjS,"}/*!sc*/
        .hJiJtU{grid-column:span 8;}/*!sc*/
        .Teletekst-style__PageSelector-sc-7ab8a5ca-2 .hJiJtU{display:none;}/*!sc*/
        @media (min-width: 47.5rem){.Teletekst-style__PageSelector-sc-7ab8a5ca-2 .hJiJtU{display:block;}}/*!sc*/
        data-styled.g991[id="NumpadBlock-style__BackspaceButton-sc-9defed1a-3"]{content:"hJiJtU,"}/*!sc*/
        .NumpadBlock-style__StyledNumpad-sc-9defed1a-0>.lgjAUD{grid-column:span 3;}/*!sc*/
        data-styled.g992[id="NumpadBlock-style__Anchor-sc-9defed1a-4"]{content:"lgjAUD,"}/*!sc*/
        .iSaWHw{grid-column:span 4;}/*!sc*/
        .iSaWHw[type='submit']{grid-column:span 3;background:#297AC3;}/*!sc*/
        .iSaWHw[type='submit']:hover{background:#4793d8;}/*!sc*/
        data-styled.g993[id="NumpadBlock-style__Button-sc-9defed1a-5"]{content:"iSaWHw,"}/*!sc*/
        .kziuZS{-webkit-font-smoothing:initial;aspect-ratio:4/5;margin:0;max-height:calc(100vh - 8.5rem0.125rem);color:white;white-space:pre-wrap;font-size:clamp(0.74rem, 0.0418rem + 3.4909vw, 1.7rem);font-family:'veramonofont2web2','Vera Mono',monospace;line-height:normal;}/*!sc*/
        @media (min-width: 47.5rem){.kziuZS{font-size:1.2rem;}}/*!sc*/
        @media (min-width: 68.75rem){.kziuZS{font-size:clamp(0.85rem, -0.2333rem + 1.9259vw, 1.5rem);}}/*!sc*/
        @media print{.kziuZS{color:#222222!important;}}/*!sc*/
        .kziuZS *.black{color:#000;}/*!sc*/
        .kziuZS *.bg-black{background:#000;}/*!sc*/
        .kziuZS *.red{color:#f00;}/*!sc*/
        .kziuZS *.bg-red{background:#f00;}/*!sc*/
        .kziuZS *.green{color:#0f0;}/*!sc*/
        .kziuZS *.bg-green{background:#0f0;}/*!sc*/
        .kziuZS *.yellow{color:#ff0;}/*!sc*/
        .kziuZS *.bg-yellow{background:#ff0;}/*!sc*/
        .kziuZS *.blue{color:#00f;}/*!sc*/
        .kziuZS *.bg-blue{background:#00f;}/*!sc*/
        .kziuZS *.magenta{color:#f0f;}/*!sc*/
        .kziuZS *.bg-magenta{background:#f0f;}/*!sc*/
        .kziuZS *.cyan{color:#0ff;}/*!sc*/
        .kziuZS *.bg-cyan{background:#0ff;}/*!sc*/
        .kziuZS *.white{color:#fff;}/*!sc*/
        .kziuZS *.bg-white{background:#fff;}/*!sc*/
        .kziuZS a{color:white;text-decoration:none;}/*!sc*/
        .kziuZS a[id^='fastText']{display:inline;}/*!sc*/
        data-styled.g994[id="TeletekstContent-style__TeletekstBlock-sc-39080529-0"]{content:"kziuZS,"}/*!sc*/
        .bnpXYt{grid-area:banner;place-self:stretch center;display:none;overflow:hidden;width:100%;}/*!sc*/
        @media print{.bnpXYt{display:none!important;}}/*!sc*/
        data-styled.g995[id="TeletekstSterBanner-style__Container-sc-a7cbf7a-0"]{content:"bnpXYt,"}/*!sc*/
        .gNlLKh{display:inline-block;margin:0.75rem 0;width:100%;color:white;text-align:center;text-transform:uppercase;letter-spacing:0.0625rem;font:bold 0.875rem/1.29 'Helvetica Neue',Helvetica,Arial,sans-serif;}/*!sc*/
        .gNlLKh a{color:white;transition:color 150ms ease-in-out;}/*!sc*/
        .gNlLKh a:hover{color:#999;}/*!sc*/
        data-styled.g996[id="TeletekstSterBanner-style__Title-sc-a7cbf7a-1"]{content:"gNlLKh,"}/*!sc*/
        .eCBVlN{display:flex;justify-content:center;overflow:hidden;margin:auto;}/*!sc*/
        data-styled.g997[id="TeletekstSterBanner-style__Banner-sc-a7cbf7a-2"]{content:"eCBVlN,"}/*!sc*/
        body {background-color: black;}</style></head><body><div class="kziuZS">"""
        base = self.json["content"].replace('\n', '<br>').lstrip().rstrip()
        after = "</div></body></html>"
        with open('/tmp/index.html', 'w') as temp:
            temp.write(f"{pre}{base}{after}")
            temp.close()

    @property
    def prevPage(self):
        try:
            value = self.json["prevPage"]
            return value
        except:
            return None

    @property
    def nextPage(self):
        try:
            value = self.json["nextPage"]
            return value
        except:
            return None

    @property
    def subpages(self):
        value = int(self.subpage)

        while True:
            if int(value) > 50:
                return 1
            if not self.checksubpageNum(value):
                return int(value)-1
            value = int(value)+1

    def checkpageNum(self, pageNum):
        try:
            url = f"https://teletekst-data.nos.nl/json/{pageNum}-1"

            rq = requests.get(url)

            son = json.loads(rq.text)

            value = self.json["content"]
            return True
        except:
            return False

    def checksubpageNum(self, subpageNum):
        try:
            url = f"https://teletekst-data.nos.nl/json/{self.pagenum}-{subpageNum}"

            rq = requests.get(url)

            son = json.loads(rq.text)

            value = self.json["content"]
            return True
        except:
            return False

class hrTeletextReader:
    def __init__(self, *args, **kwargs):
        self.pagenum = "100"
        self.subpage = "01"
        self.stationid = "hrt"
        self.getPage()
    
    def getPage(self):
        url = f"https://teletekst.hrt.hr/api/getNewPage?pageNum={self.pagenum}-{self.subpage}.HTML"

        rq = requests.get(url)

        self.json = json.loads(rq.text)

    @property
    def getPageGif(self):
        try:
            value = self.json["ttxImg"].replace("data:image/gif;base64,", "")
            return base64.b64decode(value)
        except:
            pagenum = self.pagenum
            subpage = self.subpage
            self.pagenum = "100"
            self.subpage = "01"
            self.getPage()
            value = self.json["ttxImg"].replace("data:image/gif;base64,", "")
            self.pagenum = pagenum
            self.subpage = subpage
            self.getPage()
            return base64.b64decode(value)
    
    @property
    def prevPage(self):
        try:
            value = self.json["documentJson"]["DOCUMENT"]["PREV_PAGEREF"]["_attributes"]["value"].split("-")[0]
            return int(value)
        except:
            return None
    
    @property
    def nextPage(self):
        try:
            value = self.json["documentJson"]["DOCUMENT"]["NEXT_PAGEREF"]["_attributes"]["value"].split("-")[0]
            return int(value)
        except:
            return None

    @property
    def subpages(self):
        value = int(self.subpage)

        while True:
            if int(value) > 50:
                return 1
            if not self.checksubpageNum(value):
                return int(value)-1
            value = int(value)+1

    def checkpageNum(self, pageNum):
        try:
            url = f"https://teletekst.hrt.hr/api/getNewPage?pageNum={pageNum}-01.HTML"

            rq = requests.get(url)

            son = json.loads(rq.text)

            value = self.json["ttxImg"]
            return True
        except:
            return False

    def checksubpageNum(self, subpageNum):
        try:
            url = f"https://teletekst.hrt.hr/api/getNewPage?pageNum={self.pagenum}-{subpageNum:02d}.HTML"

            rq = requests.get(url)

            son = json.loads(rq.text)

            value = self.json["ttxImg"]
            return True
        except:
            return False