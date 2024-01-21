import urllib.parse


def ank_is_map_crypted(map_data):
    nb = 0
    for c in map_data:
        if c.isdigit():
            nb += 1
    return nb > 1000


def ank_decrypt_raw_map_data(raw_map_data, key):
    # prepare key
    encoded_key = "".join([str(int(key[i : i + 2], 16)) for i in range(0, len(key), 2)])
    print(encoded_key)

    prepared_key = urllib.parse.unquote(encoded_key)
    print(prepared_key)

    # checksum key
    num = 0
    for i in range(len(key)):
        num += ord(key[i]) % 16
    checksum = int("0123456789ABCDEF"[(num % 16)], 16) * 2
    print(checksum)

    # decypher
    # StringBuilder dataToDecrypt = new StringBuilder();
    escaped = []
    num4 = len(raw_map_data) - 2
    i = 0
    while i <= num4:
        sub = raw_map_data[i : i + 2]
        num = int(sub, 16)
        s = round((i / 2) + checksum) % len(key)
        num2 = ord(key[s])
        escaped.append(str(num ^ num2))
        i += 2

    print("".join(escaped))
    # return unescape(dataToDecrypt.toString());
	assert False, 'this was never checked.'