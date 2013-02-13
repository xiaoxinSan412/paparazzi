#!/usr/bin/env python

from __future__ import print_function

import pygtk
import gtk
pygtk.require('2.0')

from os import path

# Owm Modules
import gui_dialogs
import xml_airframe
import paparazzi


# Airframe File
airframe_file = path.join(paparazzi.airframes_dir, "CDW/classix.xml")

class AirframeEditor:

    # General Functions

    def load_airframe_xml(self):
        global airframe_file
        self.tvcolumn.set_title(airframe_file.replace(paparazzi.airframes_dir,""))
        [e, self.xml] = xml_airframe.load(airframe_file, self.treestore)
        if (e):
            gui_dialogs.error_loading_xml(e.__str__())
            raise e

    def update_combo(self,combo,list):
        combo.set_sensitive(False)
        combo.get_model().clear()
        for i in list:
            combo.append_text(i)
        combo.set_active(0)
        combo.set_sensitive(True)

    # CallBack Functions

    def find_firmwares(self, widget):
        list_of_firmwares = paparazzi.get_list_of_firmwares()
        self.update_combo(self.firmwares_combo, list_of_firmwares)
    
    def find_modules(self, widget):
        list_of_modules = paparazzi.get_list_of_modules()
        self.update_combo(self.modules_combo, list_of_modules)

    def find_subsystems(self, widget):
        list_of_subsystems = paparazzi.get_list_of_subsystems(self.firmwares_combo.get_active_text())
        self.update_combo(self.subsystems_combo,list_of_subsystems)

    def find_module_defines(self, widget):
        mod = paparazzi.get_module_information(self.modules_combo.get_active_text())
        print(mod.description)
        self.text_box.set_text(mod.description)
        #for d in mod.defines:
        #    print("define: " + d[0])
        #for c in mod.configures:
        #    print("configure: " + c[0])
        self.gridstore.clear()
        for d in mod.defines:
            self.gridstore.append( [ "define", d[0], d[1], d[2], d[3] ] )

    def process(self, widget):
        xml_airframe.reorganize_airframe_xml(self.xml)

    def textchanged(self, widget):
        self.text_box.set_text(self.textbox.get_text())

    def about(self, widget):
        gui_dialogs.about(paparazzi.home_dir)

    def open(self, widget):
        global airframe_file
        filename = gui_dialogs.filechooser(paparazzi.airframes_dir)
        if (filename == ""):
            print("No file selected")
            return
        airframe_file = filename
        self.load_airframe_xml()

    # Constructor Functions        

    def select(self, widget):
        print("Selected ",self.treeview.get_selection())

    def fill_tree_from_airframe(self):
        
        # create a TreeStore with one string column to use as the model
        self.treestore = gtk.TreeStore(str)

        # create the TreeView using treestore
        self.treeview = gtk.TreeView(self.treestore)

        # create the TreeViewColumn to display the data
        self.tvcolumn = gtk.TreeViewColumn('')

        # add self.tvcolumn to treeview
        self.treeview.append_column(self.tvcolumn)
        self.treeview.connect("cursor-changed", self.select)
        self.cell = gtk.CellRendererText()
        self.tvcolumn.pack_start(self.cell, True)
        self.tvcolumn.add_attribute(self.cell, 'text', 0)
        
    def fill_datagrid_from_section(self):
        
        # create a TreeStore with one string column to use as the model
        self.gridstore = gtk.ListStore(str, str, str, str, str)

        self.datagrid = gtk.TreeView(self.gridstore)

        self.type_column = gtk.TreeViewColumn('Type')
        self.name_column = gtk.TreeViewColumn('Name')
        self.value_column = gtk.TreeViewColumn('Value')
        self.unit_column = gtk.TreeViewColumn('Unit')
        self.desc_column = gtk.TreeViewColumn('Description')

        self.datagrid.append_column(self.type_column)
        self.datagrid.append_column(self.name_column)
        self.datagrid.append_column(self.value_column)
        self.datagrid.append_column(self.unit_column)
        self.datagrid.append_column(self.desc_column)

        self.type_cell = gtk.CellRendererText()
        self.type_cell.Editable = False
        self.name_cell = gtk.CellRendererText()
        self.name_cell.Editable = False
        self.value_cell = gtk.CellRendererText()
        self.value_cell.Editable = True
        self.unit_cell = gtk.CellRendererText()
        self.unit_cell.Editable = False
        self.desc_cell = gtk.CellRendererText()
        self.desc_cell.Editable = False

        self.type_column.pack_start(self.type_cell, True)
        self.type_column.add_attribute(self.type_cell, 'text', 0)
        self.name_column.pack_start(self.name_cell, True)
        self.name_column.add_attribute(self.name_cell, 'text', 1)
        self.value_column.pack_start(self.value_cell, True)
        self.value_column.add_attribute(self.value_cell, 'text', 2)
        self.unit_column.pack_start(self.unit_cell, True)
        self.unit_column.add_attribute(self.unit_cell, 'text', 3)
        self.desc_column.pack_start(self.desc_cell, True)
        self.desc_column.add_attribute(self.desc_cell, 'text', 4)

        self.datagrid.set_search_column(1)
        self.name_column.set_sort_column_id(0)
        self.datagrid.set_reorderable(True)


    def destroy(self, widget, data=None):
        gtk.main_quit()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_size_request(1024,800)
        self.window.set_title("Paparazzi Airframe File Editor")

        self.my_vbox = gtk.VBox()

        ##### Buttons
        self.btnExit = gtk.Button("Exit")
        self.btnExit.connect("clicked", self.destroy)
        self.btnExit.set_tooltip_text("Close application")

        self.btnOpen = gtk.Button("Open")
        self.btnOpen.connect("clicked", self.open)        

        self.btnRun = gtk.Button("Reorganize XML")
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
        self.toolbar.pack_start(self.btnOpen)
        self.toolbar.pack_start(self.btnRun)
        self.toolbar.pack_start(self.btnAbout)
        self.toolbar.pack_start(self.btnExit)

        self.my_vbox.pack_start(self.toolbar)



        self.firmwares_combo = gtk.combo_box_entry_new_text()
        self.find_firmwares(self.firmwares_combo)
        self.firmwares_combo.connect("changed", self.find_subsystems)

        self.subsystems_combo = gtk.combo_box_entry_new_text()

        self.firmwarebar = gtk.HBox()
        self.firmwarebar.pack_start(self.btnFirmwares)
        self.firmwarebar.pack_start(self.btnSubSystem)
        self.firmwarebar.pack_start(self.firmwares_combo)
        self.firmwarebar.pack_start(self.subsystems_combo)


        self.my_vbox.pack_start(self.firmwarebar)


        self.modules_combo = gtk.combo_box_entry_new_text()
        self.find_modules(self.modules_combo)
        self.modules_combo.connect("changed", self.find_module_defines)


        #self.modulebar = gtk.HBox()
        self.firmwarebar.pack_start(self.btnModules)
        self.firmwarebar.pack_start(self.btnModuleDefines)
        self.firmwarebar.pack_start(self.modules_combo)

        #self.my_vbox.pack_start(self.modulebar)




        ##### Middle

        self.editor = gtk.HBox()

        self.fill_tree_from_airframe()
        self.editor.pack_start(self.treeview)
	
        self.fill_datagrid_from_section()
        self.editor.pack_start(self.datagrid)

        self.my_vbox.pack_start(self.editor)

        self.text_box = gtk.Label("")
        self.editor.pack_start(self.text_box)

        self.load_airframe_xml()

        ##### Bottom        

        self.textbox = gtk.Entry()
        self.textbox.connect("changed",self.textchanged)
        
        self.my_vbox.pack_start(self.textbox)

        self.window.add(self.my_vbox)
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

