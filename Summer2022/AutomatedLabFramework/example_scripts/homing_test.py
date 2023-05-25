from ast import Or
from LabWorkstation import LabWorkstation
from ConfigurationReader import ConfigReader
from Motors import Motor
from Orientation import Orientation

import numpy as np

# The purpose of this script is to determine how the Elliptec motor positioning system
# handles the homing procedure and to ensure that if the motor forgets its previous 0 position
# then our calibration can be recovered by comparing the sweeps before and after.

# Starts Workstation
w = LabWorkstation("configuration.json")

name = "C_UVHWP"
steps = 100
samples = 25

if "C_" not in name:
    raise Exception("This script should not be run on the measurement components. Only creation components.")

# Takes measurements as the UVHWP is swept from the initial to final orientation
w.take_calibration_measurements_1d(
    initial_orientation=Orientation(0, 0),
    final_orientation=Orientation(2 * np.pi, 0),
    num_steps=steps,
    num_samples=samples,
    component_name=name
)

# Tells this motor to home
component: Motor = w._get_adjustable_component(component_name=name)._motor
component.home()

# Takes more measurements as the UVHWP is swept from the initial to final orientation.
w.take_calibration_measurements_1d(
    initial_orientation=Orientation(0, 0),
    final_orientation=Orientation(2 * np.pi, 0),
    num_steps=steps,
    num_samples=samples,
    component_name=name
)
