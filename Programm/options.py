import argparse

parser = argparse.ArgumentParser(
    prog='mrsync.py'
)

parser.add_argument('-r','--recursive',action="store_true", default=False)
parser.add_argument('--list-only',action="store_true")
parser.add_argument('--timeout',type= int, default=0)
parser.add_argument('--blocking-io',action="store_true")
parser.add_argument("DST")
parser.add_argument("SRC", nargs="?")
args = parser.parse_args()