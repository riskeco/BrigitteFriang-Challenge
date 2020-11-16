from Crypto.Cipher import AES
key = "AES 256 ECB                     "
print(key)
cipher = AES.new(key, AES.MODE_ECB)

with open("archive_chiffree", "rb") as f:
    msg = f.read()

plain = cipher.decrypt(msg)

with open("plain_archive", "wb") as w:
    w.write(plain)
