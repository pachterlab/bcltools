from .BinaryFile import BinaryFile


class LOCSFile(BinaryFile):
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

    def __init__(
        self, path, header_fmt="<IfL", record_fmt="<ff", gzipped=False
    ):
        super().__init__(path, header_fmt, record_fmt, gzipped=False)

        self.version_num = 1
        self.magic_num = 1.0

    def read_header_locs(self):
        version_num, magic_num, n_reads = self.read_header(
        )  # vnum=1, magic_num=1.0
        return ((version_num, magic_num, n_reads),)

    def read_record_locs(self, skip_header=True):
        for record in self.read_record(skip_header=skip_header):
            x, y = record

            yield (x, y)

    def write_header_locs(self, n_reads):
        header_values = (self.version_num, self.magic_num, n_reads)
        return self.write_header(*header_values)

    def change_header_locs(self, n_reads):
        header_values = (self.version_num, self.magic_num, n_reads)
        return self.change_header(*header_values)

    def write_record_locs(self, x, y, keep_open=False):
        record_values = (x, y)
        return self.write_record(*record_values, keep_open=keep_open)

    def write_from_stream_locs(self, infile):

        for idx, data in enumerate(self.write_from_stream(infile), 1):
            x, y = map(float, data)

            self.write_record_locs(x, y, keep_open=True)

        self.close()

        n_reads = idx
        self.change_header_locs(n_reads)
