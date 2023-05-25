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

# This script is broken but its purpose in principle is to quickly locate a maximum of DD on the Quartz plate.
# It is too sensitive to noise and additionally when calibrating it is much better to minimize a value than to
# maximize a value.

w = LabWorkstation("configuration.json")

w.reposition_optical_component(
    orientation=Orientation(w._config.calibrated_ref["C_UVHWP"], 0),
    component_name="C_UVHWP"
)

STEP_SIZE = 0.02


def take_single_DD_slope_measurement(orientation, step, N, samples=50):
    now = datetime.datetime.now()
    date_string = now.strftime("%m-%d-%Y_%H-%M-%S")
    this_run_name = f"{date_string}__DD_slope__n{samples}__{N}"

    sub_dir = w.create_subdata_directory(this_run_name)

    w.reposition_optical_component(
        orientation=orientation,
        component_name="C_QP"
    )

    r1 = w._take_measurements(
        sub_dir=sub_dir,
        run_name=this_run_name + "__0",
        measurement_states=["DD"],
        num_samples=samples
    )

    w.reposition_optical_component(
        orientation=orientation + step,
        component_name="C_QP"
    )

    r2 = w._take_measurements(
        sub_dir=sub_dir,
        run_name=this_run_name + "__1",
        measurement_states=["DD"],
        num_samples=samples
    )

    return (float(r2["DD"]) - float(r1["DD"])) / STEP_SIZE


low_angle = float(input("Enter an underestimated phi angle of C_QP for max DD (in radians):"))
high_angle = float(input("Enter an overestimated phi angle of C_QP for max DD (in radians):"))

lower_bound = Orientation(0, low_angle)
upper_bound = Orientation(0, high_angle)

step = Orientation(0, STEP_SIZE)

n = 0
while True:

    new_orientation = (upper_bound + lower_bound) * (1 / 2)

    m = take_single_DD_slope_measurement(
        orientation=new_orientation,
        step=step,
        N=n
    )

    if m >= 0:
        lower_bound = new_orientation
    elif m < 0:
        upper_bound = new_orientation

    e = abs(m)
    print(new_orientation.phi, m)
    if e < 0.001:  # under 1000 indicates within a percent approximately.
        break

    n += 1

final_orientation = new_orientation + (step * (1 / 2))

w.reposition_optical_component(
    orientation=final_orientation,
    component_name="C_QP"
)

print("DD maximized.")
print(f"new C_QP orientation: {final_orientation.phi}")
