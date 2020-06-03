from .config import GZIPPED
import gzip
import struct
import sys


class BCIFile(object):

    def __init__(self, path, machine_type):
        self.path = path
        self.gzipped = GZIPPED.get(machine_type.lower(), False)

        self.header_fmt = "<L"
        self.record_fmt = "<L"
        self.header_len = 4

    def open_bci_read(self):
        f = open(self.path,
                 'rb') if not self.gzipped else gzip.open(self.path, 'rb')
        return f

    def open_bci_write(self):
        f = open(self.path,
                 'ab') if not self.gzipped else gzip.open(self.path, 'ab')
        return f

    def read_header(self):
        f = self.open_bci_read()

        BCI_version = struct.unpack(self.header_fmt, f.read(self.header_len))[0]
        n_tiles = struct.unpack(self.header_fmt, f.read(self.header_len))[0]

        sys.stdout.write(f'{BCI_version}\t{n_tiles}\n')

        f.close()

    def read_records(self):
        """
        Bytes Description
        Bytes 0–3 The tile number.
        Bytes 4–7 The number of clusters in the tile.
        """
        f = self.open_bci_read()

        BCI_version = struct.unpack(self.header_fmt, f.read(self.header_len))[0]
        n_tiles = struct.unpack(self.header_fmt, f.read(self.header_len))[0]

        sys.stdout.write(f'{BCI_version}\t{n_tiles}\n')

        itr = struct.iter_unpack(self.record_fmt, f.read())

        for idx, i in enumerate(itr, 1):
            sys.stdout.write(f'{i[0]}\n')

        f.close()
