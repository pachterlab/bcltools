import gzip


class FASTQFile(object):

    def __init__(self, path):

        self.path = path

    def n_reads(self):
        """Count the number of lines in a FASTQ file and divide by 4.
        Returns the number of reads"""
        with gzip.open(self.path, 'rb') as f:
            for lidx, l in enumerate(f, 1):
                pass
            return lidx // 4

    def read_len(self):
        """Get the length of a single FASTQ record"""
        with gzip.open(self.path, 'rb') as f:
            next(f)
            seq = f.readline().strip()
            return len(seq)
