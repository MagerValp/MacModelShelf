#!/usr/bin/env python


import sys
import shelve
import urllib2
from xml.etree import ElementTree


DBPATH = "macmodelshelf"

try:
    macmodelshelf = shelve.open(DBPATH)
except BaseException, e:
    print >>sys.stderr, "Couldn't open macmodelshelf.db: %s" % e
    sys.exit(1)


def model_code(serial):
    if "serial" in serial.lower(): # Workaround for machines with dummy serial numbers.
        return None
    elif len(serial) in (11, 12):
        return serial[8:].decode("ascii")
    else:
        return None
    

def lookup_mac_model_code_from_apple(model_code):
    try:
        f = urllib2.urlopen("http://support-sp.apple.com/sp/product?cc=%s&lang=en_US" % model_code, timeout=2)
        et = ElementTree.parse(f)
        return et.findtext("configCode").decode("utf-8")
    except:
        return None
    

def model(code):
    global macmodelshelf
    try:
        model = macmodelshelf[code]
    except KeyError:
        model = lookup_mac_model_code_from_apple(code)
        if model:
            macmodelshelf[code] = model
    return model


def _dump():
    print "macmodelshelfdump = {"
    for code, model in sorted(macmodelshelf.items()):
        print '    "%s": "%s",' % (code, model)
    print "}"
    

if __name__ == '__main__':
    try:
        if len(sys.argv[1]) in (11, 12):
            print model(model_code(sys.argv[1]))
        else:
            print model(sys.argv[1])
    except IndexError:
        print "Usage: macmodelshelf.py serial_number"
        sys.exit(1)
