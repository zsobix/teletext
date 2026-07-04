from main import *

import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version("WebKit", "6.0")
from gi.repository import Gtk, Gdk, Adw, Gio, GdkPixbuf, WebKit


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
""")
Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(760, 748)
        self.set_title("Teletext")
        self.titlebar = Adw.HeaderBar()
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
        
        self.window = Adw.NavigationSplitView()
        self.set_child(self.window)
        self.content = Adw.NavigationPage(title="content")
        self.window.set_content(self.content)
        self.sidebar = Adw.NavigationPage(title="countries")
        self.window.set_sidebar(self.sidebar)

        self.window.set_collapsed(True)
        self.window.set_show_content(True)

        self.sidebox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.sidebar.set_child(self.sidebox)

        hungary = Gtk.Button()
        hungary.connect('clicked', self.countrySelect)
        huntitle = Gtk.Label()
        huntitle.set_markup('<span size="x-large">🇭🇺 Hungary</span>')
        hungary.set_child(huntitle)
        hungary.set_css_classes(["countrybutton"])
        self.sidebox.append(hungary)

        austria = Gtk.Button()
        austria.connect('clicked', self.countrySelect)
        attitle = Gtk.Label()
        attitle.set_markup('<span size="x-large">🇦🇹 Austria</span>')
        austria.set_child(attitle)
        austria.set_css_classes(["countrybutton"])
        self.sidebox.append(austria)

        germany = Gtk.Button()
        germany.connect('clicked', self.countrySelect)
        gertitle = Gtk.Label()
        gertitle.set_markup('<span size="x-large">🇩🇪 Germany</span>')
        germany.set_child(gertitle)
        germany.set_css_classes(["countrybutton"])
        self.sidebox.append(germany)

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
        inputbuf.set_text(self.teletext.pagenum, -1)

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
                self.stations = ["orf1", "orf2", "orfiii", "sportplus"]
            case "de":
                self.stations = ["zdf", "zdfneo", "zdfinfo", "3sat"]
        togglegroup = Adw.ToggleGroup()
        togglegroup.set_css_classes(["flat", "round"])
        for station in self.stations:
            toggle = Adw.Toggle()
            label = Gtk.Label()
            label.set_markup(f'<span>{station.upper()}</span>')
            toggle.set_child(label)
            toggle.connect('notify', self.stationSwitcher)
            if station == self.teletext.stationid:
                togglegroup.set_active(self.stations.index(station))
            togglegroup.add(toggle)
        self.inputbox.append(togglegroup)

        

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
    
    def init(self, *args, **kwargs):
        match self.country:
            case "hu":
                self.teletext = hunTeletextReader()
            case "at":
                self.teletext = atTeletextReader()
            case "de":
                self.teletext = gerTeletextReader()

    def stationSwitcher(self, *args, **kwargs):
        print(args)
        print(kwargs)

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

if __name__ == "__main__":
    app = MyApp(application_id="xyz.zsobix.lidlplusui")
    app.run()
