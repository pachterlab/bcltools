import os

from .utils import prepend_zeros_to_number
from .BCLFile import BCLFile

from collections import defaultdict


class BCLFolderStructure(object):

    def __init__(self, n_lanes, n_cycles, n_reads, machine_type, base_path):

        intensities_path = "Data/Intensities"
        base_calls_path = os.path.join(intensities_path, "BaseCalls")

        self.n_lanes = n_lanes
        self.n_cycles = n_cycles
        self.n_reads = n_reads
        self.machine_type = machine_type
        self.base_path = base_path

        self.intensities_path = os.path.join(self.base_path, intensities_path)
        self.base_calls_path = os.path.join(self.base_path, base_calls_path)

        self.bcl_files = defaultdict(list)
        self.locs_files = []

    def set_n_cycles(self, n_cycles):
        self.n_cycles = n_cycles

    def set_n_reads(self, n_reads):
        self.n_reads = n_reads

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

    def initialize_bcl_files(self, lane):
        # perform action for one lane at a time
        if self.machine_type == 'nextseq':
            for m in range(self.n_cycles):
                path = os.path.join(
                    lane, f'{prepend_zeros_to_number(4, m+1)}.bcl.gz'
                )

                bcl = BCLFile(path, self.machine_type)
                bcl.write_header(self.n_reads, close=True)

                self.bcl_files[os.path.basename(lane)].append(bcl)

        if self.machine_type == 'miseq':
            raise Exception('Not implemented yet :(')

        return
