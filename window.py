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
        self.set_default_size(600, 250)
        self.set_title("Lidl Plus on Desktop")
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

    def home(self, *args, **kwargs):
        print(self.teletext.getPageGif)
        print(self.teletext.nextPage)

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
