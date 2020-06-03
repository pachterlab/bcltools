import os
from .utils import (prepend_zeros_to_number, get_bin, num2qual, qual2num)
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

    def open_bcl_read(self):
        f = open(self.path,
                 'rb') if not self.gzipped else gzip.open(self.path, 'rb')
        return f

    def open_bcl_write(self):
        f = open(self.path,
                 'ab') if not self.gzipped else gzip.open(self.path, 'ab')
        return f

    def read_header(self):
        """
        # Note: N is the cluster index
        Bytes     | Description         | Data type
        Bytes 0–3 | Number N of cluster | Unsigned 32bits little endian integer
        """

        f = self.open_bcl_read()

        up = struct.unpack(self.header_fmt, f.read(self.header_len))
        sys.stdout.write(f'{up[0]}\n')

        f.close()
        return up

    def read_record(self):
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

        f = self.open_bcl_read()

        up = struct.unpack(self.header_fmt, f.read(self.header_len))
        sys.stdout.write(f'{up}\n')
        itr = struct.iter_unpack(self.record_fmt, f.read())
        # if i[0] is equal to zero then its a no call 'N'
        for idx, i in enumerate(itr):
            base = num2base.get(3 & i[0], 0)
            num = i[0] >> 2
            qual = num2qual(num)
            sys.stdout.write(f'{get_bin(i[0], 8)}\t{base}\t{qual}\n')

        f.close()

    # Specific to Nextseq
    def write_header(self, n_reads):
        header = struct.pack(self.header_fmt, n_reads)

        f = self.open_bcl_write()
        f.write(header)

        f.close()

    def write_record(self, base, qual):
        """
        Write a single record containing a quality score and a base, to the bcl file.
        """

        r = 0
        if base != "N":
            q = qual2num(qual) << 2
            b = base2num[base]
            r = q | b
        record = struct.pack(self.record_fmt, r)

        f = self.open_bcl_write()
        f.write(record)

        f.close()


class Machine:

    def __init__(self, machine):
        pass


class BCLFolderStructure:

    def __init__(self, n_cycles, n_lanes, machine_type, base_path):

        intensities_path = "Data/Intensities"
        base_calls_path = os.path.join(intensities_path, "BaseCalls")

        self.machine_type = None
        self.n_cycles = n_cycles
        self.n_lanes = n_lanes
        self.base_path = base_path

        self.intensities_path = os.path.join(self.base_path, intensities_path)
        self.base_calls_path = os.path.join(self.base_path, base_calls_path)

        self.bcl_files = []
        self.locs_files = []

    def base_calls_lane_path(self, lane_number):
        lane = f'L{prepend_zeros_to_number(3, lane_number)}'
        return os.path.join(self.base_calls_path, lane)

    def locs_lane_path(self, lane_number):
        lane = f'L{prepend_zeros_to_number(3, lane_number)}'
        return os.path.join(self.intensities_path, lane)

    # below doesnt do anything but should
    # def make_lane_folders(path, n_lanes):
    #     base_path = os.path.join(path, "BaseCalls/")
    #     lanes = []
    #     for i in range(n_lanes):
    #         L = os.path.join(base_path, f"L{prepend_zeros_to_number(3, i+1)}")
    #         os.makedirs(L)
    #         lanes.append(L)
    #     return lanes


# TODO this is needed for Miseq
# def make_bcl_folders(read_len, path):
#     base_path = os.path.join(path, "BaseCalls/L001/")
#     if not os.path.exists(base_path):
#         for i in range(read_len):
#             os.makedirs(os.path.join(base_path, f"C{i+1}.1"))
#     return
