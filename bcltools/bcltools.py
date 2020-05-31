import struct
import sys
import gzip
import os

from .utils import (prepend_zeros_to_number)

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


def get_n_reads(fastq):
    """Count the number of lines in a FASTQ file and divide by 4.
    Returns the number of reads"""
    with gzip.open(fastq, 'rb') as f:
        for lidx, l in enumerate(f, 1):
            pass
        return lidx // 4


def get_read_len(fastq):
    """Get the length of a single FASTQ record"""
    with gzip.open(fastq, 'rb') as f:
        next(f)
        seq = f.readline().strip()
        return len(seq)


# TODO this is needed for Miseq
# def make_bcl_folders(read_len, path):
#     base_path = os.path.join(path, "BaseCalls/L001/")
#     if not os.path.exists(base_path):
#         for i in range(read_len):
#             os.makedirs(os.path.join(base_path, f"C{i+1}.1"))
#     return


# TODO: split this function in half. First half initializes folders
# Second half initializes the files
def make_bcl_files(path, read_len, n_reads):
    """
    Create initialized bcl files. There are read_len number of bcl files.
    Each has a header corresponding to the number of reads.
    """
    bcls = []
    header_fmt = "<i"
    header = struct.pack(header_fmt, n_reads)

    base_path = os.path.join(path, "BaseCalls/L001/")
    if not os.path.exists(base_path):
        os.makedirs(base_path)
        for i in range(read_len):
            bcl_name = f"{prepend_zeros_to_number(4, i+1)}.bcl"
            bcl_path = os.path.join(base_path, bcl_name)
            bcls.append(bcl_path)
            with open(bcl_path, 'wb') as f:
                f.write(header)
    return bcls


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


def write_seqs_quals(fastq, bcls):
    """
    Parse FASTQ file and write all records to their respective bcl file.
    """
    seq_bool = False
    qual_bool = False
    with gzip.open(fastq, 'rb') as f:
        next(f)

        for lidx, l in enumerate(f, 0):
            if lidx % 4 == 0:
                seq = l.strip().decode()
                seq_bool = True

            elif (lidx + 2) % 4 == 0:
                qual = l.strip().decode()
                qual_bool = True

            if seq_bool and qual_bool:
                seq_bool = False
                qual_bool = False

                for idx, (b, q) in enumerate(zip(seq, qual)):
                    write_bcl_record(b, q, bcls[idx])

    return


def fastq2bcl(path, fastq):
    read_len = get_read_len(fastq)
    n_reads = get_n_reads(fastq)
    # make_bcl_folders(read_len, path) # not needed for nextseq
    bcls = make_bcl_files(path, read_len, n_reads)
    write_seqs_quals(fastq, bcls)


num2base = {0: "A", 1: "C", 2: "G", 3: "T"}


def bcl2fastq(file_path):
    header_fmt = "<i"
    seq_fmt = "<B"

    with open(file_path, "br") as f:
        up = struct.unpack(header_fmt, f.read(4))
        print(up)
        itr = struct.iter_unpack(seq_fmt, f.read())
        for idx, i in enumerate(itr):
            base = num2base.get(3 & i[0], 0)
            qual = i[0] >> 2
            sys.stdout.write(f'{bin(i[0])}\t{base}\t{qual}\n')

    return
