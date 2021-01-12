import colorlover


def hsl_diffs():

    hsl_bins = [
        [3, 69, 50],
        [14, 89, 61],
        [30, 98, 69],
        [44, 98, 77],
        [60, 100, 87],
        [73, 76, 74],
        [88, 59, 63],
        [118, 41, 56],
        [146, 71, 35],
    ]

    diffs = []

    for bindex in range(len(hsl_bins) - 1):

        h_compdiff = hsl_bins[bindex + 1][0] - hsl_bins[bindex][0]
        s_compdiff = hsl_bins[bindex + 1][1] - hsl_bins[bindex][1]
        l_compdiff = hsl_bins[bindex + 1][2] - hsl_bins[bindex][2]

        comp_diffs = [h_compdiff, s_compdiff, l_compdiff]
        diffs.append(comp_diffs)

    return diffs


if __name__ == '__main__':
    hdb = hsl_diffs()
    print(hdb)
