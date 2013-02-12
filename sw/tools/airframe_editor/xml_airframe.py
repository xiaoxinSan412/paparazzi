#!/usr/bin/env python

from __future__ import print_function

import lxml.etree as ET
import xml_common
import paparazzi


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


    xml_common.indent(airframe)
    #print(etree.tostring(airframe))
    ET.ElementTree(airframe).write('test.xml',pretty_print=True)

def load(airframe_file, tree):
    try:
        my_xml = ET.parse(airframe_file)
        root = my_xml.getroot()

        tree.clear()
        for block in root:
            name = block.get("name")
            if name == None:
                name = ""
            
            print(block.tag.__str__() + " " + name)
            piter = tree.append(None, [ block.tag.__str__() + " " + name ])
            for elem in block:
                ename = elem.get("name")
                if ename == None:
                    ename = ""
                tree.append(piter, [ elem.tag.__str__() + " " + ename ])
        return [None, my_xml]
    except (IOError, ET.XMLSyntaxError, ET.XMLSyntaxError) as e:
        return [e, my_xml]





if __name__ == '__main__':
    import sys
    if (len(sys.argv) > 1):
        airframe_file = sys.argv[1]
        airframe = ET.parse(airframe_file)
    else:
        airframe = ET.fromstring("<!DOCTYPE airframe SYSTEM \"airframe.dtd\"><!-- \n\tAirframe comment \n--> <airframe/>")
    reorganize_airframe_xml(airframe)
