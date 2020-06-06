import struct
import sys


class LOCSFile(object):
    """
    The locs file format is one 3 Illumina formats(pos, locs, and clocs) that stores position data exclusively.
    locs files store position data for successive clusters in 4 byte float pairs, described as follows:
    bytes 1-4    : (int?) Version number (1)
    bytes 5-8    : 4 byte float equaling 1.0
    bytes 9-12   : unsigned int numClusters
    bytes 13-16: : X coordinate of first cluster (32-bit float)
    bytes 17-20: : Y coordinate of first cluster (32-bit float)

    The remaining bytes of the file store the X and Y coordinates of the remaining clusters.
    """

    def __init__(self, path):
        self.path = path

        self.header_fmt = '<IfL'
        self.header_len = 12

        self.record_fmt = '<ff'
        self.record_len = 8

        self.file = None

    def open(self, mode):
        # read = 'rb', write append = 'ab', seek write = 'r+b'
        if not self.isopen():
            self.file = open(self.path, mode)
        return

    def isopen(self):
        if self.file is None:
            return False
        else:
            return not self.file.closed

    def close(self):
        return self.file.close()

    def read_header(self):
        self.open('rb')

        header = struct.unpack(self.header_fmt, self.file.read(self.header_len))
        version_num, magic_num, n_reads = header  # vnum=1, magic_num=1.0
        sys.stdout.write(f'{version_num}\t{magic_num}\t{n_reads}\n')
        self.close()

    def read_record(self, n_lines=-1, skip_header=True):
        self.open('rb')

        if skip_header:
            self.file.seek(self.header_len)
        else:
            self.read_header()

        itr = struct.iter_unpack(self.record_fmt, self.file.read())
        for idx, i in enumerate(itr):
            if idx == n_lines:
                break
            x, y = i
            sys.stdout.write(f'{x}\t{y}\n')

        self.close()

    # def write_header(self, n_reads):
    #     pass
    # def write_record(self, x, y):
    #     pass
