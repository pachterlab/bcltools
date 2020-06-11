import os

from .utils import prepend_zeros_to_number
from .BCLFile import BCLFile
from .LOCSFile import LOCSFile
from .FILTERFile import FILTERFile
from .utils import lane2num, parse_fastq_header
from collections import defaultdict
import gzip

from contextlib import ExitStack
import logging

logger = logging.getLogger(__name__)


class BCLFolderStructure(object):

    def __init__(
        self, n_lanes, n_cycles, reads_per_lane, machine_type, base_path
    ):

        intensities_path = "Data/Intensities"
        base_calls_path = os.path.join(intensities_path, "BaseCalls")

        self.n_lanes = n_lanes
        self.n_cycles = n_cycles
        self.reads_per_lane = reads_per_lane
        self.machine_type = machine_type
        self.base_path = base_path

        self.intensities_path = os.path.join(self.base_path, intensities_path)
        self.base_calls_path = os.path.join(self.base_path, base_calls_path)

        self.bcl_files = defaultdict(list)
        self.locs_files = defaultdict(list)
        self.filter_files = defaultdict(list)

    def base_calls_lane_path(self, lane_number):
        lane = f'L{prepend_zeros_to_number(3, lane_number)}'
        return os.path.join(self.base_calls_path, lane)

    def locs_lane_path(self, lane_number):
        lane = f'L{prepend_zeros_to_number(3, lane_number)}'
        return os.path.join(self.intensities_path, lane)

    def make_base_calls_lane_folders(self):
        base_path = self.base_calls_path
        lanes = []

        if self.machine_type == "nextseq":
            for i in range(self.n_lanes):
                L = os.path.join(
                    base_path, f"L{prepend_zeros_to_number(3, i+1)}"
                )
                os.makedirs(L)
                lanes.append(L)

        elif self.machine_type == "miseq":
            for n in range(self.n_lanes):
                for m in range(self.n_cycles):
                    L = os.path.join(
                        base_path, f"L{prepend_zeros_to_number(3, n+1)}",
                        f"C{m+1}.1"
                    )
                    os.makedirs(L)
                    lanes.append(L)

        elif self.machine_type == "novaseq":
            raise Exception("Novaseq is not supported yet.")

        return lanes

    # for locs files
    def make_intensities_lane_folders(self):
        base_path = self.intensities_path
        lanes = []
        for n in range(self.n_lanes):
            L = os.path.join(base_path, f"L{prepend_zeros_to_number(3, n+1)}")

            os.makedirs(L)
            lanes.append(L)
        return lanes

    def initialize_locs_files(self, lane, n_reads):
        lane_name = os.path.basename(lane)
        if self.machine_type == 'nextseq':
            path = os.path.join(lane, f's_{lane2num(lane_name)}.locs')
            locs = LOCSFile(path)
            locs.write_header_locs(n_reads)  # account for lanes
            self.locs_files[lane_name].append(locs)
        return

    def initialize_bcl_files(self, lane, n_reads):
        # perform action for one lane at a time
        if self.machine_type == 'nextseq':
            # need to fix gz
            for m in range(self.n_cycles):
                path = os.path.join(
                    lane, f'{prepend_zeros_to_number(4, m+1)}.bcl'
                )

                bcl = BCLFile(path)
                bcl.write_header_bcl(n_reads)

                self.bcl_files[os.path.basename(lane)].append(bcl)

        if self.machine_type == 'miseq':
            raise Exception('Not implemented yet :(')

        return

    def initialize_filter_files(self, lane, n_reads):
        lane_name = os.path.basename(lane)
        if self.machine_type == 'nextseq':
            path = os.path.join(lane, f's_{lane2num(lane_name)}.filter')
            filter_file = FILTERFile(path)
            filter_file.write_header_filter(n_reads)  # account for lanes
            self.filter_files[lane_name].append(filter_file)
        return

    # Super naive implementation
    def fastq2bcl(self, fastq_objects, reads_per_lane):
        seq_bool = False
        qual_bool = False
        coord_bool = False
        with ExitStack() as stack:
            infiles = [
                stack.enter_context(gzip.open(fastq.path))
                for fastq in fastq_objects
            ]
            # lane_counter = 0
            # lane = 'L001'
            for idx, lines in enumerate(zip(*infiles), 0):
                if idx % 1000 == 0:
                    logger.info(f"Wrote {idx//4} reads")
                if idx % 4 == 0:
                    # switch between each lane every iteration
                    # this is fine for now but needs to be changed
                    lane = f'L{prepend_zeros_to_number(3, (idx//4)%self.n_lanes + 1)}'

                    line = lines[0]
                    # should check that the headers are consistent
                    h = parse_fastq_header(line.strip().decode())

                    x = h['x']
                    y = h['y']

                    pass_filter = h['is_filtered_out']

                    coord_bool = True

                elif (idx - 1) % 4 == 0:
                    seqs = [seq.strip().decode() for seq in lines]
                    seq_bool = True

                elif (idx + 1) % 4 == 0:
                    quals = [qual.strip().decode() for qual in lines]
                    qual_bool = True

                if seq_bool and qual_bool and coord_bool:
                    seq_bool = False
                    qual_bool = False
                    coord_bool = False

                    # print(x, y)
                    # print(seqs)
                    # print(quals)

                    seq = "".join(seqs)
                    qual = "".join(quals)

                    for jdx, (b, q) in enumerate(zip(seq, qual)):
                        self.bcl_files[lane][jdx].write_record_bcl(
                            b, q, keep_open=True
                        )
                    self.locs_files[lane][0].write_record_locs(
                        x, y, keep_open=True
                    )

                    self.filter_files[lane][0].write_record_filter(
                        pass_filter, keep_open=True
                    )
            logger.info(f"Wrote {idx//4 + 1} reads")
