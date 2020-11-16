
import base64
import sys

from Crypto.Cipher import AES


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Usage: %s <file.evil>' % sys.argv[0])
        sys.exit(1)

    key = base64.b64decode('RXZpbERlZmF1bHRQYXNzIQ==')
    iv = bytes([ 0, 1, 0, 3, 5, 3, 0, 1, 0, 0, 2, 0, 6, 7, 6, 0 ])

    print('[i] Using key:', key)

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    with open(sys.argv[1], 'rb') as fd:
        enc = fd.read()

    dec = cipher.decrypt(enc)

    #from Crypto.Util import Padding
    #dec = Padding.unpad(dec, 192)

    with open(sys.argv[1] + '.orig', 'wb') as fd:
        fd.write(dec)

    print('[i] Decrypted %u bytes' % len(dec))
