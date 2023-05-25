import numpy as np
import scipy.stats as st
import matplotlib.pyplot as mpl
import sys
import pprint as pp
import thorlabs_apt as apt

sys.path.append('../')
import fpga_ccu as ccu

SERIAL_NUMBER = 83811667
CHANNEL = 0

INTERVAL = 5

START = -5
END = -2
SPACING = .2

print('available motor connections:')
pp.pprint(apt.list_available_devices())
print()

motor = apt.Motor(SERIAL_NUMBER)
print('connected to motor {}'.format(SERIAL_NUMBER))
print()

print('taking samples over:')
positions = np.arange(START, END, SPACING)
print(positions)
print()
values = np.zeros(positions.shape)
sd = np.zeros(positions.shape)
for i, position in enumerate(positions):
    print('moving to {}'.format(position))
    motor.move_to(position, True)
    print('moved, taking samples')
    with ccu.FpgaCcuController() as controller:
        c = iter(controller)
        v = c.read(round(INTERVAL/.1))[:, CHANNEL]
        
        values[i] = np.mean(v)
        sd[i] = st.sem(v)
    print('samples taken')
    print(values[i], sd[i])
    print()
    mpl.cla()
    mpl.errorbar(positions[:i+1], values[:i+1], yerr=sd[:i+1], fmt='.')
    mpl.pause(.01)
sd = sd/np.sqrt(round(INTERVAL/.1))
print('resetting motor')
motor.move_to(0)
print('reset')
print()

poly = np.polyfit(positions, values, 2)
print(poly)
a, b, c = poly
print(-b/2/a)
mpl.plot(positions, np.polyval(poly, positions), label='polyfit')
mpl.xlabel('motor position (degrees)')
mpl.ylabel('average counts per .1 second')
mpl.title('calibration for channel {}, motor {}\ny = ax^2 + bx + c\na = {}\nb={}\nc={}\nvertex at {}'.format(CHANNEL, SERIAL_NUMBER, a, b, c, -b/2/a))
mpl.show()