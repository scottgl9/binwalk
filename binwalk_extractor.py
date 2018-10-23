#!/usr/bin/python3
import binwalk
import os
import sys
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action='store', dest='filename',
                        default='filename.bin',
                        help='filename of firmware to analyze')

    results = parser.parse_args()

    for module in binwalk.scan(results.filename, signature=True, quiet=True):
        for result in module.results:
            print ("\t%s %s %s  offset=0x%.8X size=%d   %s" % (result.file.path, result.module, result.name, result.offset, result.size, result.description))
            #if result.offset in module.extractor.output[result.file.path].carved.keys(): #.has_key(result.offset):
            #    print("Carved data from offset 0x%X to %s" % (result.offset, module.extractor.output[result.file.path].carved[result.offset]))
            #if result.offset in module.extractor.output[result.file.path].extracted.keys(): #has_key(result.offset):
            #    print("Extracted %d files from offset 0x%X to '%s' using '%s'" % (len(module.extractor.output[result.file.path].extracted[result.offset]),
            #                                                                      result.offset,
            #                                                                      module.extractor.output[result.file.path].extracted[result.offset],
            #                                                                      module.extractor.output[result.file.path].carved))

