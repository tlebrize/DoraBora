import math

HASH = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"


def crypt_password(password, key):
    hash_len = len(HASH)
    out = "#1"
    i = 0
    while i < len(password):
        pass_i = ord(password[i])
        key_i = ord(key[i])
        pass_floor = math.floor(pass_i // 16)
        pass_mod = pass_i % 16
        out += HASH[(pass_floor + key_i % hash_len) % hash_len] + HASH[(pass_mod + key_i % hash_len) % hash_len]
        i += 1
    return out
