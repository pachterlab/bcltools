from .utils import (num2qual, qual2num)
from .BinaryFile import BinaryFile

num2base = {0: "A", 1: "C", 2: "G", 3: "T"}
base2num = {"A": 0, "C": 1, "G": 2, "T": 3}


class BCLFile(BinaryFile):

    def __init__(
        self, path, header_fmt="<I", record_fmt="<B", compression=None
    ):
        super().__init__(path, header_fmt, record_fmt, compression=compression)

    def read_header_bcl(self):
        """
        # Note: N is the cluster index
        Bytes     | Description         | Data type
        Bytes 0–3 | Number N of cluster | Unsigned 32bits little endian integer
        """
        # consider returning this as a tuple
        n_reads = self.read_header()
        return ((n_reads),)

    def read_record_bcl(self, skip_header=True):
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
        for record in self.read_record(skip_header=skip_header):
            r, = record

            base = num2base.get(3 & r, 0)
            num = r >> 2
            qual = num2qual(num)

            yield (base, qual)

    def write_header_bcl(self, n_reads):
        header_values = (n_reads,)
        return self.write_header(*header_values)

    def change_header_bcl(self, n_reads):
        header_values = (n_reads,)
        return self.change_header(*header_values)

    def write_record_bcl(self, base, qual, keep_open=False):
        """
        Write a single record containing a quality score and a base, to the bcl file.
        """
        r = 0
        if base != "N":
            q = qual2num(qual) << 2
            b = base2num[base]
            r = q | b
        record_values = (r,)
        return self.write_record(*record_values, keep_open=keep_open)

    def write_from_stream_bcl(self, infile):

        for idx, data in enumerate(self.write_from_stream(infile), 1):
            base, qual = data
            self.write_record_bcl(base, qual, keep_open=True)

        self.close()

        n_reads = idx
        self.change_header_bcl(n_reads)
