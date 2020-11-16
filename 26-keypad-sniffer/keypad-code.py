
def check_connected(lines):
    """Vérifie que les liens 5-11 et 6-12 sont bien connectés."""

    for s in range(len(lines[0])):

        values = []

        for l in lines:
            if not(l[s] in values):
                values.append(l[s])

        print('[*] States for #%u:' % s, ', '.join(sorted(values)))

    for l in olines:
        assert(l[4] == l[10])
        assert(l[5] == l[11])

    print('[i] All ground links are consistent.')

    print('[i] Link 5-11: always %c' % lines[0][4])
    print('[i] Link 6-12: always %c' % lines[0][5])


def filter_same_sample(lines):
    """Filtre les échantillons consécutifs identiques."""

    samples = []

    first = True

    for l in lines:

        if first:
            samples.append(l)
            first = False

        elif l != samples[-1]:
            samples.append(l)

    print('[i] Filtered %u samples' % (len(lines) - len(samples)))

    return samples


def reorder_samples_states(lines):
    """Réaffecte les états des échantillons à leur ordre nominal."""

    samples = []

    for l in lines:

        c1 = l[3]
        c2 = l[2]
        c3 = l[1]
        c4 = l[0]

        l1 = l[9]
        l2 = l[8]
        l3 = l[7]
        l4 = l[6]

        samples.append(c1 + c2 + c3 + c4 + '  ' + l1 + l2 + l3 + l4 + '  ')

    return samples


def fix_samples(lines):
    """Retire les échantillons sans appui de touche répété."""

    samples = []

    patterns = [ '0111', '1011', '1101', '1110' ]

    i = 0

    while (i + 1) < len(lines):

        loop = []

        for k in range(4):

            check = lines[i]

            if check.startswith(patterns[k]):
                i += 1
                loop.append(check)

            else:
                print('[!] Missed samples for column %u @ %u: "%s"' % (k, i, check))
                loop.append(patterns[k] + '  1111  ')

        samples += loop

    if len(samples) > len(lines):
        print('[i] Added %u new samples' % (len(samples) - len(lines)))

    return samples


def filter_no_key_pressed(lines):
    """Retire les échantillons sans appui de touche répété."""

    samples = []

    last = None

    for i in range(0, len(lines), 4):

        c1 = lines[i + 0]
        c2 = lines[i + 1]
        c3 = lines[i + 2]
        c4 = lines[i + 3]

        cur = [ c1, c2, c3, c4 ]

        if last != cur:

            samples += cur
            last = cur

    print('[i] Skipped %u samples ith or without key pressed' % (len(lines) - len(samples)))

    return samples


def get_pressed_keys(lines):
    """Obtient la liste des touches pressées."""

    # Colonnes x lignes
    matrix = [
        [ '1', '4', '7', 'A' ],
        [ '2', '5', '8', '0' ],
        [ '3', '6', '9', 'B' ],
        [ 'F', 'E', 'D', 'C' ]
    ]

    code = ''

    for l in lines:

        x = l[0:4]
        y = l[6:10]

        if y == '1111':
            continue

        assert(x.count('0') == 1)
        assert(y.count('0') == 1)

        x = x.find('0')
        y = y.find('0')

        code += matrix[x][y]

    return code


if __name__ == '__main__':

    with open('keypad_sniffer.txt', 'r') as fd:
        data = fd.read()

    lines = data.split('\n')

    olines = []

    for l in lines:
        if len(l):
            olines.append(''.join([ c for c in reversed(l) ]))

    check_connected(olines)

    olines = filter_same_sample(olines)

    olines = reorder_samples_states(olines)

    olines = fix_samples(olines)
    
    #with open('data.txt', 'w') as fd:
    #    fd.write('\n'.join(olines))

    olines = filter_no_key_pressed(olines)

    code = get_pressed_keys(olines)

    print('[i] Retrieved code: %s' % code)

    print('[>] Flag is DGSESIEE{%s}' % code)
