import thorlabs_apt as apt
import pprint as pp
import sys
import numpy as np
import scipy.stats as st
import scipy.optimize as optimize
import matplotlib.pyplot as mpl

sys.path.append('../')
import fpga_ccu as ccu

SERIAL_NUMBER = 83811901
CHANNEL = 1

INTERVAL = 60

START = 350
END = 359
SPACING = 1

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
        v = np.array([next(c)[CHANNEL] for _ in range(round(INTERVAL/.1))])
        
        values[i] = np.mean(v)
        sd[i] = st.sem(v)
    print('samples taken')
    print(values[i], sd[i])
    print()
    mpl.cla()
    mpl.scatter(positions, values)
    mpl.errorbar(positions, values, yerr=sd, fmt='none')
    mpl.pause(.01)
sd = sd/np.sqrt(round(INTERVAL/.1))
print('resetting motor')
motor.move_to(0)
print('reset')
print()

#def curve(position, amplitude, period, initial, offset):
#    return -amplitude * np.cos(2*np.pi * (position-initial)/period) + offset
#
#
#def fit(positions, values):
#    guess_amplitude = np.std(values, ddof=1) * np.sqrt(2)
#    guess_period = 90
#    guess_initial = 0
#    guess_offset = np.mean(values)
#    guess_params = np.array((guess_amplitude, guess_period,
#                             guess_initial, guess_offset))
#    fit_params, covariance = optimize.curve_fit(curve, positions, values,
#                                                p0=guess_params)
#    return guess_params, fit_params, covariance


#guess_params, fit_params, covariance = fit(positions, values)
#print(np)
#uncertainty = np.sqrt(tuple(row[i] for i, row in enumerate(covariance)))

print('parameters')
print('(amplitude, period, initial, offset)')
print()

print('guess')
print(guess_params)
print()

print('fit')
print(fit_params)
print()

print('uncertainty')
print(uncertainty)
print()

mpl.cla()
mpl.scatter(positions, values)
mpl.errorbar(positions, values, yerr=sd, fmt='none')
mpl.plot(positions, curve(positions, *guess_params), label='guess')
mpl.plot(positions, curve(positions, *fit_params), label='fit')
mpl.legend()
mpl.show()
