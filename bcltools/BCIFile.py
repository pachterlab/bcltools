from .BinaryFile import BinaryFile


class BCIFile(BinaryFile):
    """
    Bci files contain one record per tile, which uses the following format:
    bytes 0-3: tile number
    bytes 4-7: number of clusters in the tile.
    Cluster numbers of one bci file sum to a cluster number listed in the beginning of each
    bcl.bgzf file of that lane.
    """

    def __init__(self, path, header_fmt="<II", record_fmt="<II", gzipped=False):
        super().__init__(path, header_fmt, record_fmt, gzipped=False)

        self.version_num = 0

    def read_header_bci(self):
        version_num, num_tiles = self.read_header()
        return ((version_num, num_tiles),)

    def read_record_bci(self, skip_header=True):
        for record in self.read_record(skip_header=skip_header):
            tile_num, num_clusters = record

            yield (tile_num, num_clusters)
