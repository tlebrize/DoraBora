"""
   static function cryptPassword(var2, var3)
   {
      var var4 = "#1";
      var var5 = 0;
      while(var5 < var2.length)
      {
         var var6 = var2.charCodeAt(var5);
         var var7 = var3.charCodeAt(var5);
         var var8 = Math.floor(var6 / 16);
         var var9 = var6 % 16;
         var4 = var4 + (ank.utils.Crypt.HASH[(var8 + var7 % ank.utils.Crypt.HASH.length) % ank.utils.Crypt.HASH.length]
            + ank.utils.Crypt.HASH[(var9 + var7 % ank.utils.Crypt.HASH.length) % ank.utils.Crypt.HASH.length]);
         var5 = var5 + 1;
      }
      return var4;
   }
"""
import sys, math

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


print(crypt_password(sys.argv[1], sys.argv[2]))
