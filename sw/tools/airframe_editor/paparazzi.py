#!/usr/bin/env python

from __future__ import print_function

import glob
from os import path, getenv

# if home_dir not set, then assume the tree containing this
# file is a reasonable substitute
home_dir = getenv("home_dir", path.normpath(path.join(
                        path.dirname(path.abspath(__file__)),
                        '../../../')))

# Directories
firmwares_dir = path.join(home_dir, "conf/firmwares/")
modules_dir   = path.join(home_dir, "conf/modules/")
airframes_dir = path.join(home_dir, "conf/airframes/")

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
    return get_list_of_files( subsys_dir, ".makefile" )


