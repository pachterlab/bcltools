MACHINE_TYPES = (
    'nextseq',
    'miseq',
    'novaseq',
)

FILE_TYPES = ('bcl', 'bci', 'locs')

GZIPPED = {'nextseq': True, 'miseq': False, 'novaseq': True}

TYPE_LEN = {
    'c': 1,  # char
    'b': 1,  # signed char
    'B': 1,  # unsigned char
    '?': 1,  # bool
    'h': 2,  # short (int)
    'H': 2,  # unsigned short (int)
    'i': 4,  # int (int)
    'I': 4,  # unsigned int (int)
    'l': 4,  # long  (int)
    'L': 4,  # unsigned long (int)
    'q': 8,  # long long (int)
    'Q': 8,  # unsigned long long (int)
    'f': 4,  # float (float)
    'd': 8,  # double (float)
}

CHAR_ORDER = set('@=<>!')
