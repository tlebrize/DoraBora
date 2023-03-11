import string

BASE64 = string.ascii_letters + string.digits + "-_"


def decode_cell_b64(encoded):
    # maybe just a base64 decoding ?
    code = [0, 0]
    for index, value in enumerate(BASE64):  # index of
        if value == encoded[0]:
            code[0] = index * 64
        if value == encoded[1]:
            code[1] = index

    return sum(code)


def encode_cell_b64(decoded):
    return BASE64[decoded // 64] + BASE64[decoded % 64]


def get_int_by_hashed_value(c):
    for i, a in enumerate(BASE64):
        if a == c:
            return i
    return -1


def int_to_byte(value):
    return int.to_bytes(value)
    # return [bool((value >> i) & 1) for i in range(8)]


def decode_map_data(data):
    for chunk in [data[0 + i : 10 + i] for i in range(0, len(data), 10)]:
        cells = [int_to_byte(get_int_by_hashed_value(c)) for c in chunk]
        print(cells[2])
        walkable = (cells[2] & 56) >> 3
        print(walkable)
