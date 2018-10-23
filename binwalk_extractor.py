#!/usr/bin/python3
import binwalk
import os
import sys
import argparse
import json
import simplejson
import lzma

def binwalk_extract(filename, path):
    offsets = []
    descriptions = []

    print("Opening {}...".format(filename))

    for module in binwalk.scan(filename, signature=True, quiet=True):
        for result in module.results:
            offsets.append(result.offset)
            descriptions.append(result.description)

    with open(results.filename, "rb") as binary_file:
        data = binary_file.read()

    counter=0
    part = None

    desc = {}

    if not os.path.exists(path):
        os.mkdir(path)

    for i in range(0, len(offsets) - 2):
        o1 = offsets[i]
        o2 = offsets[i+1]
        ext = "bin"
        if "JPEG" in descriptions[i]:
            ext = "jpg"
        elif "LZMA" in descriptions[i]:
            ext = "7z"
        elif "DER" in descriptions[i]:
            ext = "der"
        elif "(PE)" in descriptions[i]:
            ext = "exe"
        elif "PC bitmap" in descriptions[i]:
            ext = "bmp"
        outname="{}.{}".format(i, ext)
        outpath="{}/{}".format(path, outname)
        desc[outname] = { 'start': o1, 'end': o2, 'info': descriptions[i] }
        part = data[o1:o2]
        with open(outpath, "wb") as binary_file:
            binary_file.write(part)
        if ext == "7z":
            os.system("lzcat -q -q {} > {}".format(outpath, outpath.replace(".7z", ".bin")))
            extract_path = "{}/{}".format(path, i)
            if not os.path.exists(extract_path):
                os.mkdir(extract_path)
            binwalk_extract(outpath.replace(".7z",".bin"), extract_path)
    with open(path+"/info.json", "w") as f:
        f.write(simplejson.dumps(desc, indent=4, sort_keys=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action='store', dest='filename',
                        default='filename.bin',
                        help='filename of firmware to analyze')

    parser.add_argument('-d', action='store', dest='outdir',
                        default='outdir',
                        help='Output directory of extracted contents')


    results = parser.parse_args()

    binwalk_extract(results.filename, results.outdir)

