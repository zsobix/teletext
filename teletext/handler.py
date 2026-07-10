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