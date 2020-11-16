
# pip3 install --user pypng
import png


def get_tile_info(img):
    """Transpose une image en données chiffrées."""

    width, height, pixels, info = img.read_flat()

    pixel_byte_width = 4 if info['alpha'] else 3

    reds = []

    for y in range(200, 220):

        red = []

        for x in range(500, 520):

            pos = (x + y * width) * pixel_byte_width

            r, g, b = pixels[pos:pos+3]

            red.append(r)

        reds.append(red)

    return reds


def write_image(reds):
    """Constitue une image PNG à partir de valeurs."""

    extended = []

    for y in range(len(reds)):

        ext = []

        for x in range(len(reds[y])):

            for i in range(0, 20):
                ext.append(reds[y][x])

        for i in range(0, 20):
            extended.append(ext)

    w = png.Writer(len(extended[0]), len(extended), greyscale=True, bitdepth=8)

    f = open('tile.png', 'wb')
    w.write(f, extended)
    f.close()


COLOR_RED='\033[31m'
COLOR_RESET='\033[0m'


def show_raw_info(reds):
    """Affiche les données brutes de la tuile."""

    for y in range(20):

        red = []

        for x in range(20):

            r = reds[y][x]

            if r & 0x1f:
                print(COLOR_RED + '%02x' % r + COLOR_RESET, end=' ')
            else:
                print('%02x' % r, end=' ')

            red.append(r)

        reds.append(red)

        print()

    return reds


def show_masked_info(reds):
    """Affiche les données masquées de la tuile."""

    print('  ', end=' ')
    for i in range(20):
        print('%02u' % (i + 1), end=' ')
    print()

    for y in range(20):

        red = []

        print('%02u' % (y + 1), end=' ')

        for x in range(20):

            r = reds[y][x]

            if r & 0x1f:
                print(COLOR_RED + '%02u' % (r & 0x1f) + COLOR_RESET, end=' ')
            else:
                print('%02x' % r, end=' ')

            red.append(r)

        reds.append(red)

        print()

    return reds


if __name__ == '__main__':
    """Point d'entrée du programme."""

    img = png.Reader('brigitte.png')

    info = get_tile_info(img)

    write_image(info)

    show_raw_info(info)

    print()

    show_masked_info(info)
