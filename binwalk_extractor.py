#!/usr/bin/python3
import binwalk
import os
import sys
import argparse
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action='store', dest='filename',
                        default='filename.bin',
                        help='filename of firmware to analyze')

    results = parser.parse_args()

    offsets = []
    descriptions = []

    for module in binwalk.scan(results.filename, signature=True, quiet=True):
        for result in module.results:
            offsets.append(result.offset)
            descriptions.append(result.description)

    with open(results.filename, "rb") as binary_file:
        data = binary_file.read()

    counter=0
    part = None

    desc = {}

    for i in range(0, len(offsets) - 2):
        o1 = offsets[i]
        o2 = offsets[i+1]
        outname="{}.bin".format(i)
        desc[outname] = { 'start': o1, 'end': o2, 'info': descriptions[i] }
        part = data[o1:o2]
        with open("{}.bin".format(i), "wb") as binary_file:
            binary_file.write(part)

    with open("info.json", "w") as f:
        f.write(json.dumps(desc))
