import binascii


def is_gz_file(filepath):
    with open(filepath, 'rb') as test_f:
        return binascii.hexlify(test_f.read(2)) == b'1f8b'


def prepend_zeros_to_number(len_name, number):
    len_number = len(str(number))
    return '0' * (len_name - len_number) + str(number)
