import os
def main():
    try:
        from .window import MyApp
        import gi
        gi.require_version('Gtk', '4.0')
        gi.require_version('Adw', '1')
        gi.require_version("WebKit", "6.0")
        from gi.repository import Gtk, Gdk, Adw, Gio, GdkPixbuf, WebKit, GLib
    except:
        print("Couldn't find GTK/libadwaita, installing...")
        current_distro = distro.id()
        match current_distro:
            case "arch":
                os.system("sudo pacman -Sy python-gobject gtk4 libadwaita")
            case "opensuse":
                os.system("sudo zypper install python3-devel python3-gobject python3-gobject-Gdk typelib-1_0-Gtk-4_0 libgtk-4-1 libadwaita")
            case "fedora":
                os.system("sudo dnf install python3-gobject gtk4 libadwaita")
            case "ubuntu":
                os.system("sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 libadwaita-1")
            case "debian":
                os.system("sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 libadwaita-1")
            case "chromeos":
                print("You need to install https://github.com/chromebrew/chromebrew and run 'crew install gcc cairo gobject_introspection gtk4 libadwaita'")
                exit() 
            case "chrome":
                print("You need to install https://github.com/chromebrew/chromebrew and run 'crew install gcc cairo gobject_introspection gtk4 libadwaita'")
                exit()
            case "chromium":
                print("You need to install https://github.com/chromebrew/chromebrew and run 'crew install gcc cairo gobject_introspection gtk4 libadwaita'")
                exit()
            case "chromiumos":
                print("You need to install https://github.com/chromebrew/chromebrew and run 'crew install gcc cairo gobject_introspection gtk4 libadwaita'")
                exit()
            case "darwin":
                print("You need to install https://brew.sh and run 'brew install pygobject3 gtk4 libadwaita'")
                exit()
            case "macos":
                print("You need to install https://brew.sh and run 'brew install pygobject3 gtk4 libadwaita'")
                exit()
        from .window import MyApp
    app = MyApp(application_id="xyz.zsobix.teletext")
    app.run()

if __name__ == "__main__":
    main()