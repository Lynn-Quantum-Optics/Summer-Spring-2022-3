import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as mpl
import pprint as pp

amplitude, period, initial, offset = 1/2, 85, 5, 1/3
params = np.array((amplitude, period, initial, offset))
spacing = 5

variation = 1/50


def f(x, amplitude, period, initial, offset):
    return amplitude * np.sin(2*np.pi * (x-initial)/period) + offset


x = np.arange(0, 90, spacing)
y = f(x, *params) + np.random.normal(0, variation, x.shape)

guess_offset = np.mean(y)
guess_amplitude = np.std(y, ddof=1) * np.sqrt(2)
guess_period = 90
guess_initial = 0
guess_params = guess_amplitude, guess_period, guess_initial, guess_offset

opt_params, _ = opt.curve_fit(f, x, y, p0=guess_params)

smooth_x = np.arange(0, 90, .5)
opt_y = f(smooth_x, *opt_params)


pp.pprint(params)
pp.pprint(opt_params)

mpl.scatter(x, y)
mpl.plot(smooth_x, opt_y)
mpl.show()
