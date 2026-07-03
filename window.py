from main import *

import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk, Adw, Gio, GdkPixbuf


css_provider = Gtk.CssProvider()
css_provider.load_from_string("""
.margin {
    margin: 15px;
}
.image {
    margin-left: 30px;
    margin-right: 30px;
    border-radius: 10px;
}
.nav {
    margin-top: 30px;
    margin-bottom: 31px;
}
.redbutton {
    margin-left: 40px;
    margin-right: 120px;
    background-color: red;
    border-radius: 20px;
}
.greenbutton {
    margin-right: 100px;
    background-color: lime;
    border-radius: 20px;
}
.yellowbutton {
    margin-right: 100px;
    background-color: yellow;
    border-radius: 20px;
}
.bluebutton {
    margin-left: 20px;
    margin-right: 40px;
    background-color: blue;
    border-radius: 20px;
}
""")
Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(580, 685)
        self.set_title("Teletext")
        self.titlebar = Gtk.HeaderBar()
        self.set_titlebar(self.titlebar)
        self.country = "hu"
        
        action = Gio.SimpleAction.new("home", None)
        action.connect("activate", self.home)

        self.add_action(action)

        menu = Gio.Menu.new()

        menu.append("Home", "win.home")

        self.popover = Gtk.PopoverMenu()
        self.popover.set_menu_model(menu)

        self.hamburger = Gtk.MenuButton()
        self.hamburger.set_popover(self.popover)
        self.hamburger.set_icon_name("open-menu-symbolic")

        self.titlebar.pack_start(self.hamburger)

        self.homebutton = Gtk.Button()
        self.homebutton.connect("clicked", self.home)
        self.homebutton.set_icon_name("go-home-symbolic")

        self.titlebar.pack_start(self.homebutton)

        match self.country:
            case "hu":
                self.teletext = hunTeletextReader()
            case "at":
                self.teletext = atTeletextReader()
        self.home()

    def home(self, *args, **kwargs):
        self.teletext.getPage()
        self.cbox = Gtk.CenterBox()
        self.set_child(self.cbox)
        self.ccbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.cbox.set_center_widget(self.ccbox)
        img = Gio.File.new_for_uri(self.teletext.getPageGif)
        img2 = GdkPixbuf.Pixbuf.new_from_stream(img.read(cancellable=None))
        image = Gtk.Image().new_from_pixbuf(img2)
        match self.country:
            case "hu":
                self.teletext.colorbuttonsInit()
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
        backbutton.connect('clicked', self.prevPage)
        nextbutton = Gtk.Button().new_from_icon_name('go-next-symbolic')
        nextbutton.connect('clicked', self.nextPage)
        backsubbutton = Gtk.Button().new_from_icon_name('go-up-symbolic')
        backsubbutton.connect('clicked', self.prevsubPage)
        nextsubbutton = Gtk.Button().new_from_icon_name('go-down-symbolic')
        nextsubbutton.connect('clicked', self.nextsubPage)

        self.buttonsbox.append(backbutton)
        self.buttonsbox.append(backsubbutton)
        self.buttonsbox.append(nextsubbutton)
        self.buttonsbox.append(nextbutton)

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
                    self.teletext.pagenum = self.teletext.nextPage
                    self.teletext.getPage()
                except:
                    self.teletext.pagenum = "100"
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
                    self.teletext.pagenum = self.teletext.prevPage
                    self.teletext.getPage()
                except:
                    self.teletext.pagenum = "100"
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
                try:
                    nextsubpage = int(self.teletext.subpage)+1
                    if nextsubpage < self.teletext.subpages:
                        self.teletext.subpage = f"{nextsubpage:02d}"
                        self.home()
                except:
                    self.teletext.subpage = "01"
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
                try:
                    prevsubpage = int(self.teletext.subpage)-1
                    if prevsubpage >= 1:
                        self.teletext.subpage = f"{prevsubpage:02d}"
                        self.home()
                except:
                    self.teletext.subpage = "01"
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
