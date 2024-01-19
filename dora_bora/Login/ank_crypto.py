def ank_decrypt(password_hash, key):  # Stolen from StarLoco
    dictionary = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    decrypted = []

    for i in range(0, len(password_hash), 2):
        PKey = key[i // 2]
        ANB = dictionary.index(password_hash[i])
        ANB2 = dictionary.index(password_hash[i + 1])

        somme1 = ANB + len(dictionary)
        somme2 = ANB2 + len(dictionary)

        APass = somme1 - ord(PKey)
        if APass < 0:
            APass += 64
        APass *= 16

        AKey = somme2 - ord(PKey)
        if AKey < 0:
            AKey += 64

        PPass = chr(APass + AKey)

        decrypted.append(PPass)

    return "".join(decrypted)
