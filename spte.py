import re
import shutil
import sys
import os
import glob

regex = re.compile("[1-9][0-9]*\n"
    "[0-9][0-9]:[0-5][0-9]:[0-5][0-9],[0-9][0-9][0-9]"
    " --> [0-9][0-9]:[0-5][0-9]:[0-5][0-9],[0-9][0-9][0-9]\n", re.MULTILINE)


def main(argv):
    if "--help" in argv:
        print("Usage: spte [FILE/FOLDER] [OPTION]")
        print(" -rs \t remove styletags")
    else:
        inpath = argv[1]
        splitpath = os.path.splitext(inpath)
        if splitpath[1] == ".srt":
            extract_text(inpath)
        if splitpath[1] == "":  # folder
            if inpath.endswith("/"):
                files = glob.glob(inpath + "*srt")
            else:
                files = glob.glob(inpath + "/*srt")
            if not files:  # no files were found
                print("no .srt files found")
            else:
                for f in files:
                    extract_text(f)
        else:
            print("error reading filepath")


def extract_text(inpath):
    split = os.path.splitext(inpath)
    outpath = split[0] + ".txt"
    shutil.copyfile(inpath, outpath)
    f = open(outpath, "r+").read()
    open(outpath, "w").write(regex.sub("", f))
    print("extracted " + outpath)


#todo: remove syletags
#todo: refactor imports
#<[A-Za-z]+> is start styletag
#</[A-Za-z]+> is closing styletag


if __name__ == "__main__":
    main(sys.argv)