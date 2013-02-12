#!/usr/bin/env python

from __future__ import print_function

import glob

from collections import namedtuple
from os import path, getenv

import lxml.etree as ET

# if home_dir not set, then assume the tree containing this
# file is a reasonable substitute
home_dir = getenv("home_dir", path.normpath(path.join(
                        path.dirname(path.abspath(__file__)),
                        '../../../')))

# Directories
firmwares_dir = path.join(home_dir, "conf/firmwares/")
modules_dir   = path.join(home_dir, "conf/modules/")
airframes_dir = path.join(home_dir, "conf/airframes/")

# Structures
PprzModule = namedtuple("PprzModule", "description defines configures")

# List Of Stuff
def get_list_of_files(directory, extension):
    mylist = glob.glob( path.join( directory, "*" + extension) )
    mylist.sort()
    ret = []
    for it in mylist:
        ret.append( it.replace(directory,"").replace(extension, "") )
    return ret

def get_list_of_modules():
    return get_list_of_files( modules_dir, ".xml" )
    
def get_list_of_firmwares():
    return get_list_of_files( firmwares_dir, ".makefile" )

def get_list_of_subsystems(firmware):
    subsys_dir = path.join( firmwares_dir, "subsystems/" + firmware + "/" )
    # \todo how about shared
    #subsys_dir = path.join( firmwares_dir, "subsystems/shared/" )
    return get_list_of_files( subsys_dir, ".makefile" )

def get_list_of_servo_drivers():
    # \todo where do we know this?
    return ["Ppm", "Asctec", "Scilab"]

def get_module_information(module_name):
    str_desc = ""
    lst_def = []
    lst_conf = []
    try:
        xml = ET.parse(path.join(modules_dir, module_name + ".xml"))
        root = xml.getroot().find("doc")
        str_desc = root.find("description").text
        for block in root.iter("define"):
            lst_def.append([block.get("name"), block.get("value"), block.get("unit"), block.get("description")])
        for block in root.iter("configure"):
            lst_conf.append([block.get("name"), block.get("value"), block.get("unit"), block.get("description")])
    except (IOError, ET.XMLSyntaxError) as e:
        print(e.__str__())

    return PprzModule(description=str_desc, defines=lst_def, configures=lst_conf)

