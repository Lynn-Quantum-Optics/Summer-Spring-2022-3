from ast import Or
from turtle import right
from types import new_class
from LabWorkstation import LabWorkstation
from ConfigurationReader import ConfigReader
from Motors import Motor
from Orientation import Orientation
from Enums import Experiment

import numpy as np
import time
import datetime
import csv
import os

# Take approximately 20 minutes to run.
# The purpose of this script is to take a sweep of the Quartz plate
# but first it will find the leftmost and rightmost edges so that the sweep does not
# waste time searching over regions that are blocked.

w = LabWorkstation("configuration.json")

w.reposition_optical_component(
    orientation=Orientation(w._config.calibrated_ref["C_UVHWP"], 0),
    component_name="C_UVHWP"
)


def take_single_HH_measurement(N, samples=25):
    now = datetime.datetime.now()
    date_string = now.strftime("%m-%d-%Y_%H-%M-%S")
    this_run_name = f"{date_string}__HH__n{samples}__{N}"

    sub_dir = w.create_subdata_directory(this_run_name)

    return w._take_measurements(
        sub_dir=sub_dir,
        run_name=this_run_name,
        measurement_states=["HH"],
        num_samples=samples
    )


print("Finding left bound of QP.")

left_bound = Orientation(0, 0)
right_bound = Orientation(0, 0)

n = 0
latch = False
while True:
    new_orientation = (left_bound + right_bound) * (1 / 2)

    w.reposition_optical_component(
        orientation=new_orientation,
        component_name="C_QP"
    )

    m = take_single_HH_measurement(n, samples=5)

    if not latch and float(m["HH"]) != 0:
        right_bound = left_bound
        left_bound = right_bound - Orientation(0, np.pi / 8)
    elif not latch:
        left_bound = new_orientation
        right_bound = left_bound + Orientation(0, np.pi)
        latch = True
        print("Latched")
    elif float(m["HH"]) != 0:
        right_bound = new_orientation
    else:
        left_bound = new_orientation

    e = (left_bound.phi - right_bound.phi)
    print(e)
    if latch and abs(e) < 0.1:
        break

    n += 1

LEFT_BOUND = left_bound

print("Left bound located.")

right_bound = left_bound + Orientation(0, np.pi - np.pi / 8)

while True:
    new_orientation = (left_bound + right_bound) * (1 / 2)

    w.reposition_optical_component(
        orientation=new_orientation,
        component_name="C_QP"
    )

    m = take_single_HH_measurement(n, samples=5)

    if float(m["HH"]) != 0:
        left_bound = new_orientation
    else:
        right_bound = new_orientation

    e = (left_bound.phi - right_bound.phi)
    print(e)
    if abs(e) < 0.1:
        break

    n += 1

RIGHT_BOUND = right_bound

print("Right bound located.")

w.configure_measurement_basis_preset("DD")

w.take_calibration_measurements_1d(
    initial_orientation=LEFT_BOUND,
    final_orientation=RIGHT_BOUND,
    num_steps=50,
    num_samples=10,
    component_name="C_QP"
)

print("Open the sweep file and identify the peak closest to the center of the plot.")
print("Estimate this value and use it as the calibrated position for C_QP.")
print("The QP will be further calibrated later so do not worry if it is slightly off.")
