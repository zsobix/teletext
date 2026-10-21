# TeleReader

A desktop UI for some Teletext services, written in Python using GTK and libadwaita.

<img width="861" height="758" alt="260713_00h08m21s_screenshot" src="https://github.com/user-attachments/assets/10bb5703-ca7d-47a2-89f2-992a8a0cf608" />


## Installation
> This only works on Linux, because I can't package on Windows, and GTK doesn't work as well there


### Download from releases
Just download the flatpak package and install!

Install with:
```bash
flatpak install xyz.zsobix.teletext.flatpak
```

**OR**

### Download from PyPI

> You have to follow [this guide](https://pygobject.gnome.org/getting_started.html) first before running this command, so this method is **NOT recommended**

```bash
pip install teletext
```

## Usage

If you downloaded it from the releases, just run the app and enjoy!

(you may need to run it with: )
```bash
flatpak run xyz.zsobix.teletext
```

**OR**

If you downloaded it from PyPI (and followed the instructions), just run:
```bash
teletext
```

### Features

- Displaying teletext pages
- Favorites page
- Sidebar to change countries/teletext channels
- About page


## Challenges?

hmm

i feel this is very unreadme like but my hand was forced.

The hardest thing was working around weird html, sometimes HTM pages.

I don't understand why APIs aren't universal.

Like, WHY do i have to scrape websites to get just a basic SUBPAGE NUMBER.

Not in the case of ZDF, ARD, and NOS, but other than those they had actual pre rendered pages, which i can access when i just substitute the pagenumbers and subpage numbers and make a get request.

Also there were some services, with FUNCTIONAL APIs, but they provided base64 images, instead of just a link, which is good, but it was a bit harder to implement.

(more included in the open letter)

## Open letter to the devs of ZDF, ARD, and NOS

(this part is just me rambling btw)

Dear ZDF, ARD, and NOS, honestly just stop.

I had gotten brain damage from trying to implement your teletext services into my project

i dont know how you guys do this but this is insane.

I fully understand that this isnt intented behaivor, but cmon, atleast include a pre-rendered IMAGE!!!!!!!

I DONT WANT TEXT!!!!!!! I WANT IMAGES!!!!!!! just because:

- I dont have to use WebKitGTK (slow af)
- I get to just use the Gtk.Image function!!!!
- sometimes, I HAVE TO MAKE HTML PAGES BY HAND!!! then write them into tmp -> then i can display them, atleast ZDF has a page-only site, not like YOU, NOS.

sincerely, 

my braincells

## Issues
there are bugs I probably didn't notice, so pls write in the issues tab!
 

<img width="200" height="150" alt="Under_construction_graphic" src="https://github.com/user-attachments/assets/0f814f2d-37bc-446a-bf9b-7207ccdddbc5" />

## Credits

- myself for making this
- teletext services for making garbage apis
- ted for doing ted talks
- [Hack Club](https://hackclub.com) for making [Stardance!](https://stardance.hackclub.com)

please rate my project good pls

[THE ISSUE with writing readmes](THEISSUE.md)
