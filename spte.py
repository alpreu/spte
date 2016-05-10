import re
import shutil
import sys
import os
import glob

srt_structure = re.compile("[1-9][0-9]*\n"
    "[0-9][0-9]:[0-5][0-9]:[0-5][0-9],[0-9][0-9]?[0-9]?"
    " --> [0-9][0-9]:[0-5][0-9]:[0-5][0-9],[0-9][0-9]?[0-9]?\n", re.MULTILINE)
opening_styletag = re.compile("<[A-Za-z]+>")
closing_styletag = re.compile("<\/[A-Za-z]+>")


def main(argv):
    if "--help" in argv or (len(argv) == 3 and not argv[2] == "-rs"):
        print("Usage: spte [FILE/FOLDER] [OPTION]")
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
    open(outpath, "w").write(srt_structure.sub("", copyfile))
    print("extracted " + outpath)


def remove_styletags(filedata):
    outpath = filedata[0]
    copyfile = filedata[1]
    open(outpath, "w").write(opening_styletag.sub("", copyfile))
    copyfile = open(outpath, "r+").read()
    open(outpath, "w").write(closing_styletag.sub("", copyfile))
    copyfile = open(outpath, "r+").read()
    return (outpath, copyfile)


#todo: better program flow
#todo: only import the stuff used
#todo: improve input handling of flags

def create_working_copy(inpath):
    split = os.path.splitext(inpath)
    outpath = split[0] + ".txt"
    shutil.copyfile(inpath, outpath)
    copyfile = open(outpath, "r+").read()
    return (outpath, copyfile)

if __name__ == "__main__":
    main(sys.argv)