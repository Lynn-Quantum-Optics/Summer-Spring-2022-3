import fpga_ccu.renderer as renderer
import matplotlib.pyplot as mpl
import csv
import numpy as np
import time
import datetime as dt

PATH = 'temp/ccu/ccu-log.csv'

plotter = renderer.Plotter(
    [0, 1], [4], bar=True,
    title='CCU measurements monitor:\ncounts per 1.0 sec\n'
    '{:%Y-%m-%d (%A), %I:%M %p}'.format(dt.datetime.now()),
    plot_window=100
)
printer = renderer.Printer()

plotter.start()


def file_reader(path):
    with open(path, 'r') as f:
        f.read()
        f.readline()
        while True:
            line = f.readline().strip()

            if not line:
                mpl.pause(.01)
                continue

            yield line


def decode(row):
    sample = int(row[0])
    time_ = float(row[1])
    total = np.array(tuple(map(float, row[2::2])))
    uncertainty = np.array(tuple(map(float, row[3::2])))
    return sample, time_, total, uncertainty


reader = csv.reader(file_reader(PATH))

first_sample = 0
sample = np.arange(0)
time_ = np.empty(0)
total = np.empty((0, 8))
uncertainty = np.empty((0, 8))

print('listening for data from "{}"'.format(PATH))
print()

for s, ti, to, u in map(decode, reader):
    if sample.size == 0:
        first_sample = s

    if not mpl.fignum_exists(plotter.figure.number):
        print('closed; hit interrupt (ctrl-c) to exit')
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            break

    sample = np.append(sample, s)
    time_ = np.append(time_, ti)
    total = np.row_stack((total, to))
    uncertainty = np.row_stack((uncertainty, u))
    plotter.render(sample, time_, total, uncertainty)
    printer.render(sample, time_, total, uncertainty)
