import os
import sys
import struct

from .config import TYPE_LEN, CHAR_ORDER


def prepend_zeros_to_number(len_name, number):
    len_number = len(str(number))
    return '0' * (len_name - len_number) + str(number)


def get_bin(x, n=0):
    """
    Get the binary representation of x.

    Parameters
    ----------
    x : int
    n : int
        Minimum number of digits. If x needs less digits in binary, the rest
        is filled with zeros.

    Returns
    -------
    str
    """
    return format(x, 'b').zfill(n)


def qual2num(qual):
    num = ord(qual) - 33
    return num


def num2qual(num):
    qual = chr(num + 33)
    return qual


# the convention is insane for illumina
# Y means that the read is filtered out
# N means the read is not filtered out (ie it is kept)
# in binary, 1 means the read is kept == N
# in binary, 0 means the read is filtered out == Y

filter2num = lambda x: {'N': 1, 'Y': 0}.get(x, None)
num2filter = lambda x: {1: 'N', 0: 'Y'}.get(x, None)


def clean_pipe(f, **args):
    try:
        for line in f(**args):
            s = "\t".join(map(str, line))

            sys.stdout.write(s)
            sys.stdout.write("\n")

    except BrokenPipeError:
        # Python flushes standard streams on exit; redirect remaining output
        # to devnull to avoid another BrokenPipeError at shutdown
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(1)  # Python exits with error code 1 on EPIPE


def parse_fastq_header(line):
    h = {}
    # @<instrument>:<run number>:<flowcell ID>:<lane>:<tile>:<x-pos>:<y-pos> \
    # <read>:<is filtered>:<control number>:<sample number>
    first, second = line.split(" ")
    first = first.split(':')
    second = second.split(':')

    h['instrument'] = first[0][1:]
    h['run_number'] = int(first[1])
    h['flowcell_ID'] = first[2]
    h['lane'] = int(first[3])
    # composed of 5 numbers
    # surface {1, 2}, swath {1, 2, 3}, camera {1, 2, 3, 4, 5, 6}, tile {01-12}
    h['tile'] = int(first[4])
    h['x'] = int(first[5])
    h['y'] = int(first[6])

    h['read'] = int(second[0])
    h['is_filtered_out'] = second[1]
    h['control_number'] = int(second[2])
    h['sample_number'] = int(second[3])

    return h


# def touch(file):
#     if not os.path.exists(file):
#         with open(file, 'w'): pass


def binread(file, header_fmt, header_len, record_fmt):
    with open(file, 'rb') as f:

        head = struct.unpack(header_fmt, f.read(header_len))
        sys.stdout.write(f'{head}\n')

        itr = struct.iter_unpack(record_fmt, f.read())

        for idx, i in enumerate(itr):
            sys.stdout.write(f'{i[0]}\n')


def lane2num(lane):
    return int(lane[1:])


def split_reads(num, div):
    return [num // div + (1 if x < num % div else 0) for x in range(div)]


def type_to_num_bytes(s):
    s_types = ''.join(c for c in s if c not in CHAR_ORDER)
    s_len = sum([TYPE_LEN.get(i, 0) for i in s_types])
    return s_len
