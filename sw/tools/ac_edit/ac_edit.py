#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

class Base:
	def process(self, widget):
		print "Button Process"

	def destroy(self, widget, data=None):
		print "You clicked close"
		gtk.main_quit()

	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_size_request(800,600)
		self.window.set_title("Paparazzi Airframe File Editor")

		self.button1 = gtk.Button("Exit")
		self.button1.connect("clicked", self.destroy)
		self.button1.set_tooltip_text("Close application")
		
		self.button2 = gtk.Button("Run")
		self.button2.connect("clicked", self.process)
		
		fixed = gtk.Fixed()
		fixed.put(self.button1, 20,20)
		fixed.put(self.button2, 80,20)

		self.window.add(fixed)
		self.window.show_all()
		self.window.connect("destroy", self.destroy)

	def main(self):
		gtk.main()

if __name__ == "__main__":
	base = Base()
	base.main()

