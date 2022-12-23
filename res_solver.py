#
# Resistance solver
#
from pyrecord import Record
Combination = Record.create_type("Combination", "r_a", "r_b", "r_c", "calculated", "precision")

e48 = [100, 105, 110, 115, 121, 127, 133, 140, 147, 154, 162, 169, 178, 187, 196, 205, 215, 226, 237, 249, 261, 274, 287, 301, 316, 332, 348, 365, 383, 402, 422, 442, 464, 487, 511, 536, 562, 590, 619, 649, 681, 715, 750, 787, 825, 866, 909, 953]
e24 = [100, 110, 120, 130, 150, 160, 180, 200, 220, 240, 270, 300, 330, 360, 390, 430, 470, 510, 560, 620, 680, 750, 820, 910]
e12 = [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82, 100, 120, 150, 180, 220, 270, 330, 390, 470, 560, 680, 820]

series = e12
precision_percent = 1
target = 17.62


def r_in_parallel(r_a, r_b, r_c=99999999999.0):
    epsilon = 0.000001
    if abs(r_a) < epsilon or abs(r_b) < epsilon or abs(r_c) < epsilon:
        return 0.0
    else:
        return 1.0/(1.0/r_a + 1.0/r_b + 1.0/r_c)

def delta(expected, actual):
    return (expected - actual)/expected

def is_match(expected, actual, precision):
    return abs(delta(expected, actual)) < precision/100.0

records_list = list()
for Ra in series:
    for Rb in series:
        for Rc in series:
            calculated = r_in_parallel(Ra, Rb, Rc)
            if is_match(target, calculated, precision_percent) and Ra <= Rb and Rb <= Rc:
                candidate = Combination(Ra, Rb, Rc, calculated, abs(delta(target, calculated)))
                records_list.append(candidate)
            
print("Using three of ", "E12" if series == e12 else "E24" if (series == e24) else "E48", " series of resistance values in parallel to make {:.2f}Ω".format(target), " within ", precision_percent, "% precision,")
for candidate in sorted(records_list,key=lambda c: c.precision, reverse=False):
    print("\tcombine {:.0f}Ω".format(candidate.r_a), " with {:.0f}Ω".format(candidate.r_b), " and with {:.0f}Ω".format(candidate.r_c), " giving ", '{:.2f}Ω, '.format(candidate.calculated), "with {:.1f}%".format(100.0 * candidate.precision), " precision")
