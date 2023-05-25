from ast import Or
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


SAMPLES = int(input("Enter number of samples to take per measurement:"))
RATIO = float(input("Enter desired ratio HH/VV:"))

print("Now balancing HH and VV...")

if RATIO <= 0:
    raise Exception("Ratio must be non-zero and positive.")

# After initializing the workstation which performs a purity check the state
# being produced should be PHI PLUS. This is important only in that B_C_HWP
# is set to produce HH or VV instead of HV or VH, etc.
w = LabWorkstation("configuration.json")

date_string = w.get_time_stamp_long()
this_run_name = f"{date_string}__balancing_HH-VV__n{SAMPLES}"
sub_dir = w.create_subdata_directory(this_run_name)


def take_single_HH_VV_measurement(n_):
    return w.run_measurement_experiment(
        experiment=Experiment.CUSTOM,
        num_samples=SAMPLES,
        sub_dir=sub_dir,
        name_extension=f"{n_}",
        measurement_states=["HH", "VV"]
    )


n = 0

w.reposition_optical_component(
    orientation=Orientation(0, 0),
    component_name="C_UVHWP"
)

r0 = take_single_HH_VV_measurement(n)
n += 1

if r0["HH"] / r0["VV"] >= RATIO:
    lower_bound = Orientation(-np.pi / 4, 0)

    r = r0
    while True:

        w.reposition_optical_component(
            orientation=lower_bound,
            component_name="C_UVHWP"
        )

        r = take_single_HH_VV_measurement(n)
        n += 1

        if r["HH"] / r["VV"] < RATIO:
            break
        else:
            lower_bound += Orientation(0.1, 0)

            if lower_bound.theta > 0:
                raise Exception("Failed to find lower bound for iteration.")

    upper_bound = Orientation(0, 0)
else:
    lower_bound = Orientation(0, 0)

    upper_bound = Orientation(np.pi / 4, 0)

    r = r0
    while True:

        w.reposition_optical_component(
            orientation=upper_bound,
            component_name="C_UVHWP"
        )

        r = take_single_HH_VV_measurement(n)
        n += 1

        if r["HH"] / r["VV"] >= RATIO:
            break
        else:
            upper_bound -= Orientation(0.1, 0)

            if upper_bound.theta < 0:
                raise Exception("Failed to find upper bound for iteration.")

while True:

    new_orientation = (upper_bound + lower_bound) * (1 / 2)

    w.reposition_optical_component(
        orientation=new_orientation,
        component_name="C_UVHWP"
    )

    m = take_single_HH_VV_measurement(n)

    if m["HH"] / m["VV"] >= RATIO:
        upper_bound = new_orientation
    else:
        lower_bound = new_orientation

    e = abs(m["HH"] / m["VV"] - RATIO) / RATIO
    print(m["HH"] / m["VV"], e)
    if e < 0.01:
        break

    n += 1

w.reposition_optical_component(
    orientation=new_orientation,
    component_name="C_UVHWP"
)

print("HH and VV balanced.")
print(f"balanced C_UVHWP orientation: {new_orientation.theta}")
