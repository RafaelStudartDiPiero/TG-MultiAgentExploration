import matplotlib.pyplot as plt
import csv

rows = []
with open("tarry_1to30agents_250iterations_20x20.csv", "r") as f:
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
with open("my_1to30agents_250iterations_20x20.csv", "r") as f:
    csvreader = csv.reader(f)

    for row in csvreader:
        rows.append([float(e) for e in row])

my_steps_row = rows[1]
my_pionner_steps_row = rows[2]
my_fraction_row = rows[3]
my_stdev_row = rows[4]
my_fraction_pionner = rows[5]

""" plt.plot(header, tarry_steps_row, label = "TARRY: Average of steps")
plt.plot(header, my_steps_row, label = "TG: Average of steps")

plt.plot(header, tarry_pionner_steps_row, label = "TARRY: Pionner's average of steps")
plt.plot(header, my_pionner_steps_row, label = "TG: Pionner's average of steps") """

""" plt.plot(header, tarry_fraction_row, label = "TARRY: Fraction of maze explored")
plt.plot(header, my_fraction_row, label = "TG: Fraction of maze explored")
plt.plot(header, my_fraction_pionner, label = "TG: Fraction of maze explored until pionner") """

plt.plot(header, tarry_steps_row, label = "Average")
plt.plot(header, tarry_stdev_row, label = "STDEV")
plt.plot(header, tarry_steps_from_first_to_last_row, label = "Average Steps From Fist to Last")


""" plt.plot(header, tarry_fraction_row, label = "TARRY: Fraction of maze explored")
plt.plot(header, tarry_matlab_fraction_row, label = "TARRY (matlab): Fraction of maze explored") """


plt.xlabel('No. of agents')
plt.ylabel('No. of steps')
#plt.ylabel('Fraction of maze explored')
plt.title('Tarry - 20-by-20 maze')

plt.grid()
plt.legend()
plt.show()