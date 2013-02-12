#!/usr/bin/env python

from __future__ import print_function

import pygtk
import gtk
pygtk.require('2.0')

from os import path, getenv

from lxml import etree
#lxml.require('1.3.4')

# Owm Modules
import gui_dialogs
import airframe_xml
import paparazzi


# Airframe File
airframe_file = path.join(paparazzi.airframes_dir, "CDW/classix.xml")

class AirframeEditor:

    def load_airframe_xml(self):
        try:
            self.airframe_xml = etree.parse(airframe_file)
            root = self.airframe_xml.getroot()
            etree.SubElement(root, "test" )
        except (IOError, etree.XMLSyntaxError, etree.XMLSyntaxError) as e:
            gui_dialogs.error_loading_xml(e.__str__())
            raise e

    def update_combo(self,list):
        self.combo.get_model().clear()
        for i in list:
            self.combo.append_text(i)
        self.combo.set_active(0)
   

    def find_firmwares(self, widget):
        list_of_firmwares = paparazzi.get_list_of_firmwares()
        self.update_combo(list_of_firmwares)
    
    def find_modules(self, widget):
        list_of_modules = paparazzi.get_list_of_modules()
        self.update_combo(list_of_modules)

    def find_subsystems(self, widget):
        list_of_subsystems = paparazzi.get_list_of_subsystems(self.combo.get_active_text())
        self.update_combo(list_of_subsystems)

    def find_module_defines(self, widget):
        mod = paparazzi.get_module_information(self.combo.get_active_text())
        print(mod.description)
        for d in mod.defines:
            print("define: " + d[0])
        for c in mod.configures:
            print("configure: " + c[0])

    def process(self, widget):
        print(etree.tostring(self.airframe_xml, pretty_print=True))
        self.organize_airframe_xml()

    def combo_changed(self, widget):
        print("Changed Combo")
        self.textbox.set_text(widget.get_active_text())

    def textchanged(self, widget):
        self.label1.set_text(self.textbox.get_text())

    def about(self, widget):
        gui_dialogs.about(paparazzi_home)

    def fill_tree_from_airframe(self):
        
        # create a TreeStore with one string column to use as the model
        self.treestore = gtk.TreeStore(str,str)

        # Load the File
        try:
            root = self.airframe_xml.getroot()
            for block in root:
                name = block.get("name")
                if name == None:
                    name = "None"
                
                piter = self.treestore.append(None, [ name, block.tag ])
                for elem in block:
  	            ename = elem.get("name")
	            if ename == None:
	                ename = "None"
	        
    	            self.treestore.append(piter, [ ename, elem.tag ])

                    #self.treestore.append(piter, [ att , block.get(att) ])

        except (IOError, etree.XMLSyntaxError) :
            self.error()


        # create the TreeView using treestore
        self.treeview = gtk.TreeView(self.treestore)

        # create the TreeViewColumn to display the data
        self.tvcolumn = gtk.TreeViewColumn('Airframe.xml')

        # add tvcolumn to treeview
        self.treeview.append_column(self.tvcolumn)

        # create a CellRendererText to render the data
        self.cell = gtk.CellRendererText()

        # add the cell to the tvcolumn and allow it to expand
        self.tvcolumn.pack_start(self.cell, True)

        # set the cell "text" attribute to column 0 - retrieve text
        # from that column in treestore
        self.tvcolumn.add_attribute(self.cell, 'text', 0)

        # make it searchable
        self.treeview.set_search_column(0)

        # Allow sorting on the column
        # self.tvcolumn.set_sort_column_id(0)

        # Allow drag and drop reordering of rows
        # self.treeview.set_reorderable(True)
        
    def fill_datagrid_from_section(self):
        
        # create a TreeStore with one string column to use as the model
        self.gridstore = gtk.ListStore(str, str, str)

        self.gridstore.append( ["HEIGHT_MIN", "40", "m" ] )
        self.gridstore.append( ["HEIGHT_MAX", "300", "m" ] )
        self.gridstore.append( ["RADIUS_MIN", "70", "m" ] )

        self.datagrid = gtk.TreeView(self.gridstore)

        self.name_column = gtk.TreeViewColumn('Name')
        self.value_column = gtk.TreeViewColumn('Value')
        self.unit_column = gtk.TreeViewColumn('Unit')

        self.datagrid.append_column(self.name_column)
        self.datagrid.append_column(self.value_column)
        self.datagrid.append_column(self.unit_column)

        self.cell2 = gtk.CellRendererText()
	self.cell2.Editable = True
        self.cell3 = gtk.CellRendererText()
	self.cell3.Editable = True

        self.name_column.pack_start(self.cell2, True)
        self.name_column.add_attribute(self.cell2, 'text', 0)

        self.value_column.pack_start(self.cell3, True)
        self.value_column.add_attribute(self.cell3, 'text', 1)

        self.datagrid.set_search_column(0)
	self.name_column.set_sort_column_id(0)
	self.datagrid.set_reorderable(True)


    def destroy(self, widget, data=None):
        gtk.main_quit()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_size_request(800,600)
        self.window.set_title("Paparazzi Airframe File Editor")

        self.box1 = gtk.VBox()

        ##### Buttons
        self.btnExit = gtk.Button("Exit")
        self.btnExit.connect("clicked", self.destroy)
        self.btnExit.set_tooltip_text("Close application")
        
        self.btnRun = gtk.Button("Run")
        self.btnRun.connect("clicked", self.process)

        self.btnFirmwares = gtk.Button("Firmwares")
        self.btnFirmwares.connect("clicked", self.find_firmwares)

        self.btnSubSystem = gtk.Button("SubSystems")
        self.btnSubSystem.connect("clicked", self.find_subsystems)

        self.btnModules = gtk.Button("Modules")
        self.btnModules.connect("clicked", self.find_modules)

        self.btnModuleDefines = gtk.Button("Define")
        self.btnModuleDefines.connect("clicked", self.find_module_defines)

        self.btnAbout = gtk.Button("About")
        self.btnAbout.connect("clicked", self.about)

        self.toolbar = gtk.HBox()
        self.toolbar.pack_start(self.btnRun)
        self.toolbar.pack_start(self.btnFirmwares)
        self.toolbar.pack_start(self.btnSubSystem)
        self.toolbar.pack_start(self.btnModules)
        self.toolbar.pack_start(self.btnModuleDefines)
        self.toolbar.pack_start(self.btnAbout)
        self.toolbar.pack_start(self.btnExit)

        self.box1.pack_start(self.toolbar)

        ##### Tree

        self.editor = gtk.HBox()

        self.load_airframe_xml()
        self.fill_tree_from_airframe()
        self.editor.pack_start(self.treeview)
	
        self.fill_datagrid_from_section()
        self.editor.pack_start(self.datagrid)

        self.box1.pack_start(self.editor)

        ##### Bottom        

        self.combo = gtk.combo_box_entry_new_text()
        self.combo.append_text("digital_cam")
        self.combo.set_active(0)
        self.combo.connect("changed", self.combo_changed)
        self.toolbar.pack_start(self.combo)

        self.label1 = gtk.Label("")

        self.textbox = gtk.Entry()
        self.textbox.connect("changed",self.textchanged)
        
        self.box1.pack_start(self.label1)
        self.box1.pack_start(self.textbox)

        self.window.add(self.box1)
        self.window.show_all()
        self.window.connect("destroy", self.destroy)

    def main(self):
        gtk.main()

if __name__ == "__main__":
    import sys
    if (len(sys.argv) > 1):
        airframe_file = sys.argv[1]
    gui = AirframeEditor()
    gui.main()

