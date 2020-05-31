#!/usr/bin/env python3

import argparse
import sys
from .bcltools import (bcl2fastq, fastq2bcl)


def parse_b2f(args):
    return bcl2fastq(args.bcl)


def parse_f2b(args):
    # TODO check if -o exists or not, make path accordingly

    return fastq2bcl(args.o, args.fastq)


def setup_b2f_args(parser, parent):
    parser_b2f = parser.add_parser(
        'b2f',
        description='Convert bcl files to fastq files',
        help='Convert bcl files to fastq files',
        parents=[parent]
    )

    parser_b2f.add_argument(
        '-o',
        metavar='OUT FOLDER',
        help='output folder',
        type=str,
        required=True
    )

    # currently takes only one, add support for more than one
    parser_b2f.add_argument('bcl')

    # TODO add slicing functionality for the read
    # TODO add option for the type of machine

    return parser_b2f


def setup_f2b_args(parser, parent):
    parser_f2b = parser.add_parser(
        'f2b',
        description='Convert fastq files to bcl files',
        help='Convert fastq files to bcl files',
        parents=[parent]
    )

    parser_f2b.add_argument(
        '-o',
        metavar='OUT FOLDER',
        help='output folder',
        type=str,
        required=True
    )
    # currently takes only one, add support for more than one
    parser_f2b.add_argument('fastq')
    # TODO add option for the type of machine

    return parser_f2b


COMMAND_TO_FUNCTION = {'f2b': parse_f2b, 'b2f': parse_b2f}


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(
        dest='command',
        metavar='<CMD>',
    )

    parent = argparse.ArgumentParser(add_help=False)

    parser_b2f = setup_b2f_args(subparsers, parent)
    parser_f2b = setup_f2b_args(subparsers, parent)

    command_to_parser = {'f2b': parser_f2b, 'b2f': parser_b2f}

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
