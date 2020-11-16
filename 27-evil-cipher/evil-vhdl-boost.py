
import ctypes
import itertools
import math
import multiprocessing

from pyfinite import ffield

try:
    from evilnative import encrypt_one_block as encrypt_one_block_native
except:
    print('Please run "export PYTHONPATH=/path/to/evilnative.so"')
    import sys
    sys.exit(1)



class BitField():
    """Champ de bits avec ses accès."""

    def __init__(self, size, value):
        """Initialise un champ de bits."""

        self._size = size
        self._value = value & ((1 << size) - 1)


    @staticmethod
    def from_bytes(size, raw):
        """Construit un champ de bits à partir d'octets."""

        bf = BitField(size, 0)

        for i in range(len(raw)):
            for k in range(7, -1, -1):
                if raw[i] & (1 << k):
                    if size - 8 * (i + 1) + k >= 0:
                        bf[size - 8 * (i + 1) + k] = 1

        return bf


    def __int__(self):
        """Fournit de manière implicite la valeur sans accès au champ."""

        return self._value


    def __bytes__(self):
        """Fournit de manière implicite la valeur en octets sans accès au champ."""

        data = b''

        for i in range(0, 8 * (self._size // 8), 8):

            ch = 0

            for k in range(8):
                ch += (self[self._size - (i + 8) + k] << k)

            data += bytes([ ch ])

        return data


    def __str__(self):
        """Fournit une représentation textuelle du champ de bits."""

        dump = ''

        for i in range(self._size):
            dump += '1' if self[self._size - i - 1] else '0'

        return dump


    def get_size(self):
        """Indique la taille d'un champ de bits."""

        return self._size


    def _get_bit_indexes(self, key):
        """Transforme un accès en indice(s) d'accès."""

        if isinstance(key, slice):

            assert(key.step is None)
            indexes = [ i for i in range(key.start, key.stop + 1, 1) ]

        else:

            indexes = [ key ]

        assert(indexes[-1] < self._size)

        return indexes


    def __getitem__(self, key):
        """Fournit la valeur associée à une partie du champ de bits."""

        indexes = self._get_bit_indexes(key)

        mask = 0

        for i in indexes:
            mask |= (1 << i)

        item = (self._value & mask) >> indexes[0]

        return item


    def __setitem__(self, key, item):
        """Fournit la valeur associée à une partie du champ de bits."""

        item = int(item)

        indexes = self._get_bit_indexes(key)

        for i in indexes:

            if item & (1 << (i - indexes[0])):
                self._value |= (1 << i)
            else:
                #self._value &= ~(1 << i)
                if self._value & (1 << i):
                    self._value ^= (1 << i)


    def __xor__(self, other):
        """Calcule un "ou exclusif" entre deux champs de bits."""

        assert(self._size == other._size)

        return BitField(self._size, self._value ^ other._value)



class EvilCipher():
    """Chiffrement diabolique pour FPGA."""

    def __init__(self, key, legacy = False):
        """Met en place un moyen de chiffrement."""

        # Le polynôme "x^5 + x^2 + 1" est celui par défaut
        self._f = ffield.FField(5)

        assert(key.get_size() == 64)

        self._key = key
        self._iterations = 6

        self.encrypt_one_block = self.encrypt_one_block_legacy if legacy else encrypt_one_block_native


    @staticmethod
    def permutation15(in_block):
        """Réalise une opération de permutation sur 15 octets."""

        assert(in_block.get_size() == 15)

        out_block = BitField(15, 0)

        out_block[0] = in_block[7]
        out_block[1] = in_block[3]
        out_block[2] = in_block[13]
        out_block[3] = in_block[8]
        out_block[4] = in_block[12]
        out_block[5] = in_block[10]
        out_block[6] = in_block[2]
        out_block[7] = in_block[5]
        out_block[8] = in_block[0]
        out_block[9] = in_block[14]
        out_block[10] = in_block[11]
        out_block[11] = in_block[9]
        out_block[12] = in_block[1]
        out_block[13] = in_block[4]
        out_block[14] = in_block[6]

        return out_block


    @staticmethod
    def permutation(in_block):
        """Réalise une opération de permutation sur 45 octets."""

        assert(in_block.get_size() == 45)

        out_block = BitField(45, 0)

        out_block[ 0:14] = EvilCipher.permutation15(BitField(15, in_block[15:29]))
        out_block[15:29] = EvilCipher.permutation15(BitField(15, in_block[30:44]))
        out_block[30:44] = EvilCipher.permutation15(BitField(15, in_block[ 0:14]))

        return out_block


    @staticmethod
    def permutation15_inv(in_block):
        """Réalise l'inverse d'une opération de permutation sur 15 octets."""

        assert(in_block.get_size() == 15)

        out_block = BitField(15, 0)

        out_block[0] = in_block[8]
        out_block[1] = in_block[12]
        out_block[2] = in_block[6]
        out_block[3] = in_block[1]
        out_block[4] = in_block[13]
        out_block[5] = in_block[7]
        out_block[6] = in_block[14]
        out_block[7] = in_block[0]
        out_block[8] = in_block[3]
        out_block[9] = in_block[11]
        out_block[10] = in_block[5]
        out_block[11] = in_block[10]
        out_block[12] = in_block[4]
        out_block[13] = in_block[2]
        out_block[14] = in_block[9]

        return out_block


    @staticmethod
    def permutation_inv(in_block):
        """Réalise une opération de permutation sur 45 octets."""

        assert(in_block.get_size() == 45)

        out_block = BitField(45, 0)

        out_block[ 0:14] = EvilCipher.permutation15_inv(BitField(15, in_block[30:44]))
        out_block[15:29] = EvilCipher.permutation15_inv(BitField(15, in_block[ 0:14]))
        out_block[30:44] = EvilCipher.permutation15_inv(BitField(15, in_block[15:29]))

        return out_block


    @staticmethod
    def expand_key(init, prev):
        """Calcule la clef pour un tour donné."""

        load = (prev == None)

        reg = BitField(64, 0)

        for i in range(64):

            if i == 0:
                reg[0] = init[0] if load else prev[63]

            elif i in [ 9, 34, 61 ]:
                reg[i] = init[i] if load else (prev[i - 1] ^ prev[63])

            else:
                reg[i] = init[i] if load else prev[i - 1]
                #reg[8] = 0

        return reg, BitField(45, int(reg))


    def do_round(self, in_block, key):
        """Effectue un tour de chiffrement."""

        assert(in_block.get_size() == 45)
        assert(key.get_size() == 45)

        tmp = EvilCipher.permutation(in_block)

        for i in range(9):
            tmp[5 * i : 5 * i + 4] = self._f.Inverse(tmp[5 * i : 5 * i + 4])

        tmp = tmp ^ key

        out_block = BitField(45, 0)

        for i in range(3):

            out_block[15 * i : 15 * i + 4] = tmp[15 * i : 15 * i + 4] \
                                             ^ tmp[15 * i + 5 : 15 * i + 9] \
                                             ^ self._f.Multiply(tmp[15 * i + 10 : 15 * i + 14], 0b00010)

            out_block[15 * i + 5 : 15 * i + 9] = tmp[15 * i : 15 * i + 4] \
                                                 ^ self._f.Multiply(tmp[15 * i + 5 : 15 * i + 9], 0b00010) \
                                                 ^ tmp[15 * i + 10 : 15 * i + 14]
       
            out_block[15 * i + 10 : 15 * i + 14] = self._f.Multiply(tmp[15 * i : 15 * i + 4], 0b00010) \
                                                   ^ tmp[15 * i + 5 : 15 * i + 9] \
                                                   ^ tmp[15 * i + 10 : 15 * i + 14]

        return out_block


    def encrypt_one_block_legacy(self, in_block):
        """Réalise le chiffrement d'un bloc."""

        # Phase de chargement (load = 1)

        reg, rkey = EvilCipher.expand_key(self._key, None)
        assert(int(reg) == int(self._key))

        reg_data = BitField(45, int(in_block))

        # Fronts montants

        for ctr in range(self._iterations):

            if ctr == 0:

                reg_data = rkey ^ reg_data

            else:

                reg_data = self.do_round(reg_data, rkey)

            reg, rkey = EvilCipher.expand_key(None, reg)

        return reg_data


    def encrypt(self, in_blocks):
        """Réalise le chiffrement de blocs."""

        encrypted = BitField(in_blocks._size, 0)

        for i in range(in_blocks._size - 1, -1, -45):

            in_block = BitField(45, in_blocks[i - 44 : i])

            out_block = self.encrypt_one_block(in_block)

            encrypted[i - 44 : i] = int(out_block)

        return encrypted


    def do_round_inv(self, in_block, key):
        """Effectue un tour de chiffrement."""

        assert(in_block.get_size() == 45)
        assert(key.get_size() == 45)

        tmp = BitField(45, int(in_block))

        # TODO

        return tmp


    def decrypt_one_block(self, in_block):
        """Réalise le déchiffrement d'un bloc."""

        # Phase de chargement (load = 1)

        reg, rkey = EvilCipher.expand_key(self._key, None)
        assert(int(reg) == int(self._key))

        reg_data = BitField(45, int(in_block))

        # Fronts montants

        for ctr in range(self._iterations):

            if ctr == (self._iterations - 1):

                reg_data = rkey ^ reg_data

            else:

                reg_data = self.do_round_inv(reg_data, rkey)

            reg, rkey = EvilCipher.expand_key(None, reg)

        return reg_data



def test_implementation():
    """Effectue une série de tests."""

    # Champs de bits

    tmp = BitField(45, 3)

    assert(tmp[2:14] == 0)

    tmp[3:4] = 3

    assert(tmp[2:14] == 6)

    tmp[3:5] = 7

    assert(tmp[2:14] == 14)

    assert(tmp[1] == 1)

    # Permutation 15

    tmp = BitField(15, 25760)

    p15 = EvilCipher.permutation15(tmp)

    inv = EvilCipher.permutation15_inv(p15)

    assert(tmp[0:14] == inv[0:14])

    # Permutation

    tmp = BitField(45, 0x1ff4ef0ffbf3)

    p = EvilCipher.permutation(tmp)

    inv = EvilCipher.permutation_inv(p)

    assert(tmp[0:44] == inv[0:44])

    assert((tmp[0:44] ^ inv[0:44]) == 0)

    # Conversion

    orig = b'evil'
    plain = '011001010111011001101001011011000000000000000'

    txt = BitField.from_bytes(45, orig)

    assert(str(txt) == plain)

    assert(bytes(txt)[:len(orig)].decode('ascii') == orig.decode('ascii'))

    # Preuve de concept

    key = BitField(64, 0x4447534553494545)

    cipher = EvilCipher(key)

    plain = BitField.from_bytes(45, b'evil')

    enc = cipher.encrypt_one_block(plain)

    print('Encypted:', str(enc))

    expected = '000101110010110001110101010111010101001010100'

    print('Expected:', expected)

    print(str(enc) == expected)

    dec = cipher.decrypt_one_block(enc)

    print('Decypted:', str(dec))

    print('Expected:', str(plain))

    print(str(dec) == str(plain))



class EvilCracker(multiprocessing.Process):
    """Cracker pour le chiffrement Evil."""

    _alpha = bytes([ (0x61 + c) for c in range(6) ])
    _num = bytes([ (0x30 + c) for c in range(10) ])

    _charset = _alpha + _num

    _line_2 = '010111101111101000100001111000001001100111111101111010000011100111100000101100010101000110100000000011101101111110010100111111101100110001110100110101101111100111001011110110100011101100111001000111101110101010110111011110010100010000011111101011101110101111110100111011110100100100111001010001010101001011001010100110101000010110000000101101100000101000011000101111110100111100000100110101001010100110011111011101001110110010011100011000100110000011'


    @classmethod
    def complete_last_block(cls, index, known, prev_bits = None):
        """Organise l'attaque d'un bloc chiffré pour terminer un ensemble connu."""

        starting_bit_index = index * 45

        expected = cls._line_2[starting_bit_index : starting_bit_index + 45]

        print('[i] Looking for block %u:' % index, expected)

        known_bits_count = len(known) * 8

        required_bits_count = (index + 1) * 45

        missing_chars = math.ceil((required_bits_count - known_bits_count) / 8)

        extra_for_next_time = (required_bits_count - known_bits_count) % 8

        print('[i] %u characters are missing (at least), %u bits will be guessed for next block' % \
              (missing_chars, extra_for_next_time))

        guessed_chars = None
        extra_bits = None

        last_percent = None

        counter = 0
        max_loops = len(cls._charset) ** missing_chars

        for p in itertools.product(cls._charset, repeat=missing_chars):

            counter += 1

            cur_percent = int((counter * 100) / max_loops)

            if last_percent != cur_percent:
                print('[*] Processing %u / %u: %u %%' % (counter, max_loops, cur_percent), end='\r')
                last_percent = cur_percent

            key = BitField(64, 0x4447534553494545)
            cipher = EvilCipher(key)

            extra = bytes(p)

            plain = BitField.from_bytes(required_bits_count, known + extra)

            part = BitField(45, plain[0:44])

            enc = cipher.encrypt_one_block(part)

            if str(enc) == expected:

                reliable = int((required_bits_count - known_bits_count) / 8)
                guessed_chars = extra[:reliable]

                print()

                if extra_for_next_time > 0:
                    extra_bits = part[0 : extra_for_next_time - 1]
                    print('[i] New guess:', guessed_chars, '(extra bits: %02x)' % extra_bits)

                else:
                    print('[i] New guess:', guessed_chars)

                break

        print()

        return guessed_chars, { 'size' : extra_for_next_time, 'value' : extra_bits }


    def __init__(self, index, stop, known, fixed, suffix = b''):
        """Prépare une attaque sur un ensemble de caractères."""

        super(EvilCracker, self).__init__()

        # Caractérisation de la cible de l'attaque

        self._index = index

        self._stop = stop

        self._known = known

        self._fixed_first_char = fixed
        self._fixed_suffix = suffix

        # Affichage des statistiques ?

        self._main_thread = False

        # Résultats conservés

        # 45 bits = 1 + 40 + 4 = 7 caractères au max

        self._guessed_chars = multiprocessing.Array(ctypes.c_char, 7)
        self._guessed_size = multiprocessing.Value(ctypes.c_ubyte, -1)

        self._extra_bits = multiprocessing.Value(ctypes.c_ubyte, -1)
        self._extra_size = multiprocessing.Value(ctypes.c_ubyte, -1)


    @classmethod
    def run_brute_force(cls, index, known, prev_bits = None, suffix = b''):
        """Organise l'attaque d'un bloc chiffré pour terminer un ensemble connu."""

        pool = []

        stop = multiprocessing.Value('i', 0)

        for c in cls._charset:

            th = EvilCracker(index, stop, known, bytes([ c ]), suffix)

            if th.check_run(prev_bits):

                pool.append(th)

                if len(pool) == 1:
                    th.mark_as_main()

        print('[i] Threads ready to run: %u' % len(pool))

        for th in pool:

            th.start()

        guessed = None
        extra = None

        for th in pool:

            th.join()

            guessed, extra = th.get_results()

            if not(guessed is None):
                break

        return guessed, extra


    def check_run(self, prev_bits):
        """Valide que les derniers bits trouvés sont bien conformes avec l'espace visé."""

        if prev_bits is None:

            status = True

        else:

            known_bits_count = len(self._known) * 8

            required_bits_count = (self._index + 1) * 45

            missing_chars = math.ceil((required_bits_count - known_bits_count) / 8)

            sample = known + self._fixed_first_char + (b'X' * missing_chars)

            plain = BitField.from_bytes(required_bits_count, sample)

            last_known = plain[45 : 45 + prev_bits['size']] & ((1 << prev_bits['size']) - 1)

            print(' > next:', self._fixed_first_char,
                  'last:', hex(last_known), 'bsize:', prev_bits['size'],
                  'value:', hex(prev_bits['value']))

            status = (last_known == prev_bits['value'])

        return status


    def mark_as_main(self):
        """Définit le thread comme étant le principal pour l'affichage."""

        self._main_thread = True


    def run(self):
        """Lance une attaque sur un ensemble de caractères."""

        starting_bit_index = self._index * 45

        expected = self._line_2[starting_bit_index : starting_bit_index + 45]

        if self._main_thread:
            print('[i] Looking for block %u:' % self._index, expected)

        known_bits_count = len(self._known) * 8

        required_bits_count = (self._index + 1) * 45

        missing_chars = math.ceil((required_bits_count - known_bits_count) / 8)

        extra_for_next_time = (required_bits_count - known_bits_count) % 8

        if self._main_thread:
            print('[i] %u characters are missing (at least), %u bits will be guessed for next block' % \
                  (missing_chars, extra_for_next_time))

        last_percent = None

        counter = 0
        product_repeat = missing_chars - 1 - len(self._fixed_suffix)
        max_loops = len(self._charset) ** product_repeat

        key = BitField(64, 0x4447534553494545)
        cipher = EvilCipher(key)

        for p in itertools.product(self._charset, repeat=product_repeat):

            if counter % 50000 == 0:
                if self._stop.value:
                    break

            counter += 1

            if self._main_thread:

                cur_percent = int((counter * 10000) / max_loops)

                if last_percent != cur_percent:
                    print('[*] Processing %u / %u: %.02f %%' % \
                          (counter, max_loops, cur_percent / 100), end='\r')
                    last_percent = cur_percent

            extra = bytes(p)

            plain = BitField.from_bytes(required_bits_count, known + self._fixed_first_char + extra + self._fixed_suffix)

            part = BitField(45, plain[0:44])

            enc = cipher.encrypt_one_block(part)

            if str(enc) == expected:

                reliable = int((required_bits_count - known_bits_count - 8) / 8)

                self._guessed_chars.raw = self._fixed_first_char + extra[:reliable]
                self._guessed_size.value = 1 + reliable

                print()

                if extra_for_next_time > 0:

                    self._extra_bits.value = part[0 : extra_for_next_time - 1]
                    self._extra_size.value = extra_for_next_time

                    print('[i] New guess:', self._guessed_chars.raw[:self._guessed_size.value],
                          '(start: \'%s\') ' % chr(self._fixed_first_char[0]),
                          '(extra bits: %02x - size: %u)' % \
                          (self._extra_bits.value, self._extra_size.value))

                else:

                    print('[i] New guess:', self._guessed_chars.raw[:self._guessed_size.value],
                          '(start: \'%s\')' % chr(self._fixed_first_char[0]))

                self._stop.value = 1
                #break

        if self._main_thread:
            print()


    def get_results(self):
        """Fournit les éventuels résultats de la cryptanalyse."""

        if self._guessed_size.value != 0xff:

            guessed = self._guessed_chars.raw[:self._guessed_size.value]

        else:

            guessed = None

        if self._extra_size.value != 0xff:

            extra_bits = { 'size' : self._extra_size.value, 'value' : self._extra_bits.value }

        else:

            extra_bits = None

        return guessed, extra_bits



if __name__ == '__main__':
    """Point d'entrée du programme."""

    #test_implementation()

    #import sys
    #sys.exit()

    base = b'DGSESIEE{'

    known = base

    #guessed, extra = EvilCracker.complete_last_block(1, known)

    guessed = b'66'
    extra = { 'size' : 2, 'value' : 0x0 }

    # known = DGSESIEE{xx<'>
    known += guessed

    #guessed, extra = EvilCracker.run_brute_force(2, known, extra)

    guessed = b'6bcd5'
    extra = { 'size' : 7, 'value' : 0x1a }

    known += guessed

    # Suivant : 4 ou 5 (0b0011010x)
    known += b'4'
    extra = None

    #guessed, extra = EvilCracker.run_brute_force(3, known, extra)

    guessed = b'62620'
    extra = { 'size' : 4, 'value' : 0x03 }

    known += guessed

    # Suivant : [0-9] (0b0011xxxx)
    #known += b'9'
    #extra = None

    #guessed, extra = EvilCracker.run_brute_force(4, known, extra)

    guessed = b'348265'
    extra = { 'size' : 1, 'value' : 0x0 }

    known += guessed

    #guessed, extra = EvilCracker.run_brute_force(5, known, extra)

    guessed = b'78452'
    extra = { 'size' : 6, 'value' : 0x19 }

    known += guessed

    #guessed, extra = EvilCracker.run_brute_force(6, known, extra)

    guessed = b'ffa448'
    extra = { 'size' : 3, 'value' : 0x1 }

    known += guessed

    #guessed, extra = EvilCracker.run_brute_force(7, known, extra)

    guessed = b'763b31'
    extra = None

    known += guessed

    guessed, extra = EvilCracker.run_brute_force(8, known, extra)

    guessed = b'01014'
    extra = { 'size' : 5, 'value' : 0x6 }

    known += guessed

    print('Known:', known, len(known))






    for i in range(128):

        print('----', i, hex(i))

        # if i <= 47:
        #     continue
        if i in range(0x30, 0x40):
            continue
        if i in range(0x41, 0x5b):
            continue
        if i in range(0x61, 0x7b):
            continue

        extra = { 'size' : 5, 'value' : 0x6 }

        guessed, extra = EvilCracker.run_brute_force(9, known, extra, b'}' + 3 * bytes([ i ]))

        if guessed:
            break


