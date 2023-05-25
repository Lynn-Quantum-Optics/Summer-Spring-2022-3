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
print("The general form for a state that the automated workstation can produce is as follows:")
print("cos theta cos alpha |HH>")
print("+ cos theta sin alpha |HV>")
print("+ sin theta sin alpha e^(i phi) |VH>")
print("+ sin theta cos alpha e^(i phi) |VV>")

print("Note that it is hard for this procedure to acquire setting that are close to maxima or minima in this basis.")

THETA = float(input("Enter desired theta value here:"))
ALPHA = float(input("Enter desired alpha value here:"))
PHI = float(input("Enter desired phi value here:"))

# After initializing the workstation which performs a purity check the state
# being produced should be PHI PLUS. This is important only in that B_C_HWP
# is set to produce HH or VV instead of HV or VH, etc.
w = LabWorkstation("configuration.json")

print("Now acquiring THETA by balancing HH and VV counts...")
RATIO = (np.cos(THETA) ** 2) / (np.sin(THETA) ** 2)

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

print("----------- THETA acquired. -----------")
uv_hwp_orientation = new_orientation

print("Now acquiring ALPHA by balancing HH and HV counts...")
RATIO = (np.cos(ALPHA) ** 2) / (np.sin(ALPHA) ** 2)

w.reposition_optical_component(
    orientation=Orientation(w._config.calibrated_ref_2["C_UVHWP"], 0),
    component_name="C_UVHWP"
)
w.reposition_optical_component(
    orientation=Orientation(0, w._config.calibrated_ref_2["C_QP"]),
    component_name="C_QP"
)

date_string = w.get_time_stamp_long()
this_run_name = f"{date_string}__balancing_HH-HV__n{SAMPLES}"
sub_dir = w.create_subdata_directory(this_run_name)


def take_single_HH_HV_measurement(n_):
    return w.run_measurement_experiment(
        experiment=Experiment.CUSTOM,
        num_samples=SAMPLES,
        sub_dir=sub_dir,
        name_extension=f"{n_}",
        measurement_states=["HH", "HV"]
    )


n = 0

w.reposition_optical_component(
    orientation=Orientation(0, 0),
    component_name="B_C_HWP"
)

r0 = take_single_HH_HV_measurement(n)
n += 1

if r0["HH"] / r0["HV"] >= RATIO:
    lower_bound = Orientation(-np.pi / 4, 0)

    r = r0
    while True:

        w.reposition_optical_component(
            orientation=lower_bound,
            component_name="B_C_HWP"
        )

        r = take_single_HH_HV_measurement(n)
        n += 1

        if r["HH"] / r["HV"] < RATIO:
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
            component_name="B_C_HWP"
        )

        r = take_single_HH_HV_measurement(n)
        n += 1

        if r["HH"] / r["HV"] >= RATIO:
            break
        else:
            upper_bound -= Orientation(0.1, 0)

            if upper_bound.theta < 0:
                raise Exception("Failed to find upper bound for iteration.")

while True:

    new_orientation = (upper_bound + lower_bound) * (1 / 2)

    w.reposition_optical_component(
        orientation=new_orientation,
        component_name="B_C_HWP"
    )

    m = take_single_HH_HV_measurement(n)

    if m["HH"] / m["HV"] >= RATIO:
        upper_bound = new_orientation
    else:
        lower_bound = new_orientation

    e = abs(m["HH"] / m["HV"] - RATIO) / RATIO
    print(m["HH"] / m["HV"], e)
    if e < 0.01:
        break

    n += 1

print("----------- ALPHA acquired. -----------")
bobs_c_hwp_orientation = new_orientation

print("Now acquiring PHI by balancing DD and DA counts...")
RATIO = (1 + np.cos(PHI)) / (1 - np.cos(PHI))

# Acquire one bound by maximizing DD
# Acquire another bound by maximizing DA

w.reposition_optical_component(
    orientation=Orientation(w._config.calibrated_ref["C_UVHWP"], 0),
    component_name="C_UVHWP"
)
w.reposition_optical_component(
    orientation=Orientation(w._config.calibrated_ref["B_C_HWP"], 0),
    component_name="B_C_HWP"
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

w.configure_measurement_basis_preset("DA")

w.take_calibration_measurements_1d(
    initial_orientation=LEFT_BOUND,
    final_orientation=RIGHT_BOUND,
    num_steps=50,
    num_samples=10,
    component_name="C_QP"
)

# TODO: Automate these two actions

print("Open the DD sweep file and estimate the peak closest to the center of the plot.")
DD_max = float(input("Estimate this value:"))

print("Open the DA sweep file and estimate the peak closest to the center of the plot.")
DA_max = float(input("Estimate this value:"))

date_string = w.get_time_stamp_long()
this_run_name = f"{date_string}__balancing_DD-DA__n{SAMPLES}"
sub_dir = w.create_subdata_directory(this_run_name)


def take_single_DD_DA_measurement(n_):
    return w.run_measurement_experiment(
        experiment=Experiment.CUSTOM,
        num_samples=SAMPLES,
        sub_dir=sub_dir,
        name_extension=f"{n_}",
        measurement_states=["DD", "DA"]
    )


upper_bound = Orientation(0, DD_max)
lower_bound = Orientation(0, DA_max)


while True:

    new_orientation = (upper_bound + lower_bound) * (1 / 2)

    w.reposition_optical_component(
        orientation=new_orientation,
        component_name="C_QP"
    )

    m = take_single_DD_DA_measurement(n)

    if m["DD"] / m["DA"] >= RATIO:
        upper_bound = new_orientation
    else:
        lower_bound = new_orientation

    e = abs(m["DD"] / m["DA"] - RATIO) / RATIO
    print(m["DD"] / m["DA"], e)
    if e < 0.01:
        break

    n += 1

print("----------- PHI acquired. -----------")
c_qp_orientation = new_orientation

print("Moving components to acquired positions...")

w.reposition_optical_component(
    orientation=Orientation(uv_hwp_orientation, 0),
    component_name="C_UVHWP"
)
w.reposition_optical_component(
    orientation=Orientation(0, c_qp_orientation),
    component_name="C_QP"
)
w.reposition_optical_component(
    orientation=Orientation(bobs_c_hwp_orientation, 0),
    component_name="B_C_HWP"
)