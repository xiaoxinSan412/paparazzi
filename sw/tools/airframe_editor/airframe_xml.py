#!/usr/bin/env python

from __future__ import print_function

#import xml.etree.ElementTree as ET
import lxml.etree as ET


try:
    from lxml import etree
    print("running with lxml.etree")
except ImportError:
    try:
        # Python 2.5
        import xml.etree.cElementTree as etree
        print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # Python 2.5
            import xml.etree.ElementTree as etree
            print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree
                print("running with cElementTree")
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree
                    print("running with ElementTree")
                except ImportError:
                    print("Failed to import ElementTree from any known place")

import paparazzi

def indent(elem, level=0, more_sibs=False):
    i = "\n"
    num_kids = len(elem)
    if ((level <= 1)):
        i += "\n"
    if level:
        i += (level-1) * '  '
    if num_kids:
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
            if level:
                elem.text += '  '
        count = 0
        for kid in elem:
            indent(kid, level+1, count < num_kids - 1)
            count += 1
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
            if more_sibs:
                elem.tail += '  '
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
            if more_sibs:
                elem.tail += '  '

def organize_airframe_xml():
    airframe = ET.fromstring("<!DOCTYPE airframe SYSTEM \"airframe.dtd\"><!-- \n\tAirframe comment \n--> <airframe/>")
    child1 = ET.Comment("+-+-+-+-+-+-+- FIRMWARES -+-+-+-+-+-+-+")
    airframe.append(child1)
    child2 = ET.SubElement(airframe, "firmware")
    #airframe.append(airframe_xml.getroot().find("firmware"))
    airframe.append(ET.Comment("+-+-+-+-+-+-+-  MODULES  -+-+-+-+-+-+-+"))
    child3 = ET.SubElement(airframe, "modules")
    airframe.append(ET.Comment("+-+-+-+-+-+-+- ACTUATORS -+-+-+-+-+-+-+"))
    airframe.append(ET.Comment("+-+-+-+-+-+-+-   GAINS   -+-+-+-+-+-+-+"))
    child4 = ET.SubElement(airframe, "section")
    child5 = ET.SubElement(airframe, "section")
    child6 = ET.SubElement(child4, "define")
    airframe.append(ET.Comment("+-+-+-+-+-+-+-   MISC    -+-+-+-+-+-+-+"))
    indent(airframe)
    child1.tail = "\n\n" + child1.tail
    ET.ElementTree(airframe).write('test.xml',pretty_print=True)










if __name__ == '__main__':
    print(paparazzi.home_dir)
    organize_airframe_xml()

    print("test")
