import struct
import os

from .utils import (prepend_zeros_to_number)


# Number of cycles are equal per lane
# but the number of reads are now reads per lane
# TODO TEST
def make_bcl_files_per_lane(lanes, reads_per_lane, read_len, n_reads):
    assertion = "The number of lanes must equal the length of the reads_per_lane list."
    assert len(reads_per_lane) == len(lanes), assertion

    header_fmt = "<i"
    header = struct.pack(header_fmt, n_reads)

    bcls = []  # list of lists, split by lane
    for rpl, l in zip(reads_per_lane, lanes):
        tmp = []
        for i in range(read_len):
            bcl_name = f"{prepend_zeros_to_number(4, i+1)}.bcl"
            bcl_path = os.path.join(l, bcl_name)
            tmp.append(bcl_path)
            with open(bcl_path, 'wb') as f:
                f.write(header)
        bcls.append(tmp)

    return bcls
