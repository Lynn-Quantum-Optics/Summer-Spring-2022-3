import fpga_ccu.renderer as renderer
import numpy as np
import scipy.stats as stats
import itertools as it
import time
import csv
import tkinter as tk
import tkinter.filedialog as fd

LOG_PATH = 'tmp/ccu-log.csv'


root = tk.Tk()
root.withdraw()


samples = 0
while True:
    try:
        print('# of samples (pass 0 to collect indefinitely):')
        entry = input('(default: 0) > ')
        if not entry:
            samples = 0

        samples = int(entry)

        if samples < 0:
            print('must be non-negative')
            continue

        break
    except ValueError:
        print('not a valid integer')

print()

print('select output log file:')
output_path = fd.asksaveasfilename()
print('> {}'.format(output_path))

print()


def file_reader(path):
    with open(path, 'r') as f:
        f.read()
        f.readline()
        while True:
            line = f.readline().strip()

            if not line:
                time.sleep(.1)
                continue

            yield line


def decode(row):
    sample = int(row[0])
    time_ = float(row[1])
    total = np.array(tuple(map(float, row[2::2])))
    uncertainty = np.array(tuple(map(float, row[3::2])))
    return sample, time_, total, uncertainty


outputter = renderer.Outputter(output_path)
reader = csv.reader(file_reader(LOG_PATH))
printer = renderer.Printer(output_path)

outputter.start()

first_sample = 0
sample = np.arange(0)
time_ = np.empty(0)
total = np.empty((0, 8))
uncertainty = np.empty((0, 8))

if samples > 0:
    iterations = range(samples)
else:
    iterations = it.repeat(0)

print('listening for data from "{}"'.format(LOG_PATH))
print()


def end():

    mean = np.mean(total, axis=0)
    uncertainty = stats.sem(total, axis=0)

    outputter.summary(mean, uncertainty)
    printer.summary(mean, uncertainty)


try:
    for _, (s, ti, to, u) in zip(iterations, map(decode, reader)):
        if sample.size == 0:
            first_sample = s

        sample = np.append(sample, s)
        time_ = np.append(time_, ti)
        total = np.row_stack((total, to))
        uncertainty = np.row_stack((uncertainty, u))
        printer.render(sample, time_, total, uncertainty)
        outputter.render(sample, time_, total, uncertainty)

    end()
    print('done; press interrupt (ctrl-c) to exit')
    try:
        while True:
            time.sleep(.1)
    except KeyboardInterrupt:
        print('exiting')

except KeyboardInterrupt:
    print()
    print('interrupted')
    print()
    end()
    print('press interrupt (ctrl-c) again to exit')
