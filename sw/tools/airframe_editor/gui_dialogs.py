#!/usr/bin/env python

from __future__ import print_function

import pygtk, gtk
from os import path


if gtk.pygtk_version < (2,3,90):
    print("Please upgrade your pygtk")
    raise SystemExit


def filechooser(pathname):
    dialog = gtk.FileChooserDialog( "Open ...", None,
        gtk.FILE_CHOOSER_ACTION_OPEN,
        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
        gtk.STOCK_OPEN, gtk.RESPONSE_OK))

    dialog.set_default_response(gtk.RESPONSE_OK)
    dialog.set_current_folder(pathname)

    filter = gtk.FileFilter()
    filter.set_name("Airframe File")
    filter.add_pattern("*.xml")
    dialog.add_filter(filter)

    response = dialog.run()
    filename = ""
    if response == gtk.RESPONSE_OK:
        filename = dialog.get_filename()
    elif response == gtk.RESPONSE_CANCEL:
        print("No file selected")

    dialog.destroy()
    return filename

def error_loading_xml(str):
    err_msg = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT,
        gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE,
        "Error Loading XML: " + str )
    err_msg.run()
    err_msg.destroy()


def about(home):
    about = gtk.AboutDialog();
    about.set_program_name("Paparazzi Airframe Editor")
    about.set_version("0.1")
    about.set_copyright("(c) GPL v2")
    about.set_comments("Airframe Editor")
    about.set_website("http://paparazzi.github.com/")
    about.set_logo(gtk.gdk.pixbuf_new_from_file(path.join(home, "data/pictures/penguin_icon.png")))
    about.run()
    about.destroy()

