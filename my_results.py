import matplotlib.pyplot as plt
import csv

rows = []
with open("tarry_1to40agents_250iterations_40x40.csv", "r") as f:
    csvreader = csv.reader(f)

    for row in csvreader:
        rows.append([float(e) for e in row])

header = rows[0]

tarry_steps_row = rows[1]
tarry_pionner_steps_row = rows[2]
tarry_fraction_row = rows[3]
tarry_stdev_row = rows[4]
tarry_steps_from_first_to_last_row = rows[5]

rows = []
with open("my_1to40agents_250iterations_40x40.csv", "r") as f:
    csvreader = csv.reader(f)

    for row in csvreader:
        rows.append([float(e) for e in row])

header = rows[0]

my_steps_row = rows[1]
my_pionner_steps_row = rows[2]
my_fraction_row = rows[3]
my_stdev_row = rows[4]
my_fraction_pionner = rows[5]

header = rows[0]

rows = []
with open("my_1to40agents_250iterations_40x40_v2.csv", "r") as f:
    csvreader = csv.reader(f)

    for row in csvreader:
        rows.append([float(e) for e in row])

my_v2_steps_row = rows[1]
my_v2_pionner_steps_row = rows[2]
my_v2_fraction_row = rows[3]
my_v2_stdev_row = rows[4]
my_v2_fraction_pionner = rows[5]

""" plt.plot(header, my_steps_row, 'b.-',label = "Average of steps")
plt.plot(header, my_pionner_steps_row, 'bd-', label = "Pionner's average of steps")
plt.plot(header, my_stdev_row, 'bx-', label = "STDEV - Average of steps")
plt.plot(header, my_fraction_row, 'b*-',label = "Fraction of maze explored")
plt.plot(header, my_fraction_pionner, 'b^-', label = "Fraction of maze explored until pionner") """

# --- plt.plot(header, my_steps_row, 'b.-',label = "Our: Average of steps")
#plt.plot(header, my_pionner_steps_row, 'bd-', label = "Our: Pionner's average of steps")
# --- plt.plot(header, my_stdev_row, 'bx-', label = "Our: STDEV - Average of steps")
# --- plt.plot(header, my_fraction_row, 'b*-', label = "Our: Fraction of maze explored")
plt.plot(header, my_fraction_pionner, 'b^-', label = "Our: Fraction of maze explored until pionner")

# --- plt.plot(header, my_v2_steps_row, 'r.-',label = "Our (2): Average of steps")
#plt.plot(header, my_v2_pionner_steps_row, 'rd-', label = "Our (2): Pionner's average of steps")
# --- plt.plot(header, my_v2_stdev_row, 'rx-', label = "Our (2): STDEV - Average of steps")
# --- plt.plot(header, my_v2_fraction_row, 'r*-', label = "Our (2): Fraction of maze explored")
plt.plot(header, my_v2_fraction_pionner, 'r^-', label = "Our (2): Fraction of maze explored until pionner")

# --- plt.plot(header, tarry_steps_row, 'g.-',label = "Tarry: Average of steps")
#plt.plot(header, tarry_pionner_steps_row, 'gd-', label = "Tarry: Pionner's average of steps")
# --- plt.plot(header, tarry_stdev_row, 'gx-', label = "Tarry: STDEV - Average of steps")
# --- plt.plot(header, tarry_fraction_row, 'g*-', label = "Tarry: Fraction of maze explored")
plt.plot(header, tarry_fraction_row, 'g^-', label = "Tarry: Fraction of maze explored until pionner")

""" #plt.plot(header, my_steps_row, 'b.-',label = "Average of steps")
#plt.plot(header, my_pionner_steps_row, 'bd-', label = "Pionner's average of steps")
#plt.plot(header, my_stdev_row, 'bx-', label = "STDEV - Average of steps")
#plt.plot(header, my_fraction_row, 'b*-', label = "Fraction of maze explored")
#plt.plot(header, my_fraction_pionner, 'b^-', label = "Fraction of maze explored until pionner")
#plt.plot(header, my_v2_steps_row, 'r.-',label = "New policy: Average of steps")
#plt.plot(header, my_v2_pionner_steps_row, 'rd-', label = "New policy: Pionner's average of steps")
#plt.plot(header, my_v2_stdev_row, 'rx-', label = "New policy: STDEV - Average of steps")
#plt.plot(header, my_v2_fraction_row, 'r*-', label = "New policy: Fraction of maze explored")
#plt.plot(header, my_v2_fraction_pionner, 'r^-', label = "New policy: Fraction of maze explored until pionner") """

""" plt.plot(header, tarry_steps_row, label = "TARRY: Average of steps")
plt.plot(header, my_steps_row, label = "TG: Average of steps")

plt.plot(header, tarry_pionner_steps_row, label = "TARRY: Pionner's average of steps")
plt.plot(header, my_pionner_steps_row, label = "TG: Pionner's average of steps") """

""" plt.plot(header, tarry_fraction_row, label = "TARRY: Fraction of maze explored")
#plt.plot(header, my_fraction_row, label = "TG: Fraction of maze explored")
plt.plot(header, my_fraction_pionner, label = "TG: Fraction of maze explored until pionner") """

""" plt.plot(header, my_steps_row, label = "TG - Average of steps")
plt.plot(header, my_pionner_steps_row, label = "TG - Pionner's average of steps")
plt.plot(header, my_v2_steps_row, label = "TG (new) - Average of steps")
plt.plot(header, my_v2_pionner_steps_row, label = "TG (new) - Pionner's average of steps") """

""" plt.plot(header, my_fraction_row, label = "TG - Fraction of maze explored")
plt.plot(header, my_fraction_pionner, label = "TG - Fraction of maze explored until pionner")
plt.plot(header, my_v2_fraction_row, label = "TG (new) - Fraction of maze explored")
plt.plot(header, my_v2_fraction_pionner, label = "TG (new) - Fraction of maze explored until pionner") """


""" plt.plot(header, tarry_steps_row, label = "TARRY: Average")
plt.plot(header, tarry_stdev_row, label = "TARRY: STDEV")
plt.plot(header, tarry_steps_from_first_to_last_row, label = "TARRY: Average Steps From First to Last")
#plt.plot(header, tarry_fraction_row, label = "TARRY (matlab): Fraction of maze explored") """


plt.xlabel('No. of agents')
#plt.ylabel('No. of steps')
plt.ylabel('Fraction of maze explored')
plt.title('Our algorithm vs. Tarry\'algorithm - 40-by-40 maze')

plt.grid()
plt.tight_layout()
plt.legend()
#plt.legend(loc='upper center', bbox_to_anchor=(1.4, 0.7))
plt.savefig('our_algorithm_vs_tarry_40x40_fraction.svg',format="svg",bbox_inches='tight')
plt.show()