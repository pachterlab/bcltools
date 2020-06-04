import os

from .utils import prepend_zeros_to_number


class BCLFolderStructure(object):

    def __init__(self, n_lanes, machine_type, base_path):

        intensities_path = "Data/Intensities"
        base_calls_path = os.path.join(intensities_path, "BaseCalls")

        self.machine_type = machine_type

        self.base_path = base_path

        self.intensities_path = os.path.join(self.base_path, intensities_path)
        self.base_calls_path = os.path.join(self.base_path, base_calls_path)

        self.bcl_files = []
        self.locs_files = []

    def set_n_cycles(self, n_cycles):
        self.n_cycles = n_cycles

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
