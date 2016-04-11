import re
import shutil
import sys


def main(argv):
    if "--help" in argv:
        print("pass inputfile path and outputfile path as arguments.")
    else:
        inpath = argv[1]
        outpath = argv[2]
        extract_text(inpath, outpath)


def extract_text(inpath, outpath):
    regex = re.compile("[1-9][0-9]*\n[0-9][0-9]:[0-5][0-9]:[0-5][0-9],[0-9][0-9][0-9] --> [0-9][0-9]:[0-5][0-9]:[0-5][0-9],[0-9][0-9][0-9]\n", re.MULTILINE)
    shutil.copyfile(inpath, outpath)
    f = open(outpath, "r+").read()
    open(outpath, "w").write(regex.sub("", f))
    print("Plaintext extraction finished.")


if __name__ == "__main__":
    main(sys.argv)