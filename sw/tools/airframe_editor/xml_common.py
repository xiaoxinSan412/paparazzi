#!/usr/bin/env python

from __future__ import print_function

#import xml.etree.ElementTree as ET
import lxml.etree as ET


#try:
#    from lxml import etree
#    print("running with lxml.etree")
#except ImportError:
#    try:
#        # Python 2.5
#        import xml.etree.cElementTree as etree
#        print("running with cElementTree on Python 2.5+")
#    except ImportError:
#        try:
#            # Python 2.5
#            import xml.etree.ElementTree as etree
#            print("running with ElementTree on Python 2.5+")
#        except ImportError:
#            try:
#                # normal cElementTree install
#                import cElementTree as etree
#                print("running with cElementTree")
#            except ImportError:
#                try:
#                    # normal ElementTree install
#                    import elementtree.ElementTree as etree
#                    print("running with ElementTree")
#                except ImportError:
#                    print("Failed to import ElementTree from any known place")


def indent(elem, level=0, more_sibs=False):
    i = "\n"
    num_kids = len(elem)
    if level:
        i += (level-1) * '  '
    #print(level, elem.tag, num_kids, more_sibs)
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
