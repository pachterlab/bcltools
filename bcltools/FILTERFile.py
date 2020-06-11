from .BinaryFile import BinaryFile
from .utils import filter2num, num2filter


class FILTERFile(BinaryFile):
    """
    Bytes 0–3 Zero value (for backwards compatibility).
    Bytes 4–7 The filter format version number.
    Bytes 8–11 The number of clusters.
    Bytes 12–(N+11) N—cluster number Unsigned 8 bits integer. Bit 0 is pass or failed filter.
    """

    def __init__(
        self, path, header_fmt="<III", record_fmt="<B", compression=None
    ):
        super().__init__(path, header_fmt, record_fmt, compression=None)

        self.magic_num = 0
        self.version_num = 3

    def read_header_filter(self):
        magic_num, version_num, n_reads = self.read_header()
        return ((magic_num, version_num, n_reads),)

    def read_record_filter(self, skip_header=True):
        for record in self.read_record(skip_header=skip_header):
            r, = record
            value = r & 1
            pass_filter = num2filter(value)

            yield (pass_filter,)

    def write_header_filter(self, n_reads):
        header_values = (self.magic_num, self.version_num, n_reads)
        return self.write_header(*header_values)

    def change_header_filter(self, n_reads):
        header_values = (self.magic_num, self.version_num, n_reads)
        return self.change_header(*header_values)

    def write_record_filter(self, pass_filter, keep_open=False):
        """ Pass filter will be a Y or a N """
        pass_filter_value = filter2num(pass_filter)
        record_values = (pass_filter_value,)
        return self.write_record(*record_values, keep_open=keep_open)

    def write_from_stream_filter(self, infile):
        for idx, data in enumerate(self.write_from_stream(infile), 1):
            pass_filter, = data
            self.write_record_filter(pass_filter, keep_open=True)

        self.close()

        n_reads = idx
        self.change_header_filter(n_reads)
