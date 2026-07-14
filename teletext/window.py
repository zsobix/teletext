try:
    from .handler import *
except:
    from handler import *

import gi
import re
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version("WebKit", "6.0")
from gi.repository import Gtk, Gdk, Adw, Gio, GdkPixbuf, WebKit, GLib


css_provider = Gtk.CssProvider()
css_provider.load_from_string("""
.margin {
    margin: 5px;
}
.image {
    margin-left: 30px;
    margin-right: 30px;
    border-radius: 10px;
}
.nav {
    margin-top: 30px;
    margin-bottom: 30px;
}
.navbuttons {
    margin: 5px;
    border-radius: 30px
}
.redbutton {
    margin-left: 40px;
    margin-right: 120px;
    background-color: red;
    border-radius: 15px;
}
.greenbutton {
    margin-right: 100px;
    background-color: lime;
    border-radius: 15px;
}
.yellowbutton {
    margin-right: 100px;
    background-color: yellow;
    border-radius: 15px;
}
.bluebutton {
    margin-left: 20px;
    margin-right: 40px;
    background-color: blue;
    border-radius: 15px;
}
.countrybutton {
    margin: 10px;
    padding: 10px;
    border-radius: 12px;
    border-style: solid;
    border-width: 1px;
    border-color: grey;
}
.countrybutton:hover {
    background-color: #282830;
}
.label {
    margin-top: 20px;
    margin-bottom: 5px;
}
.region {
    margin: 5px;
    border-radius: 30px;
}
.background {
    background-color: #222229;
    border-color: #222229;
}
.sidebar {
    background-color: #282830;
    border-color: #282830;
}

.togglegroup {
    margin: 10px;
}
.favouritesbox {
    margin: 20px;
    border-color: white;
    border-style: dashed;
    border-width: 3px;
    border-radius: 15px;
}
.favourites {
    margin: 20px;
    padding: 10px;
    border-radius: 10px;
    background-color: #38383E;
}
.favlabel {
    margin-left: 15px;
    margin-right: 15px;
}
""")
Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(900, 800)
        self.set_title("Teletext")
        self.titlebar = Adw.HeaderBar()
        self.titlebar.set_css_classes(["background"])
        self.set_titlebar(self.titlebar)
        self.country = "hu"

        collapse = Gtk.Button()
        collapse.connect("clicked", self.collapse)
        collapse.set_icon_name("sidebar-show-symbolic")

        home = Gtk.Button()
        home.connect("clicked", self.home)
        home.set_icon_name("go-home-symbolic")

        info = Gtk.Button()
        info.connect("clicked", self.aboutDialog)
        self.dialog = Adw.AboutDialog()
        self.dialog.set_application_icon('xyz.zsobix.teletext')
        self.dialog.set_application_name('TeleReader')
        self.dialog.set_developer_name('zsobix')
        self.dialog.set_license_type(Gtk.License.GPL_3_0)
        self.dialog.set_website('https://zsobix.xyz')
        self.dialog.add_acknowledgement_section('', ['Hack Club (for hosting Stardance) https://hackclub.com'])
        info.set_icon_name("help-about-symbolic")

        favourites = Gtk.Button()
        favourites.connect("clicked", self.favouritesPage)
        favourites.set_icon_name("starred-symbolic")
        self.favourites = []
        
        fav_add = Gtk.Button()
        fav_add.connect('clicked', self.addFavorite)
        fav_add.set_icon_name("star-new-symbolic")

        self.titlebar.pack_start(collapse)
        self.titlebar.pack_start(home)

        self.titlebar.pack_end(info)
        self.titlebar.pack_end(favourites)
        self.titlebar.pack_end(fav_add)

        self.init()
        
        self.window = Adw.NavigationSplitView()
        self.set_child(self.window)

        self.content = Adw.NavigationPage(title="content")
        self.content.set_css_classes(["background"])
        self.window.set_content(self.content)

        self.sidebar = Adw.NavigationPage(title="countries")
        self.sidebar.set_css_classes(["sidebar"])
        self.window.set_sidebar(self.sidebar)

        self.window.set_collapsed(True)
        self.window.set_show_content(True)

        self.scrollsidebar = Gtk.ScrolledWindow()
        self.scrollsidebar.set_min_content_width(280)
        self.sidebar.set_child(self.scrollsidebar)

        self.sidebox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.scrollsidebar.set_child(self.sidebox)

        # TODO make this a scrolled window with all channels separated
        self.countries = [["🇭🇺 MTVA", "hu", "mtva"],
                    ["🇦🇹 ORF 1", "at", "orf1"],
                    ["🇦🇹 ORF 2", "at", "orf2"],
                    ["🇦🇹 ORF III", "at", "orfiii"],
                    ["🇦🇹 ORF Sport Plus", "at", "sportplus"],
                    ["🇦🇹 SAT.1", "other", "s1at"],
                    ["🇦🇹 ProSieben", "other", "p7at"],
                    ["🇦🇹 kabel eins", "other", "k1at"],
                    ["🇦🇹 sixx", "other", "sixxat"],
                    ["🇦🇹 SAT.1 Gold", "other", "s1goldat"],
                    ["🇦🇹 ProSieben MAXX", "other", "p7maxxat"],
                    ["🇦🇹 kabel eins Doku", "other", "k1dokuat"],
                    ["🇩🇪 ZDF", "de", "zdf"],
                    ["🇩🇪 ZDFneo", "de", "zdfneo"],
                    ["🇩🇪 ZDFinfo", "de", "zdfinfo"],
                    ["🇩🇪 3sat", "de", "3sat"],
                    ["🇩🇪 ARD", "other2", "br-alpha"],
                    ["🇩🇪 Arte", "other2", "DE_arte"],
                    ["🇩🇪 KiKa", "kika", "kika"],
                    ["🇩🇪 SAT.1", "other", "s1de"],
                    ["🇩🇪 ProSieben", "other", "p7de"],
                    ["🇩🇪 kabel eins", "other", "k1de"],
                    ["🇩🇪 sixx", "other", "sixx"],
                    ["🇩🇪 SAT.1 Gold", "other", "s1gold"],
                    ["🇩🇪 ProSieben MAXX", "other", "p7maxx"],
                    ["🇩🇪 kabel eins Doku", "other", "k1doku"],
                    ["🇩🇪 RBB", "other2", "rbb"],
                    ["🇩🇪 MDR", "other2", "mdr-sachsen"],
                    ["🇮🇹 Rai (slow)", "it", "rai"],
                    ["🇸🇪 SVT", "se", "svt"],
                    ["🇨🇭 SRF 1", "ch", "srf1"],
                    ["🇨🇭 SRF zwei", "ch", "srfzwei"],
                    ["🇨🇭 SRF Info", "ch", "srfinfo"],
                    ["🇨🇭 RTS 1", "ch", "rtsun"],
                    ["🇨🇭 RTS 2", "ch", "rtsdeux"],
                    ["🇨🇭 RSI LA 1", "ch", "rsila1"],
                    ["🇨🇭 RSI LA 2", "ch", "rsila2"],
                    ["🇨🇭 SAT.1", "other", "s1ch"],
                    ["🇨🇭 ProSieben", "other", "p7ch"],
                    ["🇨🇭 kabel eins",  "other", "k1ch"],
                    ["🇨🇭 sixx", "other", "sixxch"],
                    ["🇨🇭 SAT.1 Gold", "other", "s1goldch"],
                    ["🇨🇭 ProSieben MAXX", "other", "p7maxxch"],
                    ["🇨🇭 Puls8", "other", "puls8ch"],
                    ["🇨🇿 ČT", "cz", "ČT"],
                    ["🇫🇮 Yle", "fi", "yle"],
                    ["🇩🇰 DR", "dk", "dr"],
                    ["🇪🇸 TVE", "es", "tve"],
                    ["🇵🇱 TVP 1", "pl", "TG1"],
                    ["🇵🇱 TVP 2", "pl", "TG2"],
                    ["🇧🇦 BHRT", "ba", "bhrt"],
                    ["🇳🇱 NOS", "nl", "nos"],
                    ["🇭🇷 HRT", "hr", "hrt"],
                    ["🇽🇹 ???", "xx", "xx"]]
        
        for country in self.countries:
            button = Gtk.Button()
            button.connect('clicked', self.countrySelect)
            buttitle = Gtk.Label()
            buttitle.set_markup(f'<span size="x-large">{country[0]}</span>')
            button.set_child(buttitle)
            button.set_css_classes(["countrybutton"])
            self.sidebox.append(button)
        self.home()

    def home(self, *args, **kwargs):
        self.teletext.getPage()
        self.cbox = Gtk.CenterBox()
        self.ccbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.cbox.set_center_widget(self.ccbox)
        self.content.set_child(self.cbox)
        b64 = ["se",
                "fi",
                "hr",
                "other2",
                "xx"]
        if self.country == "de":
            scroll = Gtk.ScrolledWindow()
            scroll.set_min_content_height(500)
            scroll.set_min_content_width(500)
            scroll.set_overlay_scrolling(False)
            self.ccbox.append(scroll)
            self.view = WebKit.WebView().new()
            if int(self.teletext.subpage) == 1:
                self.view.load_uri(f"https://teletext.zdf.de/teletext/{self.teletext.stationid}/seiten/klassisch/{self.teletext.pagenum}.html")
            else:
                self.view.load_uri(f"https://teletext.zdf.de/teletext/{self.teletext.stationid}/seiten/klassisch/{self.teletext.pagenum}_{int(self.teletext.subpage)-1}.html")
            scroll.set_child(self.view)
        elif self.country == "nl":
            scroll = Gtk.ScrolledWindow()
            scroll.set_min_content_height(500)
            scroll.set_min_content_width(450)
            scroll.set_overlay_scrolling(False)
            self.ccbox.append(scroll)
            self.view = WebKit.WebView().new()
            self.teletext.writetempHTML()
            self.view.load_uri(f"file:///tmp/index.html")
            scroll.set_child(self.view)
        elif self.country not in b64:
            img = Gio.File.new_for_uri(self.teletext.getPageGif)
            img2 = GdkPixbuf.Pixbuf.new_from_stream(img.read(cancellable=None))
            image = Gtk.Image().new_from_pixbuf(img2)
            image.set_pixel_size(520)
            image.set_css_classes(["image"])
            self.ccbox.append(image)
        elif self.country in b64:
            raw = GLib.Bytes(self.teletext.getPageGif)
            rawstream = Gio.MemoryInputStream.new_from_bytes(raw)
            img2 = GdkPixbuf.Pixbuf.new_from_stream(rawstream)
            image = Gtk.Image().new_from_pixbuf(img2)
            image.set_pixel_size(520)
            image.set_css_classes(["image"])
            self.ccbox.append(image)

        self.inputbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.inputbox.set_valign(Gtk.Align.CENTER)
        self.inputbox.set_halign(Gtk.Align.CENTER)
        self.inputbox.set_css_classes(["nav"])
        self.ccbox.append(self.inputbox)

        text = Gtk.Label()
        text.set_markup('<span size="large">Page Number</span>')
        inputbuf = Gtk.EntryBuffer()
        inputbuf.set_text(str(self.teletext.pagenum), -1)

        self.input = Gtk.Entry().new_with_buffer(inputbuf)
        self.input.connect('notify::text', self.pagenumEntry)
        self.input.set_max_length(3)
        self.input.set_input_purpose(Gtk.InputPurpose.DIGITS)
        self.input.props.xalign = 0.5
        self.inputbox.append(text)
        self.inputbox.append(self.input)
        self.cccbox = Gtk.CenterBox()
        self.buttonsbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.inputbox.append(self.cccbox)
        self.cccbox.set_center_widget(self.buttonsbox)

        backbutton = Gtk.Button().new_from_icon_name('go-previous-symbolic')
        backbutton.set_css_classes(["navbuttons"])
        backbutton.connect('clicked', self.prevPage)
        nextbutton = Gtk.Button().new_from_icon_name('go-next-symbolic')
        nextbutton.set_css_classes(["navbuttons"])
        nextbutton.connect('clicked', self.nextPage)
        backsubbutton = Gtk.Button().new_from_icon_name('go-up-symbolic')
        backsubbutton.set_css_classes(["navbuttons"])
        backsubbutton.connect('clicked', self.prevsubPage)
        nextsubbutton = Gtk.Button().new_from_icon_name('go-down-symbolic')
        nextsubbutton.set_css_classes(["navbuttons"])
        nextsubbutton.connect('clicked', self.nextsubPage)

        self.buttonsbox.append(backbutton)
        self.buttonsbox.append(backsubbutton)

        subpage = Gtk.Label()
        subpage.set_markup(f'<span>{int(self.teletext.subpage)}/{self.teletext.subpages}</span>')
        subpage.set_css_classes(["margin"])
        self.buttonsbox.append(subpage)

        self.buttonsbox.append(nextsubbutton)
        self.buttonsbox.append(nextbutton)
        if self.country == "it":
            label = Gtk.Label()
            label.set_markup('<span>Regions</span>')
            label.set_css_classes(["label"])
            self.inputbox.append(label)
            
            self.regions = Gtk.DropDown()
            self.regions.set_css_classes(["region"])
            self.regions.set_enable_search(True)
            regionlist = Gtk.StringList()
            for region in self.teletext.regions:
                regionlist.append(region)
            self.regions.props.model = regionlist
            self.regions.set_selected(regionlist.find(self.teletext.region))
            self.regions.connect('notify::selected-item', self.regionSwitcher)
            self.inputbox.append(self.regions)

    def pagenumEntry(self, *args, **kwargs):
        buf = self.input.get_buffer()
        text = buf.get_text()
        if len(text) == 3:
            if self.teletext.checkpageNum(text):
                self.teletext.pagenum = text
                if self.country != "de":
                    self.teletext.subpage = "01"
                self.home()
            else:
                self.teletext.pagenum = "100"
                if self.country != "de":
                    self.teletext.subpage = "01"
                self.home()
    
    def nextPage(self, *args, **kwargs):
        if self.country == "hu":
            nextpage = self.teletext.nextPage
            if nextpage == None:
                pass
            else:
                self.teletext.pagenum = nextpage[0]
                self.teletext.subpage = nextpage[1]
                self.home()
        elif self.country == "de" or self.country == "it" or self.country == "se" or self.country == "ch":
            try:
                if self.teletext.nextPage != None:
                    self.teletext.pagenum = self.teletext.nextPage
                    self.teletext.subpage = "1"
                    self.teletext.getPage()
            except:
                self.teletext.pagenum = "100"
                self.teletext.subpage = "1"
            self.home()
        else:
            try:
                if self.teletext.nextPage != None:
                    self.teletext.pagenum = self.teletext.nextPage
                    self.teletext.subpage = "01"
                    self.teletext.getPage()
            except:
                self.teletext.pagenum = "100"
                self.teletext.subpage = "01"
            self.home()
    def prevPage(self, *args, **kwargs):
        if self.country == "hu":
            prevpage = self.teletext.prevPage
            if prevpage == None:
                pass
            else:
                self.teletext.pagenum = prevpage[0]
                self.teletext.subpage = prevpage[1]
                self.home()
        elif self.country == "de" or self.country == "it" or self.country == "se" or self.country == "ch":
            try:
                if self.teletext.prevPage != None:
                    self.teletext.pagenum = self.teletext.prevPage
                    self.teletext.subpage = "1"
                    self.teletext.getPage()
            except:
                self.teletext.pagenum = "100"
                self.teletext.subpage = "1"
            self.home()
        else:
            try:
                if self.teletext.prevPage != None:
                    self.teletext.pagenum = self.teletext.prevPage
                    self.teletext.subpage = "01"
                    self.teletext.getPage()
            except:
                self.teletext.pagenum = "100"
                self.teletext.subpage = "01"
            self.home()
    def nextsubPage(self, *args, **kwargs):
        if self.country == "hu":
            nextsubpage = self.teletext.nextSubpage
            if nextsubpage == None:
                pass
            else:
                self.teletext.pagenum = nextsubpage[0]
                self.teletext.subpage = nextsubpage[1]
                self.home()
        else:
            nextsubpage = int(self.teletext.subpage)+1
            if nextsubpage <= self.teletext.subpages:
                self.teletext.subpage = f"{nextsubpage:02d}"
                self.home()
    def prevsubPage(self, *args, **kwargs):
        if self.country == "hu":
            prevsubpage = self.teletext.prevSubpage
            if prevsubpage == None:
                pass
            else:
                self.teletext.pagenum = prevsubpage[0]
                self.teletext.subpage = prevsubpage[1]
                self.home()
        else:
            prevsubpage = int(self.teletext.subpage)-1
            if prevsubpage >= 1:
                self.teletext.subpage = f"{prevsubpage:02d}"
                self.home()
    
    def collapse(self, *args, **kwargs):
        self.window.set_collapsed(not self.window.get_collapsed())
        # if self.window.get_collapsed:
        #     self.window.set_collapsed(False)
        # else:
        #     self.window.set_collapsed(True)

    def countrySelect(self, *args, **kwargs):
        value = args[0].get_child().get_text()
        for i in range(len(self.countries)):
            try:
                if value == self.countries[i][0]:
                    self.country = self.countries[i][1]
                    self.init()
                    self.teletext.stationid = self.countries[i][2]
                    self.home()
            except:
                pass
    
    def init(self, *args, **kwargs):
        match self.country:
            case "hu":
                self.teletext = hunTeletextReader()
            case "at":
                self.teletext = atTeletextReader()
            case "de":
                self.teletext = gerTeletextReader()
            case "it":
                self.teletext = itTeletextReader()
            case "se":
                self.teletext = seTeletextReader()
            case "ch":
                self.teletext = chTeletextReader()
            case "cz":
                self.teletext = czTeletextReader()
            case "fi":
                self.teletext = fiTeletextReader()
            case "other":
                self.teletext = otherTeletextReader()
            case "dk":
                self.teletext = dkTeletextReader()
            case "other2":
                self.teletext = other2TeletextReader()
            case "kika":
                self.teletext = kikaTeletextReader()
            case "es":
                self.teletext = esTeletextReader()
            case "pl":
                self.teletext = plTeletextReader()
            case "ba":
                self.teletext = baTeletextReader()
            case "nl":
                self.teletext = nlTeletextReader()
            case "hr":
                self.teletext = hrTeletextReader()
            case "xx":
                self.teletext = xxTeletextReader()

    def stationSwitcher(self, *args, **kwargs):
        if self.teletext.stationid != self.stations[self.togglegroup.get_active()].replace(" ", ""):
            self.teletext.stationid = self.stations[self.togglegroup.get_active()].replace(" ", "")
            self.station = self.stations[self.togglegroup.get_active()]
            self.togglegroup = Adw.ToggleGroup()
            self.teletext.pagenum = "100"
            if self.country != "de":
                self.teletext.subpage = "01"
            else:
                self.teletext.subpage = "1"
            self.home()
    
    def regionSwitcher(self, *args, **kwargs):
        selected = self.regions.get_selected_item().get_string()
        if self.teletext.region != selected:
            self.teletext.region = selected
            self.teletext.subpage = "1"
            if selected == "Nazionale":
                self.teletext.pagenum = "100"
            else:
                self.teletext.pagenum = "300"
            self.home()
    
    def otherstationSwitcher(self, *args, **kwargs):
        selected = self.stationdd.get_selected_item().get_string()
        result = re.search(r'^.*\((.*)\)', selected)

        if self.teletext.stationid != result.group(1):
            self.teletext.stationid = result.group(1)
            self.teletext.subpage = "01"
            self.teletext.pagenum = "100"
            self.home()
    
    def aboutDialog(self, *args, **kwargs):
        self.dialog.present()

    def favouritesPage(self, *args, **kwargs):
        scroll = Gtk.ScrolledWindow()
        self.content.set_child(scroll)

        mainbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        mainbox.set_css_classes(["favouritesbox"])

        scroll.set_child(mainbox)

        for favourite in self.favourites:
            button = Gtk.CenterBox()
            button.set_css_classes(["favourites"])

            favbutton = Gtk.Button()

            label = Gtk.Label()
            label.set_css_classes(["favlabel"])
            label.set_markup(f'<span>{favourite[0]}</span>')

            favbutton.set_child(label)
            favbutton.set_halign(Gtk.Align.START)
            favbutton.connect('clicked', self.gotoFavourite)
            button.set_start_widget(favbutton)

            endbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            endbox.set_halign(Gtk.Align.END)
            button.set_end_widget(endbox)

            label = Gtk.Label()
            label.set_css_classes(["favlabel"])
            label.set_markup(f'<span>{favourite[1]}</span>')
            endbox.append(label)

            remove = Gtk.Button()
            remove.set_icon_name('window-close-symbolic')
            remove.connect('clicked', self.removeFavourite)
            endbox.append(remove)

            mainbox.append(button)
        if len(self.favourites) == 0:
            label = Gtk.Label()
            label.set_markup('<span weight="bold" size="x-large">There are no favorites right now.</span>')
            
            label.set_halign(Gtk.Align.CENTER)
            label.set_valign(Gtk.Align.CENTER)
            mainbox.append(label)

    def removeFavourite(self, *args, **kwargs):
        pagenum = args[0].get_parent().get_parent().get_start_widget().get_child().get_text()
        value = args[0].get_parent().get_first_child().get_text()
        for favorite in self.favourites:
            if favorite[0] == pagenum and favorite[1] == value:
                self.favourites.remove(favorite)
        self.favouritesPage()
    
    def gotoFavourite(self, *args, **kwargs):
        pagenum = args[0].get_child().get_text()
        value = args[0].get_parent().get_end_widget().get_first_child().get_text()
        for i in range(len(self.countries)):
            if self.countries[i][0] == value:
                self.country = self.countries[i][1]
                self.init()
                self.teletext.stationid = self.countries[i][2]
                self.teletext.pagenum = pagenum
                self.home()

    def addFavorite(self, *args, **kwargs):
        for i in range(len(self.countries)):
            if self.country == self.countries[i][1] and self.teletext.stationid == self.countries[i][2]:
                value = [str(self.teletext.pagenum), self.countries[i][0]]
        if value not in self.favourites:
            self.favourites.append(value)
        

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

if __name__ == "__main__":
    app = MyApp(application_id="xyz.zsobix.teletext")
    app.run()
