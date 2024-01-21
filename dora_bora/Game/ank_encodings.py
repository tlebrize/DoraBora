import string

BASE64 = string.ascii_letters + string.digits + "-_"


def ank_decode_cell(encoded):
    # maybe just a base64 decoding ?
    code = [0, 0]
    for index, value in enumerate(BASE64):  # index of
        if value == encoded[0]:
            code[0] = index * 64
        if value == encoded[1]:
            code[1] = index

    return sum(code)


def ank_encode_cell(decoded):
    return BASE64[decoded // 64] + BASE64[decoded % 64]
