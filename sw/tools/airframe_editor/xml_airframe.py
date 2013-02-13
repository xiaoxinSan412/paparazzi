#!/usr/bin/env python

from __future__ import print_function

import lxml.etree as ET
import StringIO

import xml_common
import paparazzi


def find_and_add(source, target, search):
    temp = source.getroot().findall("./"+search)
    for t in temp:
        xml_common.indent(t,1)
    target.extend(temp)

def find_and_add_sections_with_name(source, target, find_name):
    temp = source.getroot().findall("./*[@name='" +find_name+ "']")
    for t in temp:
        xml_common.indent(t,1)
    target.extend(temp)

def reorganize_airframe_xml(airframe_xml):
    some_file_like_object = StringIO.StringIO("<!DOCTYPE airframe SYSTEM \"airframe.dtd\">\n\n<!-- \n\tAirframe comment \n-->\n\n<airframe/>")
    airframe_xml_tree = ET.parse(some_file_like_object)
    airframe = airframe_xml_tree.getroot()
    

    child1 = ET.Comment("+-+-+-+-+-+-+- FIRMWARES -+-+-+-+-+-+-+")
    airframe.append(child1)

    find_and_add(airframe_xml, airframe, "firmware")
    find_and_add_sections_with_name(airframe_xml,airframe,"AUTOPILOT")

    airframe.append(ET.Comment("+-+-+-+-+-+-+-  MODULES  -+-+-+-+-+-+-+"))
    find_and_add(airframe_xml, airframe, "modules")

    airframe.append(ET.Comment("+-+-+-+-+-+-+- ACTUATORS -+-+-+-+-+-+-+"))
    find_and_add(airframe_xml, airframe, "servos")
    find_and_add(airframe_xml, airframe, "commands")
    find_and_add(airframe_xml, airframe, "rc_commands")
    find_and_add_sections_with_name(airframe_xml,airframe,"AUTO1")
    find_and_add_sections_with_name(airframe_xml,airframe,"SERVO_MIXER_GAINS")
    find_and_add_sections_with_name(airframe_xml,airframe,"MIXER")
    find_and_add_sections_with_name(airframe_xml,airframe,"MIXING")
    find_and_add(airframe_xml, airframe, "command_laws")
    find_and_add_sections_with_name(airframe_xml,airframe,"FAILSAFE")

    airframe.append(ET.Comment("+-+-+-+-+-+-+-  SENSORS  -+-+-+-+-+-+-+"))
    find_and_add_sections_with_name(airframe_xml,airframe,"ADC")
    find_and_add_sections_with_name(airframe_xml,airframe,"IMU")
    find_and_add_sections_with_name(airframe_xml,airframe,"AHRS")
    find_and_add_sections_with_name(airframe_xml,airframe,"INS")
    find_and_add_sections_with_name(airframe_xml,airframe,"XSENS")

    airframe.append(ET.Comment("+-+-+-+-+-+-+-   GAINS   -+-+-+-+-+-+-+"))
    # Fixedwing
    find_and_add_sections_with_name(airframe_xml,airframe,"HORIZONTAL CONTROL")
    find_and_add_sections_with_name(airframe_xml,airframe,"VERTICAL CONTROL")
    find_and_add_sections_with_name(airframe_xml,airframe,"AGGRESSIVE")
    # Rotorcraft
    find_and_add_sections_with_name(airframe_xml,airframe,"STABILIZATION_RATE")
    find_and_add_sections_with_name(airframe_xml,airframe,"STABILIZATION_ATTITUDE")
    find_and_add_sections_with_name(airframe_xml,airframe,"GUIDANCE_V")
    find_and_add_sections_with_name(airframe_xml,airframe,"GUIDANCE_H")

    airframe.append(ET.Comment("+-+-+-+-+-+-+-   MISC    -+-+-+-+-+-+-+"))

    find_and_add(airframe_xml,airframe,"*")

    xml_common.indent(airframe)

    temp = airframe.findall("./*")
    for t in temp:
        t.tail = "\n\n  "

    #print(etree.tostring(airframe))
    #ET.ElementTree(airframe_xml_tree).write('test.xml')
    return airframe_xml_tree

def load(airframe_file):
    try:
        my_xml = ET.parse(airframe_file)
        return [None, my_xml]
    except (IOError, ET.XMLSyntaxError, ET.XMLSyntaxError) as e:
        return [e, my_xml]


def fill_tree(my_xml, tree):
    root = my_xml.getroot()

    tree.clear()
    for block in root:
        if not isinstance(block, ET._Comment):
            name = block.get("name")
            if name == None:
                name = ""

            #print(block.tag.__str__() + " " + name)
            piter = tree.append(None, [ block.tag.__str__() + " " + name ])
            for elem in block:
                ename = elem.get("name")
                if ename == None:
                    ename = ""
                if not isinstance(elem, ET._Comment):
                    tree.append(piter, [ elem.tag.__str__() + " " + ename ])


if __name__ == '__main__':
    import sys
    if (len(sys.argv) > 1):
        airframe_file = sys.argv[1]
        airframe = ET.parse(airframe_file)
    else:
        [e, airframe] = load("../../../conf/airframes/CDW/classix.xml")
    xml = reorganize_airframe_xml(airframe)
    ET.ElementTree(xml.getroot()).write('test.xml')
