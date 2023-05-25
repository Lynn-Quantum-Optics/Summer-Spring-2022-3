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

# This script is broken but its purpose in principle is to quickly maximize HH on the UV HWP.
# It is too sensitive to noise and additionally when calibrating it is much better to minimize a value than to
# maximize a value.

w = LabWorkstation("configuration.json")

STEP_SIZE = 0.005


def take_single_HH_slope_measurement_3(orientation, step, N, samples=50):
    now = datetime.datetime.now()
    date_string = now.strftime("%m-%d-%Y_%H-%M-%S")
    this_run_name = f"{date_string}__HH_slope__n{samples}__{N}"

    sub_dir = w.create_subdata_directory(this_run_name)

    w.reposition_optical_component(
        orientation=orientation,
        component_name="C_UVHWP"
    )

    r1 = w._take_measurements(
        sub_dir=sub_dir,
        run_name=this_run_name + "__0",
        measurement_states=["HH"],
        num_samples=samples
    )

    w.reposition_optical_component(
        orientation=orientation + step,
        component_name="C_UVHWP"
    )

    r2 = w._take_measurements(
        sub_dir=sub_dir,
        run_name=this_run_name + "__1",
        measurement_states=["HH"],
        num_samples=samples
    )

    return (float(r2["HH"]) - float(r1["HH"])) / STEP_SIZE


low_angle = w._config.calibrated_ref[
                "C_UVHWP"] + np.pi / 8 - 0.2  # float(input("Enter an underestimated phi angle of C_PCC for max DD (in radians):"))
high_angle = w._config.calibrated_ref[
                 "C_UVHWP"] + np.pi / 8 + 0.2  # float(input("Enter an overestimated phi angle of C_PCC for max DD (in radians):"))

lower_bound = Orientation(low_angle, 0)
upper_bound = Orientation(high_angle, 0)

step = Orientation(STEP_SIZE, 0)

n = 0
while True:

    new_orientation = (upper_bound + lower_bound) * (1 / 2)

    m = take_single_HH_slope_measurement_3(
        orientation=new_orientation,
        step=step,
        N=n
    )

    if m >= 0:
        lower_bound = new_orientation
    elif m < 0:
        upper_bound = new_orientation

    e = abs(m)
    print(new_orientation.theta, m)
    if e < 0.001:  # under 1000 indicates within a percent approximately.
        break

    n += 1

final_orientation = new_orientation + (step * (1 / 2))

w.reposition_optical_component(
    orientation=final_orientation,
    component_name="C_UVHWP"
)

print("HH maximized.")
print(f"C_UVHWP orientation: {final_orientation.theta}")
