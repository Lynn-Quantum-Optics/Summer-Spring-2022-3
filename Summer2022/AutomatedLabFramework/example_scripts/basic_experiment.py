from ast import Or

from Enums import Experiment
from LabWorkstation import LabWorkstation
from ConfigurationReader import ConfigReader
from Motors import Motor
from Orientation import Orientation

import numpy as np

# The purpose of this script is to show a basic experiment in which
# a state is prepared and then a set of measurement is taken.

# Starts Workstation
w = LabWorkstation("configuration.json")

# Positions Optical Components
w.reposition_optical_component(
    orientation=Orientation(0, 0),
    component_name="C_UVHWP"
)
w.reposition_optical_component(
    orientation=Orientation(0, 0),
    component_name="C_QP"
)

# Runs a particular experiment
results = w.run_measurement_experiment(
    experiment=Experiment.BELL,
    num_samples=25
)

# Does something with the results.
print(f"VP: {results['VP']}")
