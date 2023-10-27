import matplotlib.pyplot as plt
import csv

""" rows = []
with open("tarry_1to80agents_250iterations_20x20.csv", "r") as f:
    csvreader = csv.reader(f)

    for row in csvreader:
        rows.append([float(e) for e in row])

header = rows[0]

tarry_steps_row = rows[1]
tarry_pionner_steps_row = rows[2]
tarry_fraction_row = rows[3]
tarry_stdev_row = rows[4]
tarry_steps_from_first_to_last_row = rows[5] """

fig, ax = plt.subplots(4, 1)

rows = []
with open("my_1to40agents_250iterations_10x10.csv", "r") as f:
    csvreader = csv.reader(f)

    for row in csvreader:
        rows.append([float(e) for e in row])

header = rows[0]

my10_steps_row = rows[1]
my10_pionner_steps_row = rows[2]
my10_fraction_row = rows[3]
my10_stdev_row = rows[4]
my10_fraction_pionner = rows[5]

rows = []
with open("my_1to40agents_250iterations_20x20.csv", "r") as f:
    csvreader = csv.reader(f)

    for row in csvreader:
        rows.append([float(e) for e in row])

header = rows[0]

my20_steps_row = rows[1]
my20_pionner_steps_row = rows[2]
my20_fraction_row = rows[3]
my20_stdev_row = rows[4]
my20_fraction_pionner = rows[5]


rows = []
with open("my_1to40agents_250iterations_30x30.csv", "r") as f:
    csvreader = csv.reader(f)

    for row in csvreader:
        rows.append([float(e) for e in row])

header = rows[0]

my30_steps_row = rows[1]
my30_pionner_steps_row = rows[2]
my30_fraction_row = rows[3]
my30_stdev_row = rows[4]
my30_fraction_pionner = rows[5]


rows = []
with open("my_1to40agents_250iterations_40x40.csv", "r") as f:
    csvreader = csv.reader(f)

    for row in csvreader:
        rows.append([float(e) for e in row])

header = rows[0]

my40_steps_row = rows[1]
my40_pionner_steps_row = rows[2]
my40_fraction_row = rows[3]
my40_stdev_row = rows[4]
my40_fraction_pionner = rows[5]

""" rows = []
with open("my_1to40agents_250iterations_10x10_v2.csv", "r") as f:
    csvreader = csv.reader(f)

    for row in csvreader:
        rows.append([float(e) for e in row])

my_v2_steps_row = rows[1]
my_v2_pionner_steps_row = rows[2]
my_v2_fraction_row = rows[3]
my_v2_stdev_row = rows[4]
my_v2_fraction_pionner = rows[5] """

ax[0].plot(header, my10_steps_row, 'b.-',label = "Average of steps")
ax[0].plot(header, my10_pionner_steps_row, 'bd-', label = "Pionner's average of steps")
ax[0].plot(header, my10_stdev_row, 'bx-', label = "STDEV - Average of steps")
ax[0].set_xlabel('No. of agents')
ax[0].set_ylabel('No. of steps')
ax[0].set_title('Our algorithm - Old vs. New - 10-by-10 maze')
ax[0].grid()

ax[1].plot(header, my20_steps_row, 'b.-')
ax[1].plot(header, my20_pionner_steps_row, 'bd-')
ax[1].plot(header, my20_stdev_row, 'bx-')
ax[1].set_xlabel('No. of agents')
ax[1].set_ylabel('No. of steps')
ax[1].set_title('Our algorithm - Old vs. New - 10-by-10 maze')
ax[1].grid()

ax[2].plot(header, my30_steps_row, 'b.-')
ax[2].plot(header, my30_pionner_steps_row, 'bd-')
ax[2].plot(header, my30_stdev_row, 'bx-')
ax[2].set_xlabel('No. of agents')
ax[2].set_ylabel('No. of steps')
ax[2].set_title('Our algorithm - Old vs. New - 10-by-10 maze')
ax[2].grid()

ax[3].plot(header, my40_steps_row, 'b.-')
ax[3].plot(header, my40_pionner_steps_row, 'bd-')
ax[3].plot(header, my40_stdev_row, 'bx-')
ax[3].set_xlabel('No. of agents')
ax[3].set_ylabel('No. of steps')
ax[3].set_title('Our algorithm - Old vs. New - 10-by-10 maze')
ax[3].grid()

""" plt.plot(header, my_steps_row, 'b.-',label = "Average of steps")
plt.plot(header, my_pionner_steps_row, 'bd-', label = "Pionner's average of steps")
plt.plot(header, my_stdev_row, 'bx-', label = "STDEV - Average of steps")
plt.plot(header, my_v2_steps_row, 'r.-',label = "New policy: Average of steps")
plt.plot(header, my_v2_pionner_steps_row, 'rd-', label = "New policy: Pionner's average of steps")
plt.plot(header, my_v2_stdev_row, 'rx-', label = "New policy: STDEV - Average of steps") """

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


""" plt.xlabel('No. of agents')
plt.ylabel('No. of steps')
#plt.ylabel('Fraction of maze explored')
plt.title('Our algorithm - Old vs. New - 10-by-10 maze')
plt.grid() """

fig.tight_layout()
#fig.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1))
fig.legend(bbox_to_anchor=(1.3, 0.5))
fig.savefig('our_algorithm_10x10_old_vs_new.svg',format="svg",bbox_inches='tight')
plt.show()