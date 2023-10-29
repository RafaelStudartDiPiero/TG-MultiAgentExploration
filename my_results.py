import matplotlib.pyplot as plt
import csv

rows = []
with open("tarry_1to40agents_250iterations_40x40.csv", "r") as f:
    csvreader = csv.reader(f)

    for row in csvreader:
        rows.append([float(e) for e in row])

header = rows[0]

tarry_steps_row = rows[1]
tarry_pioneer_steps_row = rows[2]
tarry_fraction_row = rows[3]
tarry_fraction_row = [i*100 for i in tarry_fraction_row]
tarry_stdev_row = rows[4]
tarry_steps_from_first_to_last_row = rows[5]


rows = []
with open("my_1to40agents_250iterations_40x40.csv", "r") as f:
    csvreader = csv.reader(f)

    for row in csvreader:
        rows.append([float(e) for e in row])

header = rows[0]

my_steps_row = rows[1]
my_pioneer_steps_row = rows[2]
my_fraction_row = rows[3]
my_fraction_row = [i*100 for i in my_fraction_row]
my_stdev_row = rows[4]
my_fraction_pioneer = rows[5]
my_fraction_pioneer = [i*100 for i in my_fraction_pioneer]


rows = []
with open("my_1to40agents_250iterations_40x40_v2.csv", "r") as f:
    csvreader = csv.reader(f)

    for row in csvreader:
        rows.append([float(e) for e in row])

my_v2_steps_row = rows[1]
my_v2_pioneer_steps_row = rows[2]
my_v2_fraction_row = rows[3]
my_v2_fraction_row = [i*100 for i in my_v2_fraction_row]
my_v2_stdev_row = rows[4]
my_v2_fraction_pioneer = rows[5]
my_v2_fraction_pioneer = [i*100 for i in my_v2_fraction_pioneer]



#plt.plot(header, my_steps_row, 'b.-',label = "Average of steps")
#plt.plot(header, my_pioneer_steps_row, 'gd-', label = "Pioneer's average of steps")
#plt.plot(header, my_stdev_row, 'rx-', label = "STDEV - Average of steps")
#plt.plot(header, my_fraction_row, 'b*-',label = "Fraction of maze explored")
#plt.plot(header, my_fraction_pioneer, 'g^-', label = "Fraction of maze explored when pioneer reaches target")

# --- plt.plot(header, my_steps_row, 'b.-',label = "Our (1I): Average of steps")
#plt.plot(header, my_pioneer_steps_row, 'bd-', label = "Our (1I): Pioneer's average of steps")
# --- plt.plot(header, my_stdev_row, 'bx-', label = "Our (1I): STDEV - Average of steps")
# --- plt.plot(header, my_fraction_row, 'b*-', label = "Our (1I): Fraction of maze explored")
plt.plot(header, my_fraction_pioneer, 'b^-', label = "Our (1I): Fraction of maze explored when pioneer reaches target")

# --- plt.plot(header, my_v2_steps_row, 'r.-',label = "Our (2I): Average of steps")
#plt.plot(header, my_v2_pioneer_steps_row, 'rd-', label = "Our (2I): Pioneer's average of steps")
# --- plt.plot(header, my_v2_stdev_row, 'rx-', label = "Our (2I): STDEV - Average of steps")
# --- plt.plot(header, my_v2_fraction_row, 'r*-', label = "Our (2I): Fraction of maze explored")
plt.plot(header, my_v2_fraction_pioneer, 'r^-', label = "Our (2I): Fraction of maze explored when pioneer reaches target")

# --- plt.plot(header, tarry_steps_row, 'g.-',label = "Tarry: Average of steps")
#plt.plot(header, tarry_pioneer_steps_row, 'gd-', label = "Tarry: Pioneer's average of steps")
# --- plt.plot(header, tarry_stdev_row, 'gx-', label = "Tarry: STDEV - Average of steps")
# --- plt.plot(header, tarry_fraction_row, 'g*-', label = "Tarry: Fraction of maze explored")
plt.plot(header, tarry_fraction_row, 'g^-', label = "Tarry: Fraction of maze explored when pioneer reaches target")

#plt.plot(header, my_steps_row, 'b.-',label = "1I: Average of steps")
#plt.plot(header, my_pioneer_steps_row, 'bd-', label = "1I: Pioneer's average of steps")
#plt.plot(header, my_stdev_row, 'bx-', label = "1I: STDEV - Average of steps")
#plt.plot(header, my_fraction_row, 'b*-', label = "1I: Fraction of maze explored")
#plt.plot(header, my_fraction_pioneer, 'b^-', label = "1I: Fraction of maze explored when pioneer reaches target")
#plt.plot(header, my_v2_steps_row, 'r.-',label = "2I: Average of steps")
#plt.plot(header, my_v2_pioneer_steps_row, 'rd-', label = "2I: Pioneer's average of steps")
#plt.plot(header, my_v2_stdev_row, 'rx-', label = "2I: STDEV - Average of steps")
#plt.plot(header, my_v2_fraction_row, 'r*-', label = "2I: Fraction of maze explored")
#plt.plot(header, my_v2_fraction_pioneer, 'r^-', label = "2I: Fraction of maze explored when pioneer reaches target")

""" plt.plot(header, tarry_steps_row, label = "TARRY: Average of steps")
plt.plot(header, my_steps_row, label = "TG: Average of steps")

plt.plot(header, tarry_pioneer_steps_row, label = "TARRY: Pioneer's average of steps")
plt.plot(header, my_pioneer_steps_row, label = "TG: Pioneer's average of steps") """

""" plt.plot(header, tarry_fraction_row, label = "TARRY: Fraction of maze explored")
#plt.plot(header, my_fraction_row, label = "TG: Fraction of maze explored")
plt.plot(header, my_fraction_pioneer, label = "TG: Fraction of maze explored when pioneer reaches target") """

""" plt.plot(header, my_steps_row, label = "TG - Average of steps")
plt.plot(header, my_pioneer_steps_row, label = "TG - Pioneer's average of steps")
plt.plot(header, my_v2_steps_row, label = "TG (new) - Average of steps")
plt.plot(header, my_v2_pioneer_steps_row, label = "TG (new) - Pioneer's average of steps") """

""" plt.plot(header, my_fraction_row, label = "TG - Fraction of maze explored")
plt.plot(header, my_fraction_pioneer, label = "TG - Fraction of maze explored when pioneer reaches target")
plt.plot(header, my_v2_fraction_row, label = "TG (new) - Fraction of maze explored")
plt.plot(header, my_v2_fraction_pioneer, label = "TG (new) - Fraction of maze explored when pioneer reaches target") """


""" plt.plot(header, tarry_steps_row, label = "TARRY: Average")
plt.plot(header, tarry_stdev_row, label = "TARRY: STDEV")
plt.plot(header, tarry_steps_from_first_to_last_row, label = "TARRY: Average Steps From First to Last")
#plt.plot(header, tarry_fraction_row, label = "TARRY (matlab): Fraction of maze explored") """


plt.xlabel('No. of agents')
plt.ylabel('No. of steps')
plt.ylabel('Fraction of maze explored (%)')
#plt.title('Our algorithm - 40-by-40 maze')
plt.title('Our algorithm vs. Tarry\'s algorithm - 40-by-40 maze')
#plt.title('Our algorithm - 1 interval vs. 2 intervals - 10-by-10 maze')

plt.grid()
plt.tight_layout()
plt.legend()
#plt.legend(loc='upper center', bbox_to_anchor=(1.4, 0.7))
plt.savefig('our_algorithm_vs_tarry_40x40_fraction.svg',format="svg",bbox_inches='tight')
plt.show()

""" # 1 interval vs 2 intervals - fraction
import pylab
fig = pylab.figure()
figlegend = pylab.figure(figsize=(6,2))
ax = fig.add_subplot(111)
lines = ax.plot(range(10), pylab.randn(10), 'b*-',
                range(10), pylab.randn(10), 'b^-',
                range(10), pylab.randn(10), 'r*-',
                range(10), pylab.randn(10), 'r^-')
text = (
    "1I: Fraction of maze explored",
    "1I: Fraction of maze explored when pioneer reaches target",
    "2I: Fraction of maze explored",
    "2I: Fraction of maze explored when pioneer reaches target"
)
figlegend.legend(lines, text, 'center')
fig.show()
figlegend.show()
figlegend.savefig('legend.svg') """

""" # 1 interval vs 2 intervals - steps
import pylab
fig = pylab.figure()
figlegend = pylab.figure(figsize=(3,2))
ax = fig.add_subplot(111)
lines = ax.plot(range(10), pylab.randn(10), 'b.-',
                range(10), pylab.randn(10), 'bd-',
                range(10), pylab.randn(10), 'bx-',
                range(10), pylab.randn(10), 'r.-',
                range(10), pylab.randn(10), 'rd-',
                range(10), pylab.randn(10), 'rx-',)
text = (
    "1I: Average of steps",
    "1I: Pioneer's average of steps",
    "1I: STDEV - Average of steps",
    "2I: Average of steps",
    "2I: Pioneer's average of steps",
    "2I: STDEV - Average of steps"
)
figlegend.legend(lines, text, 'center')
fig.show()
figlegend.show()
figlegend.savefig('legend.svg') """