
# pip3 install --user pypng

import png


def to_binary(val, size):
    """Convertit une valeur en suite de 0 et 1."""

    return bin(val)[2:].zfill(size)


def image_to_binary(img):
    """Transpose une image en données chiffrées."""

    width, height, pixels, info = img.read_flat()

    print('[i] Size: %u x %u' % (width, height))

    pixel_byte_width = 4 if info['alpha'] else 3

    print('[i] Pixel width:', pixel_byte_width)

    offset_data_size = width * height * 8 * 3

    print('[i] Offset data size:', offset_data_size)

    data_size_bit = len(bin(offset_data_size)[2:])

    print('[i] Data size bit:', data_size_bit)

    data = ''

    for y in range(height):
        for x in range(width):

            pos = (x + y * width) * pixel_byte_width

            r, g, b, a = pixels[pos:pos+4]

            data += to_binary(r, 8)
            data += to_binary(g, 8)
            data += to_binary(b, 8)

    return data_size_bit, data


def read_offsets(data_size_bit, data):
    """Retrouve les localisations des bribes de texte."""

    header = data[: 2 * data_size_bit]

    offset_array = int(data[:data_size_bit], 2)

    print('[i] Offset array:', offset_array)

    length_size_bit = int(data[data_size_bit : 2 * data_size_bit], 2)

    print('[i] Length size bit:', length_size_bit)

    locations = data[2 * data_size_bit:]

    offsets = []

    main_offset = round(len(data) / 4)

    for i in range(offset_array):

        start = i * (data_size_bit + length_size_bit)

        offset = main_offset + int(locations[start : start + data_size_bit], 2)
        length = int(locations[start + data_size_bit : start + data_size_bit + length_size_bit], 2)

        print('[i] Hidden: %u bits at offset %u' % (length, offset))

        offsets.append([ offset, length ])

    return offsets


if __name__ == '__main__':
    """Point d'entrée du programme."""

    img = png.Reader('flag.png')

    data_size_bit, data = image_to_binary(img)

    offsets = read_offsets(data_size_bit, data)

    total = 0

    for o in offsets:
        total += o[1]

    print('[i] Total: %u' % total)

    hidden = ''

    for o in offsets:
        hidden += data[ o[0] : o[0] + o[1] ]

    assert(len(hidden) == total)

    utf8 = []

    for i in range(0, total, 8):

        utf8.append(int(hidden[i : i + 8], 2) & 0x7f)

    print('[!] Flag:', bytes(utf8).decode('utf8'))

    print()
