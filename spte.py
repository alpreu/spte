# -*- coding: utf-8 -*-
import re
import shutil
import sys
import os
import glob
import chardet
import codecs
import argparse


srt_structure = re.compile("[1-9][0-9]*\r?\n"
    "[0-9][0-9]:[0-5][0-9]:[0-5][0-9],[0-9][0-9]?[0-9]?"
    " --> [0-9][0-9]:[0-5][0-9]:[0-5][0-9],[0-9][0-9]?[0-9]?\r?\n", re.MULTILINE)
opening_styletag = re.compile("<[A-Za-z]+>")
closing_styletag = re.compile("<\/[A-Za-z]+>")


parser = argparse.ArgumentParser(description="Extract meaningful plaintext from .srt files.")
parser.add_argument("inpath", metavar="FILE...", nargs="?",  type=str, default=os.getcwd(), help="file or directory to process")
parser.add_argument("-rs", "--removestyle", help="remove styletags", dest="style_should_be_removed", action="store_true")


def main(argv):
    args = parser.parse_args() # parse command line arguments
    if os.path.isfile(args.inpath): # file was given
        file_extension = os.path.splitext(args.inpath)[1]
        if file_extension == ".srt":
            filedata = create_working_copy(args.inpath)
            if args.style_should_be_removed:
                filedata = remove_styletags(filedata)
            extract_text(filedata)
    elif os.path.isdir(args.inpath): # directory was given
        files = glob.glob(args.inpath + "/*srt")
        if files:
            for f in files:
                filedata = create_working_copy(f)
                if args.style_should_be_removed:
                    filedata = remove_styletags(filedata)
                extract_text(filedata)
        else:
            print("No .srt files found in directory")
    else:
        print("Error reading filepath")


def extract_text(filedata):
    outpath = filedata[0]
    copyfile = filedata[1]
    file_encoding = filedata[2]
    codecs.open(outpath, "w", file_encoding).write(srt_structure.sub("", copyfile))
    print("extracted " + os.path.split(outpath)[1])


def remove_styletags(filedata):
    outpath = filedata[0]
    copyfile = filedata[1]
    file_encoding = filedata[2]
    codecs.open(outpath, "w", file_encoding).write(opening_styletag.sub("", copyfile))
    copyfile = codecs.open(outpath, "r+", file_encoding).read()
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
