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
    if len(serial) in (12, 13) and serial.startswith("S"): # Remove S prefix from scanned codes.
        serial = serial[1:]
    if len(serial) in (11, 12):
        return serial[8:].decode("ascii")
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
    code = code.upper()
    try:
        model = macmodelshelf[code]
    except KeyError:
        print >>sys.stderr, "Looking up %s from Apple" % code
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
        if sys.argv[1] == "dump":
            _dump()
            sys.exit(0)
        if len(sys.argv[1]) in (11, 12, 13):
            m = model(model_code(sys.argv[1]))
        else:
            m = model(sys.argv[1])
        if m:
            print m
            sys.exit(0)
        else:
            print >>sys.stderr, "Unknown model %s" % repr(sys.argv[1])
            sys.exit(1)
    except IndexError:
        print "Usage: macmodelshelf.py serial_number"
        sys.exit(1)
