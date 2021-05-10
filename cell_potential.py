import csv
import sys

# parameters
potentials_file = 'potentials_reformatted.csv'
cells_file = 'cells.csv'
if len(sys.argv) > 1: cells_file = sys.argv[1]
voltage_decimals = 2

# read cell potentials from file
with open(potentials_file, 'r') as f:
    raw_data = list(csv.reader(f))
    potentials = [[i[0], int(i[1]), i[2], float(i[3])] for i in raw_data[1:]]


# determine if two strings are the same species
# match species with/without states given
# with/without whitespace before state
def eq_species(a, b):
    al = [i.split('(')[0] for i in a.split(' + ')]
    bl = [i.split('(')[0] for i in b.split(' + ')]
    return len(al) == len(bl) and all([i == j for i, j in zip(al, bl)])

# takes two half-reaction rows from potentials
# chooses anode and cathode and calcuates cell potential
def cell_potential(h1, h2):
    cathode, anode = sorted([h1, h2], key=lambda x: x[-1])
    return anode, cathode, anode[-1] - cathode[-1]

# cells.csv has rows of format electrode1,electrode2
with open(cells_file, 'r') as f:
    cells = list(csv.reader(f))



for s1, s2 in cells:
    s1_candidates = list(filter(lambda p: eq_species(p[2], s1) ,potentials))
    s2_candidates = list(filter(lambda p: eq_species(p[2], s2) ,potentials))
    lengths = [len(i[0]) + len(i[2]) for i in s1_candidates + s2_candidates]
    rxn_padding = max(lengths) + 14

    def print_row(a, c, v, av, cv):
        print(a.ljust(rxn_padding), c.ljust(rxn_padding), v.ljust(14), av.ljust(14), cv.ljust(14), sep='')

    print(f'Cell with {s1}, {s2}')
    print_row('anode', 'cathode', 'cell pot.', 'anode pot.', 'cathode pot.')
    for a in s1_candidates:
        for b in s2_candidates:
            an, ct, v = cell_potential(a, b)
            ah = an[0] + ' + ' + str(an[1]) + 'e-' + ' -> ' + an[2]
            ch = ct[2] + ' -> '+ ct[0] + ' + ' + str(ct[1]) + 'e-'
            print_row(ah, ch, str(round(v, voltage_decimals)), str(an[3]), str(ct[3]))
    print()
