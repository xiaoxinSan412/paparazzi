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


def find_and_add(source, target, search):
    temp = source.getroot().findall(search)
    if temp == None:
        return
    target.extend(temp)

def find_and_add_sections_with_name(source, target, find_name):
    for block in source.getroot():
        name = block.get("name")
        if name == find_name:
            target.append(block)



def reorganize_airframe_xml(airframe_xml):
    airframe = ET.fromstring("<!DOCTYPE airframe SYSTEM \"airframe.dtd\"><!-- \n\tAirframe comment \n--> <airframe/>")
    child1 = ET.Comment("+-+-+-+-+-+-+- FIRMWARES -+-+-+-+-+-+-+")
    airframe.append(child1)

    find_and_add(airframe_xml, airframe, "firmware")

    airframe.append(ET.Comment("+-+-+-+-+-+-+-  MODULES  -+-+-+-+-+-+-+"))
    find_and_add(airframe_xml, airframe, "modules")

    airframe.append(ET.Comment("+-+-+-+-+-+-+- ACTUATORS -+-+-+-+-+-+-+"))
    find_and_add(airframe_xml, airframe, "servos")
    find_and_add(airframe_xml, airframe, "commands")
    find_and_add(airframe_xml, airframe, "rc_commands")
    find_and_add_sections_with_name(airframe_xml,airframe,"SERVO_MIXER_GAINS")
    find_and_add(airframe_xml, airframe, "command_laws")
    find_and_add_sections_with_name(airframe_xml,airframe,"FAILSAFE")

    airframe.append(ET.Comment("+-+-+-+-+-+-+-  SENSORS  -+-+-+-+-+-+-+"))
    find_and_add_sections_with_name(airframe_xml,airframe,"ADC")
    find_and_add_sections_with_name(airframe_xml,airframe,"INS")
    find_and_add_sections_with_name(airframe_xml,airframe,"AHRS")
    find_and_add_sections_with_name(airframe_xml,airframe,"XSENS")

    airframe.append(ET.Comment("+-+-+-+-+-+-+-   GAINS   -+-+-+-+-+-+-+"))
    find_and_add_sections_with_name(airframe_xml,airframe,"HORIZONTAL CONTROL")
    find_and_add_sections_with_name(airframe_xml,airframe,"VERTICAL CONTROL")
    find_and_add_sections_with_name(airframe_xml,airframe,"AGGRESSIVE")


    airframe.append(ET.Comment("+-+-+-+-+-+-+-   MISC    -+-+-+-+-+-+-+"))

    for block in airframe_xml.getroot():
        name = block.get("name")
        if name == None:
            name = "None"
        if (block.tag == "firmware"):
            print("firmware",block.tag, name)
        elif (block.tag in ["servos", "commands", "rc_commands", "command_laws"]):
            print("actuator",block.tag, name)
        else:
            print("other",block.tag, name)
            airframe.append(block)


    indent(airframe)
    #print(etree.tostring(airframe))
    ET.ElementTree(airframe).write('test.xml',pretty_print=True)










if __name__ == '__main__':
    print(paparazzi.home_dir)
    reorganize_airframe_xml(ET.fromstring("<!DOCTYPE airframe SYSTEM \"airframe.dtd\"><!-- \n\tAirframe comment \n--> <airframe/>"))

    print("test")
