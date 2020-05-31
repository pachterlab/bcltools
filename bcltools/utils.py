

def prepend_zeros_to_number(len_name, number):
    len_number = len(str(number))
    return '0'*(len_name-len_number) + str(number)