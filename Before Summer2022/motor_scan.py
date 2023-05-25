import thorlabs_apt as apt
import operator as op
import fpga_ccu.renderer as renderer
import time
import numpy as np
import tkinter as tk
import tkinter.filedialog as fd
import fpga_ccu.config as config
import matplotlib.pyplot as mpl
import matplotlib.ticker as ticker
import datetime as dt
import scipy.stats as stats
import csv

LOG_PATH = 'tmp/ccu-log.csv'

motors = apt.list_available_devices()
serial_numbers = set(map(op.itemgetter(1), motors))

print('available motors:')
for model, serial_number in motors:
    print('SN {} (model {})'.format(serial_number, model))

print()
print('select a motor (serial number):')
serial_number = None
while True:
    try:
        serial_number = int(input('> ').strip())

        if serial_number not in serial_numbers:
            print('please enter one of the available serial numbers')
            continue

        break

    except ValueError:
        print('please enter a valid serial number')

motor = apt.Motor(serial_number)

print()

print('select start angle:')
start = 0
while True:
    try:
        entry = input('(default: 0) > ').strip()

        if not entry:
            break

        start = float(entry)
        break

    except ValueError:
        print('please enter a valid number')

print()

print('select end angle:')
end = 180
while True:
    try:
        entry = input('(default: 180)> ').strip()

        if not entry:
            break

        end = float(entry)

        if end <= start:
            print('end angle must be greater than start angle')
            continue

        break
    except ValueError:
        print('please enter a valid number')

print()

print('select step size:')
step = 5
while True:
    try:
        entry = input('(default: 5) > ').strip()

        if not entry:
            break

        step = float(entry)

        if step <= 0:
            print('step angle must be positive')
            continue

        break

    except ValueError:
        print('please enter a valid number')

print('number of samples at each point (1 sec each):')
samples = 1
while True:
    try:
        entry = input('(default: 1) > ').strip()

        if not entry:
            break

        samples = int(entry)

        if samples <= 0:
            print('number of samples must be positive')
            continue

        break

    except ValueError:
        print('please enter a valid integer')

print()

print('select measurement channel (0 through 7):')
channel = 0
while True:
    try:
        channel = int(input('> ').strip())
        if channel not in range(8):
            print('channel must be between 0 through 7')
            continue
        break
    except ValueError:
        print('please enter a valid integer')


print('select output file:')
root = tk.Tk()
root.withdraw()
output_path = fd.asksaveasfilename()
if not output_path.endswith('.csv'):
    output_path = output_path + '.csv'
print('> {}'.format(output_path))

print()

print('estimated time: {:.0f} sec'.format((samples+1) * (end-start)/step))

print('beginning')


def decode(row):
    sample = int(row[0])
    time_ = float(row[1])
    total = np.array(tuple(map(float, row[2::2])))
    uncertainty = np.array(tuple(map(float, row[3::2])))
    return sample, time_, total, uncertainty


def file_reader(path):
    f.read()
    f.readline()
    while True:
        line = f.readline().strip()

        if not line:
            mpl.pause(.01)
            continue

        yield line


f = open(LOG_PATH, 'r')
reader = csv.reader(file_reader(f))
printer = renderer.Printer()
outputter = renderer.Outputter(output_path, extra=('position / deg',))

sample = np.arange(0)
time_ = np.empty(0)
total = np.empty((0, 8))
uncertainty = np.empty((0, 8))
position = np.empty(0)

printer.start()
outputter.start()

figure = mpl.figure()
axes = figure.add_subplot(1, 1, 1)
axes.set_title('Motor scan/calibration for channel {} ({}), motor {}\n'
               'averaged over {} seconds each\n'
               '{:%Y-%m-%d (%A), %I:%M %p}'
               .format(channel, config.CHANNEL_KEYS[channel], serial_number,
                       samples, dt.datetime.now()))
axes.set_xlabel('motor position (deg)')
axes.set_ylabel('incidence counts per second')

line, (cap_lower, cap_upper), (bar,) = axes.errorbar((), (), yerr=(),
                                                     capsize=1, fmt='.-')
cap_lower.set_marker('')
cap_upper.set_marker('')
axes.yaxis.set_major_locator(ticker.MaxNLocator(integer=True, min_n_ticks=1))
mpl.pause(.01)


for angle in np.arange(start, end+1e-3, step):
    print('moving to {:.2f}'.format(angle))
    motor.move_to(angle, True)
    print('moved, measuring')
    f.read()
    f.readline()
    s, ti, to, u = zip(
        *(decode(next(reader)) for _ in range(samples))
    )
    to = np.row_stack(to)
    u = stats.sem(to, axis=0)
    to = np.mean(to, axis=0)
    sample = np.append(sample, s[-1])
    time_ = np.append(time_, ti[-1])
    total = np.row_stack((total, to))
    uncertainty = np.row_stack((uncertainty, u))
    position = np.append(position, angle)
    
    
    print('position: {:.2f}'.format(angle))
    printer.render(sample, time_, total, uncertainty)
    outputter.render(sample, time_, total, uncertainty, extra=(position,))
    
    tc = total[:, channel]
    uc = uncertainty[:, channel]
    
    line.set_xdata(position)
    line.set_ydata(tc)
    cap_lower.set_xdata(position)
    cap_lower.set_ydata(tc - uc)
    cap_upper.set_xdata(position)
    cap_upper.set_ydata(tc + uc)
    bar.set_segments(tuple(zip(
        zip(position, tc-uc),
        zip(position, tc+uc)
    )))
    
    axes.relim()
    axes.autoscale_view()
    mpl.pause(.01)
    
motor.move_to(0, False)
f.close()

figure.savefig(output_path[:-3]+'pdf', format='pdf')
print('done; close plot window to exit')
while mpl.fignum_exists(figure.number):
    mpl.pause(.01)
    
print('closed; exiting')
