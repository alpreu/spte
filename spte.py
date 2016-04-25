import re
import shutil
import sys
import os
import glob

srt_structure = re.compile("[1-9][0-9]*\n"
    "[0-9][0-9]:[0-5][0-9]:[0-5][0-9],[0-9][0-9]?[0-9]?"
    " --> [0-9][0-9]:[0-5][0-9]:[0-5][0-9],[0-9][0-9]?[0-9]?\n", re.MULTILINE)
opening_tag = re.compile("<[A-Za-z]+>")
closing_tag = re.compile("<\/[A-Za-z]+>")


def main(argv):
    if "--help" in argv:
        print("Usage: spte [FILE/FOLDER] [OPTION]")
        print(" -rs \t remove styletags")
    else:
        inpath = argv[1]
        splitpath = os.path.splitext(inpath)
        if splitpath[1] == ".srt":
            if argv[2] == "-rs":
                print("remove")
                remove_styletags(inpath)
            #extract_text(inpath)
        elif splitpath[1] == "":  # folder
            if inpath.endswith("/"):
                files = glob.glob(inpath + "*srt")
            else:
                files = glob.glob(inpath + "/*srt")
            if not files:  # no files were found
                print("no .srt files found")
            else:
                if argv[2] == "-rs":
                    for f in files:
                        remove_styletags(f)
                        extract_text(f)
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
    #for line in f:
     #   print(line)
    open(outpath, "w").write(srt_structure.sub("", f))
    print("extracted " + outpath)


def remove_styletags(inpath):
    split = os.path.splitext(inpath)
    outpath = split[0] + ".txt"
    #shutil.copyfile(inpath, outpath)
    f = open(outpath, "r+").read()
    open(outpath, "w").write(opening_tag.sub("", f))
    open(outpath, "w").write(closing_tag.sub("", f))

#todo: dont onverwrite changes, open file/outout once, use multiple regexes
#todo: better program flow
#todo: refactor imports
#todo: proper checking for flags



if __name__ == "__main__":
    main(sys.argv)