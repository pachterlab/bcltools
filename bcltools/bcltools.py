from .BCLFolderStructure import BCLFolderStructure
from .FASTQFile import FASTQFile
from .BCLFile import BCLFile
from .BCIFile import BCIFile
from .LOCSFile import LOCSFile
from .FILTERFile import FILTERFile
from .utils import (clean_pipe, split_reads)
from .config import COMPRESSION

import logging

logger = logging.getLogger(__name__)


def bclwrite(bcl_path, infile):
    # gzipped = GZIPPED.get(technology.lower(), False)
    # gzipped doesnt do anything for now but it should
    # affect whether the bcl file is gzipped
    out_bcl = BCLFile(bcl_path)
    out_bcl.write_header_bcl(0)
    out_bcl.write_from_stream_bcl(infile)
    infile.close()

    return


def bclread(bcl_path, technology, head=False):
    bcl = BCLFile(bcl_path, compression=COMPRESSION[technology])

    if head:
        return clean_pipe(bcl.read_header_bcl)
    elif not head:
        return clean_pipe(bcl.read_record_bcl)


def locsread(locs_path, head=False):
    locs_file = LOCSFile(locs_path)

    if head:
        clean_pipe(locs_file.read_header_locs)
    elif not head:
        clean_pipe(locs_file.read_record_locs)


def locswrite(locs_path, infile):
    locs = LOCSFile(locs_path)
    locs.write_header_locs(0)
    locs.write_from_stream_locs(infile)
    infile.close()
    return


def filterread(filter_path, head=False):
    filter_file = FILTERFile(filter_path)

    if head:
        clean_pipe(filter_file.read_header_filter)
    elif not head:
        clean_pipe(filter_file.read_record_filter)


def filterwrite(filter_path, infile):
    filter_file = FILTERFile(filter_path)

    filter_file.write_header_filter(0)
    filter_file.write_from_stream_filter(infile)
    infile.close()
    return


def bciread(bci_path, head=False):
    bci_file = BCIFile(bci_path)

    if head:
        clean_pipe(bci_file.read_header_bci)
    elif not head:
        clean_pipe(bci_file.read_record_bci)


def bclconvert(n_lanes, machine_type, base_path, fastqs):

    fastq_objects = [FASTQFile(path) for path in fastqs]
    logger.info(f"Number of FASTQ Files {len(fastq_objects)}")

    logger.info("Counting number of cycles")
    n_cycles = sum([fastq.read_len() for fastq in fastq_objects])

    logger.info("Counting number of reads")
    n_reads = fastq_objects[0].n_reads()

    reads_per_lane = split_reads(n_reads, n_lanes)

    folder_structure = BCLFolderStructure(
        n_lanes, n_cycles, reads_per_lane, machine_type, base_path
    )

    # initialize the BaseCalls/L00X folders
    logger.info("Initializing BCL Folder structure")
    lanes_bcls = folder_structure.make_base_calls_lane_folders()
    lanes_locs = folder_structure.make_intensities_lane_folders()

    # initialize locs and bcl files
    # TODO fix the pluralization of words, its confusing
    logger.info("Initializing LOCS and BCL files")
    for idx, (lane_locs, lane_bcl) in enumerate(zip(lanes_locs, lanes_bcls)):
        folder_structure.initialize_locs_files(lane_locs, reads_per_lane[idx])
        folder_structure.initialize_bcl_files(lane_bcl, reads_per_lane[idx])
        # filter is in same folder as bcl
        folder_structure.initialize_filter_files(lane_bcl, reads_per_lane[idx])

    # Do the transpose
    logger.info('Writing records to LOCS and BCL files')

    folder_structure.fastq2bcl(fastq_objects, reads_per_lane)

    return
