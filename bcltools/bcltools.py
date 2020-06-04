# import gzip
# import os

# from .utils import prepend_zeros_to_number
# from .fastq_utils import (get_n_reads, get_read_len)
# # from .bcl_utils import (write_bcl_header, write_bcl_record, read_bcl)

# from .BCLFile import BCLFile

# def make_bcl_files(path, lane_num, read_len, n_reads):
#     """
#     Create initialized bcl files. There are read_len number of bcl files.
#     Each has a header corresponding to the number of reads.
#     """
#     bcls = []

#     base_path = os.path.join(path, "BaseCalls/L001/")

#     os.makedirs(base_path, exist_ok=True)
#     for i in range(read_len):
#         bcl_name = f"{prepend_zeros_to_number(4, i+1)}.bcl"
#         bcl_path = os.path.join(base_path, bcl_name)
#         BCLFile(bcl_path, )
#         bcls.append(bcl_path)

#         write_bcl_header(n_reads, bcl_path)

#     return bcls

# def write_seqs_quals(fastq, bcls):
#     """
#     Parse FASTQ file and write all records to their respective bcl file.
#     """
#     seq_bool = False
#     qual_bool = False
#     pos_bool = True
#     with gzip.open(fastq, 'rb') as f:
#         for lidx, l in enumerate(f, 0):
#             if lidx % 4 == 0:
#                 # h = parse_fastq_header(l.strip().decode())

#                 # x = h['x']
#                 # y = h['y']

#                 pos_bool = True

#             elif (lidx - 1) % 4 == 0:
#                 seq = l.strip().decode()
#                 seq_bool = True

#             elif (lidx + 1) % 4 == 0:
#                 qual = l.strip().decode()
#                 qual_bool = True

#             if seq_bool and qual_bool and pos_bool:
#                 seq_bool = False
#                 qual_bool = False
#                 pos_bool = False

#                 # print(x, y)
#                 # print(seq)
#                 # print(qual)

#                 for idx, (b, q) in enumerate(zip(seq, qual)):
#                     write_bcl_record(b, q, bcls[idx])

#     return

# def write_seqs_quals_3(fastqs, bcls):
#     """
#     Parse FASTQ file and write all records to their respective bcl file.
#     """
#     seq_bool = False
#     qual_bool = False
#     with gzip.open(fastqs[0], 'rb') as f1:
#         with gzip.open(fastqs[1], 'rb') as f2:
#             with gzip.open(fastqs[2], 'rb') as f3:
#                 next(f1)
#                 next(f2)
#                 next(f3)

#                 for lidx, (l1, l2, l3) in enumerate(zip(f1, f2, f3), 0):
#                     if lidx % 4 == 0:
#                         seq1 = l1.strip().decode()
#                         seq2 = l2.strip().decode()
#                         seq3 = l3.strip().decode()

#                         seq = seq1 + seq2 + seq3

#                         seq_bool = True

#                     elif (lidx + 2) % 4 == 0:
#                         qual1 = l1.strip().decode()
#                         qual2 = l2.strip().decode()
#                         qual3 = l3.strip().decode()

#                         qual = qual1 + qual2 + qual3

#                         qual_bool = True

#                     if seq_bool and qual_bool:
#                         seq_bool = False
#                         qual_bool = False

#                         for idx, (b, q) in enumerate(zip(seq, qual)):
#                             write_bcl_record(b, q, bcls[idx])

#     return

# def fastq2bcl(path, fastqs):
#     # Read length should be the same in all fastqs
#     read_lens = []
#     n_reads = []
#     for f in fastqs:
#         read_lens.append(get_read_len(f))
#         n_reads.append(get_n_reads(f))

#     assert len(set(n_reads)) == 1, "Fastq files have different lengths."

#     n_reads = set(n_reads).pop()
#     read_len = sum(read_lens)

#     # make_bcl_folders(read_len, path) # not needed for nextseq
#     bcls = make_bcl_files(path, read_len, n_reads)
#     if len(fastqs) == 3:
#         write_seqs_quals_3(fastqs, bcls)
#     elif len(fastqs) == 1:
#         write_seqs_quals(fastqs[0], bcls)

# def bcl2fastq(bcl, header=False):
#     read_bcl(bcl)

#     return
