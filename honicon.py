#!/usr/bin/env python
# -*- coding: utf-8-*-
# AS-IS, Source Code under Public Domain

from sys import exit
import xml.etree.ElementTree as etree
import zipfile,os
from dds import dds2png


def main():
    try:
        import argparse
        have_argparse = True
        parser = argparse.ArgumentParser(description='HoN Icon Extract')
    except:
        import optparse
        have_argparse = False
        parser = optparse.OptionParser(description='HoN Patcher')
        parser.add_argument = parser.add_option

    parser.add_argument("-s","--hondir", dest="hondir",help="source HoN directory, otherwise - current directory")
    parser.add_argument("-d","--destdir", dest="destdir",help="icon destination directory, otherwise will extract to HoN's root dir O_O")

    options = parser.parse_args()

    destdir = '.'
    if options.destdir:
        destdir = options.destdir
    destdir = os.path.abspath(destdir)

    if not have_argparse:
        options = options[0]
    if options.hondir:
        os.chdir(options.hondir)


    resources0 = zipfile.ZipFile('game/resources0.s2z')
    textures = zipfile.ZipFile('game/textures.s2z')
    upgrades = resources0.read('base.upgrades')

    xml = etree.fromstring(upgrades)
    for e in xml:
        if e.tag == 'chatsymbol' and e.attrib['texture'].startswith('/heroes/'):
            destname = os.path.join(destdir, e.attrib['name'] + '.png')
            f = open(destname,'wb')
            try:
                f.write(dds2png(textures.open('00000000' + e.attrib['texture'][:-3] + 'dds')))
            except:
                print ( 'failed processing ' + e.attrib['name'] + ',' + e.attrib['texture'])
            f.close()




if __name__ == '__main__':
    main()

