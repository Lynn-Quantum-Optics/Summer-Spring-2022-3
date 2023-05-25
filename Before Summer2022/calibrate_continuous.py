import thorlabs_apt as apt
import matplotlib.pyplot as mpl
import scipy.optimize as optimize
import numpy as np
import sys
sys.path.append('../fpga')
import fpga_ccu

SERIAL_NUMBER = 83811904
CHANNEL = 4

START = 0
END = 90
SPEED = 1

print('motor devices')
print(apt.list_available_devices())

print('connecting to fpga')
with fpga_ccu.FpgaCcuController(interval=.1) as ccu:
    print('connected to fpga')
    print('connecting to motor {}'.format(SERIAL_NUMBER))
    motor = apt.Motor(SERIAL_NUMBER)
    print('connected to motor')
    motor.maximum_velocity = SPEED

    points = []

    print('starting motion')
    motor.move_to(0, True)
    motor.move_to(END, False)

    while not motor.is_in_motion:
        pass

    for entry in ccu:
        point = motor.position, entry[CHANNEL]
        print(point)
        points.append(point)
        if not motor.is_in_motion and abs(motor.position - END) < 1:
            break

    positions, values = zip(*points)

motor.move_to(0, False)

def curve(position, amplitude, period, initial, offset):
    return -amplitude * np.cos(2*np.pi * (position-initial)/period) + offset


def fit(positions, values):
    guess_amplitude = np.std(values, ddof=1) * np.sqrt(2)
    guess_period = 90
    guess_initial = 0
    guess_offset = np.mean(values)
    guess_params = np.array((guess_amplitude, guess_period,
                             guess_initial, guess_offset))
    fit_params, covariance = optimize.curve_fit(curve, positions, values,
                                                p0=guess_params)
    return guess_params, fit_params, covariance


guess_params, fit_params, covariance = fit(positions, values)
print(np)
uncertainty = np.sqrt(tuple(row[i] for i, row in enumerate(covariance)))

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

mpl.scatter(positions, values)
#mpl.plot(positions, curve(positions, *guess_params), label='guess')
mpl.plot(positions, curve(positions, *fit_params), label='fit')
mpl.legend()
mpl.show()
