import os
import sys
import struct


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


def clean_pipe(f, **args):
    try:
        f(**args)
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
    h['is_filtered'] = True if second[1] == 'Y' else False
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
