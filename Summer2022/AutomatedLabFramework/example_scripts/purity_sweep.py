from ast import Or
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

# The purpose of this example is to show how you can create your own procedure that saves and processes data in
# a way that is different from existing procedures. In this case instead of summarizing raw averages from each
# detection state our summary file will compile the results of a sweep of complete purity experiments.

# Starts Workstation
w = LabWorkstation("configuration.json")

# Isolates a particular component
component_name = "B_C_HWP"

# Sets initial and final orientation for this sweep
initial_orientation = Orientation(2.2007 - 0.1, 0)
final_orientation = Orientation(2.2007 + 0.1, 0)

num_steps = 10


date_string = w.get_time_stamp_long()
this_run_name = f"{date_string}__{component_name}__fr{initial_orientation}__to{final_orientation}__n{num_steps}"
sub_dir = w.create_subdata_directory(this_run_name)

# Creates a summary file in the directory
summary_file = open(
    f"{sub_dir}/{date_string}__SUMMARY.csv", 'w', newline=''
)
csv_writer = csv.writer(summary_file)
csv_writer.writerow(
    ["Theta",
     "Phi",
     "Purity"]
)

orientations = [
    final_orientation * (x / num_steps) + initial_orientation * (1 - x / num_steps) for x in
    range(num_steps + 1)
]
for orientation in orientations:
    w.reposition_optical_component(orientation=orientation, component_name=component_name)

    time.sleep(3)  # Arbitrarily chosen sleep time to wait for the motor to settle. May not be necessary.

    # This line runs an purity experiment
    p = w.run_measurement_experiment(
        experiment=Experiment.PURITY,
        num_samples=5,
        sub_dir=sub_dir,
        name_extension=f"{orientation}"
    )

    aa = float(p["AA"])
    dd = float(p["DD"])
    ad = float(p["AD"])
    da = float(p["DA"])

    p = (aa + dd - ad - da) / (aa + dd + ad + da)

    csv_writer.writerow(
        [orientation.theta, orientation.phi] + [p]
    )
