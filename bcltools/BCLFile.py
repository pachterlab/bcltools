from .utils import (num2qual, qual2num)
import struct
import sys
import gzip

from .config import GZIPPED

num2base = {0: "A", 1: "C", 2: "G", 3: "T"}
base2num = {"A": 0, "C": 1, "G": 2, "T": 3}


class BCLFile(object):

    def __init__(self, path, machine_type):
        self.path = path
        self.gzipped = GZIPPED.get(machine_type.lower(), False)

        self.header_fmt = "<i"
        self.record_fmt = "<B"
        self.header_len = 4

        self.file = None

    def open(self, mode):
        # mode for read = 'rb'
        # mode for write append = 'ab'
        # mode for seek write = 'r+b'
        if not self.isopen():
            self.file = open(
                self.path, mode
            ) if not self.gzipped else gzip.open(self.path, mode)
        return

    def close(self):
        return self.file.close()

    def isopen(self):
        if self.file is None:
            return False
        else:
            return not self.file.closed

    def read_header(self):
        """
        # Note: N is the cluster index
        Bytes     | Description         | Data type
        Bytes 0–3 | Number N of cluster | Unsigned 32bits little endian integer
        """

        self.open('rb')

        up = struct.unpack(self.header_fmt, self.file.read(self.header_len))
        sys.stdout.write(f'{up[0]}\n')

        self.close()

        return up

    def read_record(self, n_lines=-1, skip_header=True):
        """
        # Byte specification of *.bcl
        # Note: N is the cluster index
        #
        # Bytes         | Description              | Data type
        # -----------------------------------------------------
        # Bytes 0–3     | Number N of cluster      | Unsigned 32bits little endian integer
        #
        # Bytes 4–(N+3) | Bits 0-1 are the bases,  | Unsigned 8bits integer
        #               | respectively [A, C, G, T]
        #               | for [0, 1, 2, 3]: bits
        #               | 2-7 are shifted by two
        #               | bits and contain the
        #               | quality score. All bits
        #               | ‘0’ in a byte is reserved
        #               | for no-call.
        """

        self.open('rb')

        if skip_header:
            self.file.seek(self.header_len)
        else:
            self.read_header()

        itr = struct.iter_unpack(self.record_fmt, self.file.read())
        # if i[0] is equal to zero then its a no call 'N'
        for idx, i in enumerate(itr):
            if idx == n_lines:
                break
            base = num2base.get(3 & i[0], 0)
            num = i[0] >> 2
            qual = num2qual(num)
            sys.stdout.write(f'{base}\t{qual}\n')

        self.close()

    def write_header(self, n_reads, close=True):
        header = struct.pack(self.header_fmt, n_reads)

        self.open('wb')
        self.file.write(header)

        if close:
            self.close()

    def change_header(self, n_reads):
        header = struct.pack(self.header_fmt, n_reads)

        self.open('r+b')
        self.file.seek(0)
        self.file.write(header)
        self.file.close()

    def write_record(self, base, qual, close=True):
        """
        Write a single record containing a quality score and a base, to the bcl file.
        """

        r = 0
        if base != "N":
            q = qual2num(qual) << 2
            b = base2num[base]
            r = q | b
        record = struct.pack(self.record_fmt, r)

        self.open('ab')
        self.file.write(record)

        if close:
            self.close()

    def write_records(self, infile):

        for idx, line in enumerate(infile, 1):
            base, qual = line.strip().split()
            self.write_record(base, qual, close=False)

        self.close()

        n_reads = idx
        self.change_header(n_reads)


class Machine:

    def __init__(self, machine):
        pass
