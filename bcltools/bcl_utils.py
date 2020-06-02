import struct
import sys
import gzip
import os

from .utils import (prepend_zeros_to_number)


# Specific to Nextseq
def write_bcl_header(n_reads, bcl):
    header_fmt = "<i"
    header = struct.pack(header_fmt, n_reads)

    with open(bcl, 'wb') as f:
        f.write(header)


# Specific to Nextseq
base2num = {"A": 0, "C": 1, "G": 2, "T": 3}


def write_bcl_record(base, qual, bcl):
    """
    Write a single record containing a quality score and a base, to the bcl file.
    """
    seq_fmt = "<B"

    r = 0
    if base != "N":
        q = (ord(qual) - 33) << 2
        b = base2num[base]
        r = q | b
    record = struct.pack(seq_fmt, r)
    with open(bcl, 'ab') as f:
        f.write(record)
    return


num2base = {0: "A", 1: "C", 2: "G", 3: "T"}


def read_bcl(bcl):
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
    header_fmt = "<i"
    seq_fmt = "<B"

    with open(bcl, "br") as f:
        up = struct.unpack(header_fmt, f.read(4))
        sys.stdout.write(f'{up}\n')
        itr = struct.iter_unpack(seq_fmt, f.read())
        for idx, i in enumerate(itr):
            base = num2base.get(3 & i[0], 0)
            qual = i[0] >> 2
            sys.stdout.write(f'{bin(i[0])}\t{base}\t{qual}\n')


def read_bcl_header(bcl):
    """
    # Note: N is the cluster index
    Bytes     | Description         | Data type
    Bytes 0–3 | Number N of cluster | Unsigned 32bits little endian integer
    """
    header_fmt = "<i"

    with open(bcl, "rb") as f:
        up = struct.unpack(header_fmt, f.read(4))
        return up


# if bcl file is bgzf then you have to use this one
def read_bcl_header_gzip(bcl):
    header_fmt = "<i"

    with gzip.open(bcl, "rb") as f:
        up = struct.unpack(header_fmt, f.read(4))
        sys.stdout.write(f'{up[0]}\n')
        return up


def read_bci(bci):
    """
    Bytes Description
    Bytes 0–3 The tile number.
    Bytes 4–7 The number of clusters in the tile.
    """
    header_fmt = "<L"
    fmt = "<L"
    with open(bci, "br") as f:
        BCI_version = struct.unpack(header_fmt, f.read(4))[0]
        n_tiles = struct.unpack(header_fmt, f.read(4))[0]

        sys.stdout.write(f'{BCI_version}\t{n_tiles}\n')
        s = 0
        itr = struct.iter_unpack(fmt, f.read())
        for idx, i in enumerate(itr, 1):
            if (idx - 1) % 2 == 0:
                s += i[0]
            sys.stdout.write(f'{idx}\t{i[0]}\n')
    print('{:,.0f}'.format(s))


# TODO this is needed for Miseq
# def make_bcl_folders(read_len, path):
#     base_path = os.path.join(path, "BaseCalls/L001/")
#     if not os.path.exists(base_path):
#         for i in range(read_len):
#             os.makedirs(os.path.join(base_path, f"C{i+1}.1"))
#     return
# TODO: split this function in half. First half nitializes folders
# Second half initializes the files
# TODO TEST
def make_lane_folders(path, n_lanes):
    base_path = os.path.join(path, "BaseCalls/")
    lanes = []
    for i in range(n_lanes):
        L = os.path.join(base_path, f"L{prepend_zeros_to_number(3, i+1)}")
        os.makedirs(L)
        lanes.append(L)
    return lanes


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
