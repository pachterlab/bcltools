#!/usr/bin/env python3

from struct import *
import sys
import argparse
from .bcltools import (
    bcl2fastq,
    fastq2bcl
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', metavar="OUT", help='output folder', type=str, required=True)
    parser.add_argument('file')
    args = parser.parse_args()

    bcl2fastq(args.file)
    # fastq2bcl(args.o, args.file)

    return 1

if __name__=="__main__":
    main()
