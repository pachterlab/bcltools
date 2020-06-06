import argparse
import binascii


def check_gz_file(file):
    with open(file, 'rb') as test_f:
        is_gz = binascii.hexlify(test_f.read(2)) == b'1f8b'
    if not is_gz:
        raise argparse.ArgumentTypeError('FASTQ file must be gz')
    return file


def check_lane_lim(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(
            f"{value} is an invalid positive int value"
        )
    elif ivalue >= 5:
        raise argparse.ArgumentTypeError("The maximum number of lanes is 4")
    return ivalue


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(
            f"{value} is an invalid positive int value"
        )
    return ivalue
