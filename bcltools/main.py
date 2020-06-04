#!/usr/bin/env python3

import argparse
import sys
# from .bcltools import (fastq2bcl)
from .utils import (clean_pipe)
from .config import MACHINE_TYPES

from .BCLFile import BCLFile
# from .BCLFolderStructure import BCLFolderStructure


def parse_read(args):
    bcl = BCLFile(args.bcl, args.x)

    if args.head:
        return clean_pipe(bcl.read_header)

    elif not args.head:
        return clean_pipe(bcl.read_record)

    return


def parse_write(args):
    # given a text format of a bcl file, write a bcl file
    if not args.file:
        sys.exit("Please provide an input file, or pipe it via stdin.")
    else:
        if not args.p:
            if not args.o:
                sys.exit('Please provide an output file or pipe')
            else:
                # overwrite the file
                out_bcl = BCLFile(args.o, args.x)
                out_bcl.write_header(0, close=False)
                out_bcl.write_records(args.file)
                args.file.close()


# def parse_convert(args):
#     # folder_stucture = BCLFolderStructure()
#     # TODO check if -o exists or not, make path accordingly
#     for f in args.fastqs:
#         if not is_gz_file(f):
#             raise Exception(f"{f} is not a gzipped file.")
#
#     return fastq2bcl(args.o, args.fastqs)


def setup_read_args(parser, parent):
    parser_read = parser.add_parser(
        'read',
        description='Convert bcl files to fastq files',
        help='Convert bcl files to fastq files',
        parents=[parent],
        add_help=False
    )

    required_read = parser_read.add_argument_group('required arguments')

    required_read.add_argument(
        '-x',
        help="Type of machine",
        choices=MACHINE_TYPES,
        type=str.lower,
        required=True
    )

    optional_read = parser_read.add_argument_group('optional arguments')

    optional_read.add_argument(
        '-o', metavar='OUT FILE', help='output file', type=str, required=False
    )

    # fix to make -n take in a number
    optional_read.add_argument(
        "-hd",
        "--head",
        help="Read the header of a bcl file",
        action='store_true',
        required=False
    )

    optional_read.add_argument(
        "-h", "--help", action="help", help="show this help message and exit"
    )

    # currently takes only one, add support for more than one
    parser_read.add_argument('bcl')

    # TODO add slicing functionality for the read
    # TODO add option for the type of machine

    return parser_read


def setup_write_args(parser, parent):
    parser_write = parser.add_parser(
        'write',
        description='Convert fastq files to bcl files',
        help='Convert fastq files to bcl files',
        parents=[parent],
        add_help=False
    )

    required_write = parser_write.add_argument_group('required arguments')

    required_write.add_argument(
        '-x',
        help="Type of machine",
        choices=MACHINE_TYPES,
        type=str.lower,
        required=True
    )

    optional_write = parser_write.add_argument_group('optional arguments')

    optional_write.add_argument(
        '-o',
        metavar='OUT FOLDER',
        help='output folder',
        type=str,
        required=True
    )

    optional_write.add_argument(
        '-p', metavar='PIPE', help='Pipe file out', type=str, required=False
    )

    optional_write.add_argument(
        "-h", "--help", action="help", help="show this help message and exit"
    )
    # currently takes only one, add support for more than one
    # parser_write.add_argument('file', nargs='+')
    parser_write.add_argument(
        'file', nargs='?', type=argparse.FileType('r'), default=sys.stdin
    )
    # TODO add option for the type of machine

    return parser_write


COMMAND_TO_FUNCTION = {'write': parse_write, 'read': parse_read}


# Add parser to print bcl header
def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(
        dest='command',
        metavar='<CMD>',
    )

    parent = argparse.ArgumentParser(add_help=False)

    parser_read = setup_read_args(subparsers, parent)
    parser_write = setup_write_args(subparsers, parent)

    command_to_parser = {'write': parser_write, 'read': parser_read}

    # Show help when no arguments are given
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    if len(sys.argv) == 2:
        if sys.argv[1] in command_to_parser:
            command_to_parser[sys.argv[1]].print_help(sys.stderr)
        else:
            parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    COMMAND_TO_FUNCTION[args.command](args)

    return 1


if __name__ == "__main__":
    main()
