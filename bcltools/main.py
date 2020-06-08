#!/usr/bin/env python3

import argparse
import sys
import logging
import os

from .bcltools import (
    bclconvert, bclread, bclwrite, bciread, locsread, locswrite, filterread,
    filterwrite
)
from .type_checkers import (check_gz_file, check_lane_lim)
from .config import (MACHINE_TYPES, FILE_TYPES)

logger = logging.getLogger(__name__)


def parse_read(args):
    base_name = os.path.basename(args.file)
    if args.f not in base_name:
        logger.warning(f'Specified "{args.f}" but reading "{base_name}"')

    if args.f == 'bcl':
        bclread(args.file, args.head)
    elif args.f == 'bci':
        bciread(args.file, args.head)
    elif args.f == 'locs':
        locsread(args.file, args.head)
    elif args.f == 'filter':
        filterread(args.file, args.head)
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
                if args.f == 'bcl':
                    bclwrite(args.o, args.file)
                elif args.f == 'locs':
                    locswrite(args.o, args.file)
                elif args.f == 'filter':
                    filterwrite(args.o, args.file)


def parse_convert(args):
    # TODO check if -o exists or not, make path accordingly

    bclconvert(args.n, args.x, args.o, args.fastqs)

    return


def setup_read_args(parser, parent):
    parser_read = parser.add_parser(
        'read',
        description='Read binary file',
        help='Read binary file',
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
        '-f',
        help='type of file (default: bcl)',
        choices=FILE_TYPES,
        type=str,
        required=False,
        default='bcl'
    )

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

    optional_read.add_argument(
        '--verbose', help='Print debugging information', action='store_true'
    )

    # currently takes only one, add support for more than one
    parser_read.add_argument('file')

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
        '-f',
        help='type of file (default: bcl)',
        choices=FILE_TYPES,
        type=str,
        required=False,
        default='bcl'
    )

    optional_write.add_argument(
        '-p', metavar='PIPE', help='Pipe file out', type=str, required=False
    )

    optional_write.add_argument(
        "-h", "--help", action="help", help="show this help message and exit"
    )

    optional_write.add_argument(
        '--verbose', help='Print debugging information', action='store_true'
    )

    # currently takes only one, add support for more than one
    parser_write.add_argument(
        'file', nargs='?', type=argparse.FileType('r'), default=sys.stdin
    )

    return parser_write


def setup_convert_args(parser, parent):
    parser_convert = parser.add_parser(
        'convert',
        description='Convert fastq files to bcl files',
        help='Convert fastq files to bcl files',
        parents=[parent],
        add_help=False
    )

    required_convert = parser_convert.add_argument_group('required arguments')

    required_convert.add_argument(
        '-x',
        help="Type of machine",
        choices=MACHINE_TYPES,
        type=str.lower,
        required=True
    )

    required_convert.add_argument(
        '-n', help="Number of lanes", type=check_lane_lim, required=True
    )

    required_convert.add_argument(
        '-o',
        metavar='OUT FOLDER',
        help='output folder',
        type=str,
        required=True
    )

    optional_convert = parser_convert.add_argument_group('optional arguments')

    optional_convert.add_argument(
        "-h", "--help", action="help", help="show this help message and exit"
    )

    optional_convert.add_argument(
        '--verbose', help='Print debugging information', action='store_true'
    )

    # currently only supports from fastqs to bcls
    parser_convert.add_argument('fastqs', nargs='+', type=check_gz_file)

    return parser_convert


COMMAND_TO_FUNCTION = {
    'write': parse_write,
    'read': parse_read,
    'convert': parse_convert
}


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
    parser_convert = setup_convert_args(subparsers, parent)

    command_to_parser = {
        'write': parser_write,
        'read': parser_read,
        'convert': parser_convert
    }

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

    logging.basicConfig(
        format='[%(asctime)s] %(levelname)7s %(message)s',
        level=logging.DEBUG if args.verbose else logging.INFO,
    )
    logging.getLogger('chardet.charsetprober').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

    logger.debug('Printing verbose output')
    logger.debug(args)

    COMMAND_TO_FUNCTION[args.command](args)

    return 1


if __name__ == "__main__":
    main()
