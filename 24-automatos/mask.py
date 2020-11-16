
# pip3 install --user pypng
import png


def process_ref_tile(img, keep):
    """Transpose une image en niveau de bit."""

    print('[i] Processing bit %u' % keep)

    width, height, pixels, info = img.read_flat()

    pixel_byte_width = 4 if info['alpha'] else 3

    reds = []
    greens = []
    blues = []

    for y in range(height):

        red = []
        green = []
        blue = []

        for x in range(width):

            pos = (x + y * width) * pixel_byte_width

            r, g, b = pixels[pos:pos+3]

            if r & (1 << keep):
                red.append(0)
            else:
                red.append(255)

            if g & (1 << keep):
                green.append(0)
            else:
                green.append(255)

            if b & (1 << keep):
                blue.append(0)
            else:
                blue.append(255)

        reds.append(red)
        greens.append(green)
        blues.append(blue)

    w = png.Writer(len(reds[0]), len(reds), greyscale=True, bitdepth=8)

    f = open('masked-red-%u.png' % keep, 'wb')
    w.write(f, reds)
    f.close()

    w = png.Writer(len(greens[0]), len(greens), greyscale=True, bitdepth=8)

    f = open('masked-green-%u.png' % keep, 'wb')
    w.write(f, greens)
    f.close()

    w = png.Writer(len(blues[0]), len(blues), greyscale=True, bitdepth=8)

    f = open('masked-blue-%u.png' % keep, 'wb')
    w.write(f, blues)
    f.close()


if __name__ == '__main__':
    """Point d'entrée du programme."""

    for i in range(8):

        img = png.Reader('brigitte.png')

        process_ref_tile(img, i)
