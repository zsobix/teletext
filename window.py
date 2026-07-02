from main import TeletextReader

import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk, Adw, Gio, GdkPixbuf


# css_provider = Gtk.CssProvider()
# css_provider.load_from_path("")
# Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(800, 600)
        self.set_title("Teletext")
        self.titlebar = Gtk.HeaderBar()
        self.set_titlebar(self.titlebar)
        
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

        self.teletext = TeletextReader()
        self.home()

    def home(self, *args, **kwargs):
        self.teletext.getPage()
        self.cbox = Gtk.CenterBox()
        self.set_child(self.cbox)
        self.ccbox = Gtk.CenterBox()
        self.cbox.set_center_widget(self.ccbox)

        img = Gio.File.new_for_uri(self.teletext.getPageGif)
        img2 = GdkPixbuf.Pixbuf.new_from_stream(img.read(cancellable=None))
        image = Gtk.Image().new_from_pixbuf(img2)
        image.set_pixel_size(520)
        self.ccbox.set_start_widget(image)

        self.inputbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.inputbox.set_valign(Gtk.Align.CENTER)
        self.ccbox.set_end_widget(self.inputbox)

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
            self.teletext.pagenum = text
            self.home()
    
    def nextPage(self, *args, **kwargs):
        nextpage = self.teletext.nextPage
        if nextpage == None:
            pass
        else:
            self.teletext.pagenum = nextpage[0]
            self.teletext.subpage = nextpage[1]
            self.home()

    def prevPage(self, *args, **kwargs):
        prevpage = self.teletext.prevPage
        if prevpage == None:
            pass
        else:
            self.teletext.pagenum = prevpage[0]
            self.teletext.subpage = prevpage[1]
            self.home()
    def nextsubPage(self, *args, **kwargs):
        nextsubpage = self.teletext.nextSubpage
        if nextsubpage == None:
            pass
        else:
            self.teletext.pagenum = nextsubpage[0]
            self.teletext.subpage = nextsubpage[1]
            self.home()

    def prevsubPage(self, *args, **kwargs):
        prevsubpage = self.teletext.prevSubpage
        if prevsubpage == None:
            pass
        else:
            self.teletext.pagenum = prevsubpage[0]
            self.teletext.subpage = prevsubpage[1]
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
