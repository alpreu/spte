# -*- coding: utf-8 -*-
import re
import sys
import os
import glob
import chardet
import codecs
import argparse


srt_structure = re.compile(
    "[1-9][0-9]*\r?\n"
    "[0-9][0-9]:[0-5][0-9]:[0-5][0-9],[0-9][0-9]?[0-9]?"
    " --> "
    "[0-9][0-9]:[0-5][0-9]:[0-5][0-9],[0-9][0-9]?[0-9]?\r?\n",
    re.MULTILINE)
opening_styletag = re.compile("<[A-Za-z]+>")
closing_styletag = re.compile("<\/[A-Za-z]+>")
blank_line = re.compile("(^|\n)\s*(\n|$)")


parser = argparse.ArgumentParser(description="Extract meaningful plaintext from .srt files.")
parser.add_argument("inpath", metavar="FILE...", help="file or directory to process", nargs="?", type=str, default=os.getcwd())
parser.add_argument("-s", "--removestyle", help="remove styletags", dest="style_should_be_removed", action="store_true")
parser.add_argument("-b", "--removeblanks", help="remove blank lines", dest="blanks_should_be_removed", action="store_true")


def main(argv):
    args = parser.parse_args()  # parse command line arguments
    files = []
    if os.path.isfile(args.inpath):  # file was given
        file_extension = os.path.splitext(args.inpath)[1]
        if file_extension == ".srt":
            files = [args.inpath]
    elif os.path.isdir(args.inpath):  # directory was given
        files = glob.glob(args.inpath + "/*.srt")
    else:
        print("Error reading filepath")
    if files:
        process(files, args)
    else:
        print("No .srt files found")


def process(files, args):
    for f in files:
        encoding = get_file_encoding(f)
        outputfile = create_output_file(f, encoding)
        original_content = get_file_content(f, encoding)
        modified_content = extract_text(original_content)
        if args.style_should_be_removed:
            modified_content = remove_styletags(modified_content)
        if args.blanks_should_be_removed:
            modified_content = remove_blank_lines(modified_content)
        outputfile.write(modified_content)
        outputfile.close()
        print("Processed " + os.path.split(f)[1])


def get_file_content(path, encoding):
    return codecs.open(path, "r", encoding).read()


def extract_text(content):
    return srt_structure.sub("", content)


def remove_styletags(content):
    content = opening_styletag.sub("", content)
    content = closing_styletag.sub("", content)
    return content


def remove_blank_lines(content):
    return blank_line.sub("", content)


def create_output_file(inpath, encoding):
    split = os.path.splitext(inpath)
    outpath = split[0] + ".txt"
    return codecs.open(outpath, "w", encoding)


def get_file_encoding(path):
    rawdata = open(path, "rb").read()  # open in bytes-mode
    return chardet.detect(rawdata)["encoding"]


if __name__ == "__main__":
    main(sys.argv)
