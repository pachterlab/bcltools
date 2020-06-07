import struct

from .utils import type_to_num_bytes


class BinaryFile(object):

    def __init__(self, path, header_fmt, record_fmt, gzipped=False):
        self.path = path
        self.header_fmt = header_fmt
        self.record_fmt = record_fmt

        self.header_len = type_to_num_bytes(self.header_fmt)
        self.record_len = type_to_num_bytes(self.record_fmt)

        self.gzipped = gzipped

        self.file = None

    def isopen(self):
        if self.file is None:
            return False
        else:
            return not self.file.closed

    def open(self, mode):
        # read = 'rb', write append = 'ab', seek write = 'r+b'
        if not self.isopen():
            self.file = open(self.path, mode)
        return

    def close(self):
        return self.file.close()

    def read_header(self):
        self.open('rb')

        header = struct.unpack(self.header_fmt, self.file.read(self.header_len))
        self.close()

        return header

    def read_record(self, skip_header=True):
        self.open('rb')

        if skip_header:
            self.file.seek(self.header_len)
        else:
            self.read_header()

        itr = struct.iter_unpack(self.record_fmt, self.file.read())
        for idx, record in enumerate(itr):
            yield record

        # this may be unnecessary
        self.close()

    def write_header(self, *header_values):
        self.open('wb')

        header = struct.pack(self.header_fmt, *header_values)

        self.file.write(header)

        self.close()

    def change_header(self, *header_values):
        self.open('r+b')

        header = struct.pack(self.header_fmt, *header_values)

        self.file.seek(0)
        self.file.write(header)
        self.close()

    def write_record(self, *record_values, keep_open=False):
        self.open('ab')

        record = struct.pack(self.record_fmt, *record_values)
        self.file.write(record)
        if not keep_open:
            return self.close()
        return

    def write_from_stream(self, stream):
        # assume the stream is open already
        for line in stream:
            data = line.strip().split()
            yield data

        self.close()
