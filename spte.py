# -*- coding: utf-8 -*-
import re
import shutil
import sys
import os
import glob
import chardet
import codecs

srt_structure = re.compile("[1-9][0-9]*\r?\n"
    "[0-9][0-9]:[0-5][0-9]:[0-5][0-9],[0-9][0-9]?[0-9]?"
    " --> [0-9][0-9]:[0-5][0-9]:[0-5][0-9],[0-9][0-9]?[0-9]?\r?\n", re.MULTILINE)
opening_styletag = re.compile("<[A-Za-z]+>")
closing_styletag = re.compile("<\/[A-Za-z]+>")


def main(argv):
    if "--help" in argv:
        print("Usage: spte.py [FILE/FOLDER] [OPTIONS]")
        print("Options:")
        print(" -rs \t remove styletags")
    else:
        inpath = argv[1]
        splitpath = os.path.splitext(inpath)
        if splitpath[1] == ".srt":
            filedata = create_working_copy(inpath)  # create working copy first
            if len(argv) == 3 and argv[2] == "-rs":
                filedata = remove_styletags(filedata)
            extract_text(filedata)
        elif splitpath[1] == "":  # folder
            if inpath.endswith("/"):
                files = glob.glob(inpath + "*srt")
            else:
                files = glob.glob(inpath + "/*srt")
            if not files:  # no files were found
                print("no .srt files found")
            else:
                if len(argv) == 3 and argv[2] == "-rs":
                    for f in files:
                        filedata = create_working_copy(f)  # create working copy first
                        filedata = remove_styletags(filedata)
                        extract_text(filedata)
                else:
                    for f in files:
                        filedata = create_working_copy(f)  # create working copy first
                        extract_text(filedata)
        else:
            print("error reading filepath")


def extract_text(filedata):
    outpath = filedata[0]
    copyfile = filedata[1]
    file_encoding = filedata[2]
    codecs.open(outpath, "w", file_encoding).write(srt_structure.sub("", copyfile))
    print("extracted " + outpath)


def remove_styletags(filedata):
    outpath = filedata[0]
    copyfile = filedata[1]
    file_encoding = filedata[2]
    matches = opening_styletag.findall(copyfile)
    print(matches)
    codecs.open(outpath, "w", file_encoding).write(opening_styletag.sub("", copyfile))
    copyfile = codecs.open(outpath, "r+", file_encoding).read()
    matches = closing_styletag.findall(copyfile)
    print(matches)
    codecs.open(outpath, "w", file_encoding).write(closing_styletag.sub("", copyfile))
    copyfile = codecs.open(outpath, "r+", file_encoding).read()
    return (outpath, copyfile, file_encoding)


def create_working_copy(inpath):
    split = os.path.splitext(inpath)
    outpath = split[0] + ".txt"
    shutil.copyfile(inpath, outpath)
    rawdata = open(outpath, "rb").read()
    file_encoding = chardet.detect(rawdata)["encoding"]
    copyfile = codecs.open(outpath, "r+", file_encoding).read()
    return (outpath, copyfile, file_encoding)


if __name__ == "__main__":
    main(sys.argv)
