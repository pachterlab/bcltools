import gzip


def parse_fastq_header(line):
    h = {}
    # @<instrument>:<run number>:<flowcell ID>:<lane>:<tile>:<x-pos>:<y-pos> \
    # <read>:<is filtered>:<control number>:<sample number>
    first, second = line.split(" ")
    first = first.split(':')
    second = second.split(':')

    h['instrument'] = first[0][1:]
    h['run_number'] = int(first[1])
    h['flowcell_ID'] = first[2]
    h['lane'] = int(first[3])
    h['tile'] = int(first[4])
    h['x'] = int(first[5])
    h['y'] = int(first[6])

    h['read'] = int(second[0])
    h['is_filtered'] = True if second[1] == 'Y' else False
    h['control_number'] = int(second[2])
    h['sample_number'] = int(second[3])

    return h


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
