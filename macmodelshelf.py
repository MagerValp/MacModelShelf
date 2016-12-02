#!/usr/bin/env python


import sys
import os
import argparse
import shelve
import urllib2
from xml.etree import ElementTree
import re


DBPATH = "macmodelshelf"


def print8(*args):
    print " ".join(unicode(x).encode(u"utf-8") for x in args)

def printerr8(*args):
    print >>sys.stderr, " ".join(unicode(x).encode(u"utf-8") for x in args)


try:
    macmodelshelf = shelve.open(DBPATH)
except BaseException, e:
    printerr8(u"Couldn't open macmodelshelf.db: %s" % unicode(e))
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
    

CLEANUP_RES = [
    (re.compile(ur"inch ? "), u"inch, "),
    (re.compile(ur"  "), u" "),
]
def cleanup_model(model):
    for pattern, replacement in CLEANUP_RES:
        model = pattern.sub(replacement, model)
    return model
    

def model(code, cleanup=True):
    global macmodelshelf
    if code == None:
        return None
    code = code.upper()
    try:
        model = macmodelshelf[code]
    except KeyError:
        printerr8(u"Looking up %s from Apple" % code)
        model = lookup_mac_model_code_from_apple(code)
        if model:
            macmodelshelf[code] = model
    if cleanup and model:
        return cleanup_model(model)
    else:
        return model
    

def _dump(cleanup=True):
    def clean(model):
        if cleanup:
            return cleanup_model(model)
        else:
            return model
    items = macmodelshelf.keys()
    items.sort()
    items.sort(key=len)
    print8(u"macmodelshelfdump = {")
    print8(u",\n".join([u'    "%s": "%s"' % (code, clean(macmodelshelf[code])) for code in items]))
    print8(u"}")


def main(argv):   
    p = argparse.ArgumentParser()
    p.add_argument(u"-n", u"--no-cleanup", action=u"store_false",
                   dest=u"cleanup", help=u"Don't clean up model strings.")
    p.add_argument(u"code", help=u"Serial number or model code")
    args = p.parse_args([x.decode(u"utf-8") for x in argv[1:]])
    
    if args.code == u"dump":
        _dump(args.cleanup)
        return 0
    
    if len(args.code) in (11, 12, 13):
        m = model(model_code(args.code), cleanup=args.cleanup)
    else:
        m = model(args.code, cleanup=args.cleanup)
    if m:
        print m
        return 0
    else:
        printerr8(u"Unknown model %s" % repr(args.code))
        return os.EX_UNAVAILABLE


if __name__ == '__main__':
    sys.exit(main(sys.argv))
