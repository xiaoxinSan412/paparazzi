#!/usr/bin/env python
from __future__ import print_function

from optparse import OptionParser
#import xml.etree.ElementTree as ET
import lxml.etree as ET
#print(lxml.etree.LXML_VERSION)


import os
import sys
import glob
import re

import paparazzi

def organize_airframe_xml():
    airframe = ET.fromstring("<!DOCTYPE airframe SYSTEM \"airframe.dtd\"><!-- Airframe comment --> <airframe/>")
    airframe.append(ET.Comment("+-+-+-+-+-+-+- FIRMWARES -+-+-+-+-+-+-+"))
    child2 = ET.SubElement(airframe, "firmware")
    #airframe.append(airframe_xml.getroot().find("firmware"))
    airframe.append(ET.Comment("+-+-+-+-+-+-+-  MODULES  -+-+-+-+-+-+-+"))
    child3 = ET.SubElement(airframe, "modules")
    airframe.append(ET.Comment("+-+-+-+-+-+-+- ACTUATORS -+-+-+-+-+-+-+"))
    airframe.append(ET.Comment("+-+-+-+-+-+-+-   GAINS   -+-+-+-+-+-+-+"))
    child4 = ET.SubElement(airframe, "gains")
    airframe.append(ET.Comment("+-+-+-+-+-+-+-   MISC    -+-+-+-+-+-+-+"))
    print(ET.tostring(airframe, encoding=None, method="xml", pretty_print=True, with_tail=True,
standalone=None))
    ET.ElementTree(airframe).write('test.xml', pretty_print=True)










if __name__ == '__main__':
    print(paparazzi.home_dir)
    organize_airframe_xml()

    print("test")
