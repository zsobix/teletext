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
    margin-top: 10px;
    margin-left: 5px;
    margin-right: 5px;
    margin-bottom: 10px;
    padding: 10px;
    border-radius: 30px;
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

        self.titlebar.pack_start(collapse)

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

        self.sidebox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.sidebar.set_child(self.sidebox)

        # TODO make this a scrolled window with all channels separated
        countries = ["🇭🇺 Hungary", "🇦🇹 Austria", "🇩🇪 Germany", "🇮🇹 Italy (slow)", "🇸🇪 Sweden", "🇨🇭 Switzerland", "🇨🇿 Czechia", "🇫🇮 Finland", "🇧🇺 Other"]
        for country in countries:
            button = Gtk.Button()
            button.connect('clicked', self.countrySelect)
            buttitle = Gtk.Label()
            buttitle.set_markup(f'<span size="x-large">{country}</span>')
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
        match self.country:
            case "hu":
                img = Gio.File.new_for_uri(self.teletext.getPageGif)
                img2 = GdkPixbuf.Pixbuf.new_from_stream(img.read(cancellable=None))
                image = Gtk.Image().new_from_pixbuf(img2)
                self.teletext.colorbuttonsInit()
                image.set_pixel_size(520)
                image.set_css_classes(["image"])
                self.ccbox.append(image)
            case "at":
                img = Gio.File.new_for_uri(self.teletext.getPageGif)
                img2 = GdkPixbuf.Pixbuf.new_from_stream(img.read(cancellable=None))
                image = Gtk.Image().new_from_pixbuf(img2)
                image.set_pixel_size(520)
                image.set_css_classes(["image"])
                self.ccbox.append(image)
            case "it":
                img = Gio.File.new_for_uri(self.teletext.getPageGif)
                img2 = GdkPixbuf.Pixbuf.new_from_stream(img.read(cancellable=None))
                image = Gtk.Image().new_from_pixbuf(img2)
                image.set_pixel_size(520)
                image.set_css_classes(["image"])
                self.ccbox.append(image)
            case "de":
                scroll = Gtk.ScrolledWindow()
                scroll.set_min_content_height(500)
                scroll.set_min_content_width(500)
                scroll.set_overlay_scrolling(False)
                self.ccbox.append(scroll)
                self.view = WebKit.WebView().new()
                if self.teletext.subpage == "1":
                    self.view.load_uri(f"https://teletext.zdf.de/teletext/{self.teletext.stationid}/seiten/klassisch/{self.teletext.pagenum}.html")
                else:
                    self.view.load_uri(f"https://teletext.zdf.de/teletext/{self.teletext.stationid}/seiten/klassisch/{self.teletext.pagenum}_{int(self.teletext.subpage)-1}.html")
                scroll.set_child(self.view)
            case "se":
                raw = GLib.Bytes(self.teletext.getPageGif)
                rawstream = Gio.MemoryInputStream.new_from_bytes(raw)
                img2 = GdkPixbuf.Pixbuf.new_from_stream(rawstream)
                image = Gtk.Image().new_from_pixbuf(img2)
                image.set_pixel_size(520)
                image.set_css_classes(["image"])
                self.ccbox.append(image)
            case "ch":
                img = Gio.File.new_for_uri(self.teletext.getPageGif)
                img2 = GdkPixbuf.Pixbuf.new_from_stream(img.read(cancellable=None))
                image = Gtk.Image().new_from_pixbuf(img2)
                image.set_pixel_size(520)
                image.set_css_classes(["image"])
                self.ccbox.append(image)
            case "cz":
                img = Gio.File.new_for_uri(self.teletext.getPageGif)
                img2 = GdkPixbuf.Pixbuf.new_from_stream(img.read(cancellable=None))
                image = Gtk.Image().new_from_pixbuf(img2)
                image.set_pixel_size(520)
                image.set_css_classes(["image"])
                self.ccbox.append(image)
            case "fi":
                raw = GLib.Bytes(self.teletext.getPageGif)
                rawstream = Gio.MemoryInputStream.new_from_bytes(raw)
                img2 = GdkPixbuf.Pixbuf.new_from_stream(rawstream)
                image = Gtk.Image().new_from_pixbuf(img2)
                image.set_pixel_size(520)
                image.set_css_classes(["image"])
                self.ccbox.append(image)
            case "other":
                img = Gio.File.new_for_uri(self.teletext.getPageGif)
                img2 = GdkPixbuf.Pixbuf.new_from_stream(img.read(cancellable=None))
                image = Gtk.Image().new_from_pixbuf(img2)
                image.set_pixel_size(520)
                image.set_css_classes(["image"])
                self.ccbox.append(image)
        if self.country == "hu":
            #buttons
            self.colorbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

            redbutton = Gtk.Button()
            redbutton.set_css_classes(["redbutton"])
            redbutton.connect('clicked', self.redbuttonHandler)
            self.colorbox.append(redbutton)

            greenbutton = Gtk.Button()
            greenbutton.set_css_classes(["greenbutton"])
            greenbutton.connect('clicked', self.greenbuttonHandler)
            self.colorbox.append(greenbutton)

            yellowbutton = Gtk.Button()
            yellowbutton.set_css_classes(["yellowbutton"])
            yellowbutton.connect('clicked', self.yellowbuttonHandler)
            self.colorbox.append(yellowbutton)

            bluebutton = Gtk.Button()
            bluebutton.set_css_classes(["bluebutton"])
            bluebutton.connect('clicked', self.bluebuttonHandler)
            self.colorbox.append(bluebutton)

            self.ccbox.append(self.colorbox)
        

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
        match self.country:
            case "hu":
                self.stations = ["mtva"]
            case "at":
                self.stations = ["orf 1", "orf 2", "orf iii", "sport plus"]
            case "de":
                self.stations = ["zdf", "zdf neo", "zdf info", "3sat"]
            case "it":
                self.stations = ["rai"]
            case "se":
                self.stations = ["svt"]
            case "ch":
                self.stations = ["SRF 1", "SRF zwei", "SRF Info", "RTS Un", "RTS Deux", "RSI LA 1", "RSI LA 2"]
            case "cz":
                self.stations = ["ČT"]
            case "fi":
                self.stations = ["yle"]
        if self.country != "other":
            self.togglegroup = Adw.ToggleGroup()
            self.togglegroup.set_css_classes(["round", "togglegroup"])
            try:
                if self.station not in self.stations:
                    raise Exception
            except:
                self.station = self.stations[0]
            for station in self.stations:
                toggle = Adw.Toggle()
                label = Gtk.Label()
                label.set_markup(f'<span>{station.upper()}</span>')
                toggle.set_child(label)
                self.togglegroup.set_active(self.stations.index(self.station))
                self.togglegroup.add(toggle)
            self.togglegroup.connect('notify::active', self.stationSwitcher)
            self.inputbox.append(self.togglegroup)

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
        if self.country == "other":
            label = Gtk.Label()
            label.set_markup('<span>Stations</span>')
            label.set_css_classes(["label"])
            self.inputbox.append(label)
            
            self.stationdd = Gtk.DropDown()
            self.stationdd.set_css_classes(["region"])
            self.stationdd.set_enable_search(True)
            stationlist = Gtk.StringList()
            for station in self.teletext.stations:
                stationlist.append(station)
            self.stationdd.props.model = stationlist
            self.stationdd.set_selected(self.teletext.stationsid.index(self.teletext.stationid))
            self.stationdd.connect('notify::selected-item', self.otherstationSwitcher)
            self.inputbox.append(self.stationdd)
        

    def pagenumEntry(self, *args, **kwargs):
        buf = self.input.get_buffer()
        text = buf.get_text()
        if len(text) == 3:
            if self.teletext.checkpageNum(text):
                self.teletext.pagenum = text
                self.home()
            else:
                self.teletext.pagenum = "100"
                self.home()
    
    def nextPage(self, *args, **kwargs):
        match self.country:
            case "hu":
                nextpage = self.teletext.nextPage
                if nextpage == None:
                    pass
                else:
                    self.teletext.pagenum = nextpage[0]
                    self.teletext.subpage = nextpage[1]
                    self.home()
            case "at":
                try:
                    if self.teletext.nextPage != None:
                        self.teletext.pagenum = self.teletext.nextPage
                        self.teletext.subpage = "01"
                        self.teletext.getPage()
                except:
                    self.teletext.pagenum = "100"
                    self.teletext.subpage = "01"
                self.home()
            case "de":
                try:
                    if self.teletext.nextPage != None:
                        self.teletext.pagenum = self.teletext.nextPage
                        self.teletext.subpage = "1"
                        self.teletext.getPage()
                except:
                    self.teletext.pagenum = "100"
                    self.teletext.subpage = "1"
                self.home()
            case "it":
                try:
                    if self.teletext.nextPage != None:
                        self.teletext.pagenum = self.teletext.nextPage
                        self.teletext.subpage = "1"
                        self.teletext.getPage()
                except:
                    self.teletext.pagenum = "100"
                    self.teletext.subpage = "1"
                self.home()
            case "se":
                try:
                    if self.teletext.nextPage != None:
                        self.teletext.pagenum = self.teletext.nextPage
                        self.teletext.subpage = "1"
                        self.teletext.getPage()
                except:
                    self.teletext.pagenum = "100"
                    self.teletext.subpage = "1"
                self.home()
            case "ch":
                try:
                    if self.teletext.nextPage != None:
                        self.teletext.pagenum = self.teletext.nextPage
                        self.teletext.subpage = "1"
                        self.teletext.getPage()
                except:
                    self.teletext.pagenum = "100"
                    self.teletext.subpage = "1"
                self.home()
            case "cz":
                try:
                    if self.teletext.nextPage != None:
                        self.teletext.pagenum = self.teletext.nextPage
                        self.teletext.subpage = "01"
                        self.teletext.getPage()
                except:
                    self.teletext.pagenum = "100"
                    self.teletext.subpage = "01"
                self.home()
            case "fi":
                try:
                    if self.teletext.nextPage != None:
                        self.teletext.pagenum = self.teletext.nextPage
                        self.teletext.subpage = "01"
                        self.teletext.getPage()
                except:
                    self.teletext.pagenum = "100"
                    self.teletext.subpage = "01"
                self.home()
            case "other":
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
        match self.country:
            case "hu":
                prevpage = self.teletext.prevPage
                if prevpage == None:
                    pass
                else:
                    self.teletext.pagenum = prevpage[0]
                    self.teletext.subpage = prevpage[1]
                    self.home()
            case "at":
                try:
                    if self.teletext.prevPage != None:
                        self.teletext.pagenum = self.teletext.prevPage
                        self.teletext.subpage = "01"
                        self.teletext.getPage()
                except:
                    self.teletext.pagenum = "100"
                    self.teletext.subpage = "01"
                self.home()
            case "de":
                try:
                    if self.teletext.prevPage != None:
                        self.teletext.pagenum = self.teletext.prevPage
                        self.teletext.subpage = "1"
                        self.teletext.getPage()
                except:
                    self.teletext.pagenum = "100"
                    self.teletext.subpage = "1"
                self.home()
            case "it":
                try:
                    if self.teletext.prevPage != None:
                        self.teletext.pagenum = self.teletext.prevPage
                        self.teletext.subpage = "1"
                        self.teletext.getPage()
                except:
                    self.teletext.pagenum = "100"
                    self.teletext.subpage = "1"
                self.home()
            case "se":
                try:
                    if self.teletext.prevPage != None:
                        self.teletext.pagenum = self.teletext.prevPage
                        self.teletext.subpage = "1"
                        self.teletext.getPage()
                except:
                    self.teletext.pagenum = "100"
                    self.teletext.subpage = "1"
                self.home()
            case "ch":
                try:
                    if self.teletext.prevPage != None:
                        self.teletext.pagenum = self.teletext.prevPage
                        self.teletext.subpage = "1"
                        self.teletext.getPage()
                except:
                    self.teletext.pagenum = "100"
                    self.teletext.subpage = "1"
                self.home()
            case "cz":
                try:
                    if self.teletext.prevPage != None:
                        self.teletext.pagenum = self.teletext.prevPage
                        self.teletext.subpage = "01"
                        self.teletext.getPage()
                except:
                    self.teletext.pagenum = "100"
                    self.teletext.subpage = "01"
                self.home()
            case "fi":
                try:
                    if self.teletext.prevPage != None:
                        self.teletext.pagenum = self.teletext.prevPage
                        self.teletext.subpage = "01"
                        self.teletext.getPage()
                except:
                    self.teletext.pagenum = "100"
                    self.teletext.subpage = "01"
                self.home()
            case "other":
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
        match self.country:
            case "hu":
                nextsubpage = self.teletext.nextSubpage
                if nextsubpage == None:
                    pass
                else:
                    self.teletext.pagenum = nextsubpage[0]
                    self.teletext.subpage = nextsubpage[1]
                    self.home()
            case "at":
                nextsubpage = int(self.teletext.subpage)+1
                if nextsubpage <= self.teletext.subpages:
                    self.teletext.subpage = f"{nextsubpage:02d}"
                    self.home()
            case "de":
                nextsubpage = int(self.teletext.subpage)+1
                if nextsubpage <= self.teletext.subpages:
                    self.teletext.subpage = f"{nextsubpage:02d}"
                    self.home()
            case "it":
                nextsubpage = int(self.teletext.subpage)+1
                if nextsubpage <= self.teletext.subpages:
                    self.teletext.subpage = f"{nextsubpage}"
                    self.home()
            case "se":
                nextsubpage = int(self.teletext.subpage)+1
                if nextsubpage <= self.teletext.subpages:
                    self.teletext.subpage = f"{nextsubpage:02d}"
                    self.home()
            case "ch":
                nextsubpage = int(self.teletext.subpage)+1
                if nextsubpage <= self.teletext.subpages:
                    self.teletext.subpage = f"{nextsubpage:02d}"
                    self.home()
            case "cz":
                nextsubpage = int(self.teletext.subpage)+1
                if nextsubpage <= self.teletext.subpages:
                    self.teletext.subpage = f"{nextsubpage:02d}"
                    self.home()
            case "fi":
                nextsubpage = int(self.teletext.subpage)+1
                if nextsubpage <= self.teletext.subpages:
                    self.teletext.subpage = f"{nextsubpage:02d}"
                    self.home()
            case "other":
                nextsubpage = int(self.teletext.subpage)+1
                if nextsubpage <= self.teletext.subpages:
                    self.teletext.subpage = f"{nextsubpage:02d}"
                    self.home()
    def prevsubPage(self, *args, **kwargs):
        match self.country:
            case "hu":
                prevsubpage = self.teletext.prevSubpage
                if prevsubpage == None:
                    pass
                else:
                    self.teletext.pagenum = prevsubpage[0]
                    self.teletext.subpage = prevsubpage[1]
                    self.home()
            case "at":
                prevsubpage = int(self.teletext.subpage)-1
                if prevsubpage >= 1:
                    self.teletext.subpage = f"{prevsubpage:02d}"
                    self.home()
            case "de":
                prevsubpage = int(self.teletext.subpage)-1
                if prevsubpage >= 1:
                    self.teletext.subpage = f"{prevsubpage:02d}"
                    self.home()
            case "it":
                prevsubpage = int(self.teletext.subpage)-1
                if prevsubpage >= 1:
                    self.teletext.subpage = f"{prevsubpage}"
                    self.home()
            case "se":
                prevsubpage = int(self.teletext.subpage)-1
                if prevsubpage >= 1:
                    self.teletext.subpage = f"{prevsubpage:02d}"
                    self.home()
            case "ch":
                prevsubpage = int(self.teletext.subpage)-1
                if prevsubpage >= 1:
                    self.teletext.subpage = f"{prevsubpage:02d}"
                    self.home()
            case "cz":
                prevsubpage = int(self.teletext.subpage)-1
                if prevsubpage >= 1:
                    self.teletext.subpage = f"{prevsubpage:02d}"
                    self.home()
            case "fi":
                prevsubpage = int(self.teletext.subpage)-1
                if prevsubpage >= 1:
                    self.teletext.subpage = f"{prevsubpage:02d}"
                    self.home()
            case "other":
                prevsubpage = int(self.teletext.subpage)-1
                if prevsubpage >= 1:
                    self.teletext.subpage = f"{prevsubpage:02d}"
                    self.home()
    def redbuttonHandler(self, *args, **kwargs):
        self.teletext.pagenum = self.teletext.colorbuttons[0][0]
        self.teletext.subpage = self.teletext.colorbuttons[0][1]
        self.home()

    def greenbuttonHandler(self, *args, **kwargs):
        self.teletext.pagenum = self.teletext.colorbuttons[1][0]
        self.teletext.subpage = self.teletext.colorbuttons[1][1]
        self.home()

    def yellowbuttonHandler(self, *args, **kwargs):
        self.teletext.pagenum = self.teletext.colorbuttons[2][0]
        self.teletext.subpage = self.teletext.colorbuttons[2][1]
        self.home()

    def bluebuttonHandler(self, *args, **kwargs):
        self.teletext.pagenum = self.teletext.colorbuttons[3][0]
        self.teletext.subpage = self.teletext.colorbuttons[3][1]
        self.home()
    
    def collapse(self, *args, **kwargs):
        self.window.set_collapsed(not self.window.get_collapsed())
        # if self.window.get_collapsed:
        #     self.window.set_collapsed(False)
        # else:
        #     self.window.set_collapsed(True)

    def countrySelect(self, *args, **kwargs):
        match args[0].get_child().get_text():
            case "🇭🇺 Hungary":
                self.country = "hu"
                self.init()
                self.home()
            case "🇦🇹 Austria":
                self.country = "at"
                self.init()
                self.home()
            case "🇩🇪 Germany":
                self.country = "de"
                self.init()
                self.home()
            case "🇮🇹 Italy (slow)":
                self.country = "it"
                self.init()
                self.home()
            case "🇸🇪 Sweden":
                self.country = "se"
                self.init()
                self.home()
            case "🇨🇭 Switzerland":
                self.country = "ch"
                self.init()
                self.home()
            case "🇨🇿 Czechia":
                self.country = "cz"
                self.init()
                self.home()
            case "🇫🇮 Finland":
                self.country = "fi"
                self.init()
                self.home()
            case "🇧🇺 Other":
                self.country = "other"
                self.init()
                self.home()
    
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
        result = re.search('^.*\((.*)\)', selected)

        if self.teletext.stationid != result.group(1):
            self.teletext.stationid = result.group(1)
            self.teletext.subpage = "01"
            self.teletext.pagenum = "100"
            self.home()

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
