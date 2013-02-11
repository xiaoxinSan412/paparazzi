#!/usr/bin/env python

PAPARAZZI_HOME = "../../../"


import pygtk
pygtk.require('2.0')
import gtk
import glob

from lxml import etree
#from elementtree.ElementTree import parse

class Base:
	def process(self, widget):
		print "Button Process"
		list_of_firmwares = glob.glob( PAPARAZZI_HOME + "conf/firmwares/*.makefile" )
		for firm in list_of_firmwares:
			print firm.replace(".makefile","").replace(PAPARAZZI_HOME + "conf/firmwares/", "")
		for firm in list_of_firmwares:
			self.combo.append_text( firm.replace(".makefile","").replace(PAPARAZZI_HOME + "conf/firmwares/", "") )
		
		try:
			tree = etree.parse(  PAPARAZZI_HOME + "conf/airframes/CDW/classix.xml")
			root = tree.getroot()
			self.label1.set_text(root.tag)
		except (IOError, etree.XMLSyntaxError) :
			self.error()
		#elem = tree.getroot()

	def combo_changed(self, widget):
		print "Changed Combo"
		self.textbox.set_text(widget.get_active_text())
		

	def textchanged(self, widget):
		self.label1.set_text(self.textbox.get_text())

	def about(self, widget):
		about = gtk.AboutDialog();
		about.set_program_name("Paparazzi Airframe Editor")
		about.set_version("0.1")
		about.set_copyright("(c) GPL v2")
		about.set_comments("Airframe Editor")
		about.set_website("http://paparazzi.github.com/")
		about.set_logo(gtk.gdk.pixbuf_new_from_file("../../../data/pictures/penguin_icon.png"))
		about.run()
		about.destroy()

	def error(self):
		err_msg = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT,
			gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE,
			"Error Loading XML" )
		err_msg.run()
		err_msg.destroy()

	def destroy(self, widget, data=None):
		print "You clicked close"
		gtk.main_quit()

	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		# self.window.set_size_request(800,600)
		self.window.set_title("Paparazzi Airframe File Editor")

		self.btnExit = gtk.Button("Exit")
		self.btnExit.connect("clicked", self.destroy)
		self.btnExit.set_tooltip_text("Close application")
		
		self.btnRun = gtk.Button("Run")
		self.btnRun.connect("clicked", self.process)

		self.btnAbout = gtk.Button("About")
		self.btnAbout.connect("clicked", self.about)

		self.toolbar = gtk.HBox()
		self.toolbar.pack_start(self.btnRun)
		self.toolbar.pack_start(self.btnAbout)
		self.toolbar.pack_start(self.btnExit)

		self.combo = gtk.combo_box_entry_new_text()
		self.combo.append_text("Entry 1")
		self.combo.append_text("Entry 2")
		self.combo.connect("changed", self.combo_changed)

		self.label1 = gtk.Label("")

		self.textbox = gtk.Entry()
		self.textbox.connect("changed",self.textchanged)
		
		self.box1 = gtk.VBox()
		self.box1.pack_start(self.toolbar)
		self.box1.pack_start(self.label1)
		self.box1.pack_start(self.textbox)
		self.box1.pack_start(self.combo)

		self.window.add(self.box1)
		self.window.show_all()
		self.window.connect("destroy", self.destroy)

	def main(self):
		gtk.main()

if __name__ == "__main__":
	base = Base()
	base.main()

