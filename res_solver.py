#
# Resistance solver
#
from pyrecord import Record
Combination = Record.create_type("Combination", "r_a", "r_b", "precision")

e48 = [100, 105, 110, 115, 121, 127, 133, 140, 147, 154, 162, 169, 178, 187, 196, 205, 215, 226, 237, 249, 261, 274, 287, 301, 316, 332, 348, 365, 383, 402, 422, 442, 464, 487, 511, 536, 562, 590, 619, 649, 681, 715, 750, 787, 825, 866, 909, 953]
e24 = [100, 110, 120, 130, 150, 160, 180, 200, 220, 240, 270, 300, 330, 360, 390, 430, 470, 510, 560, 620, 680, 750, 820, 910]
e12 = [100, 120, 150, 180, 220, 270, 330, 390, 470, 560, 680, 820]

series = e12
precision_percent = 20
target = 195.43


def r_in_parallel(Ra, Rb):
    epsilon = 0.000001
    if abs(Ra) < epsilon or abs(Rb) < epsilon:
        return 0.0
    else:
        return 1.0/(1.0/Ra + 1.0/Rb)

def delta(target, value):
    return (target - value)/target

def is_match(target, value, precision):
    return abs(delta(target, value)) < precision/100.0

records_list = list()
for Ra in series:
    for Rb in series:
        calculated = r_in_parallel(Ra, Rb)
        if is_match(target, calculated, precision_percent) and Ra <= Rb:
            candidate = Combination(Ra, Rb, abs(delta(target, calculated)))
            records_list.append(candidate)
            
print("Using ", "E12" if series == e12 else "E24" if (series == e24) else "E96", " series of resistance values in parallel to make {:.2f}Ω".format(target), " within ", precision_percent, "% precision,")
for candidate in sorted(records_list,key=lambda c: c.precision, reverse=False):
    calculated = r_in_parallel(candidate.r_a, candidate.r_b)
    print("\tcombine {:.0f}Ω".format(candidate.r_a), " with {:.0f}Ω".format(candidate.r_b), " giving ", '{:.2f}Ω, '.format(calculated), "within {:.1f}%".format(100.0 * candidate.precision), " precision")
            

