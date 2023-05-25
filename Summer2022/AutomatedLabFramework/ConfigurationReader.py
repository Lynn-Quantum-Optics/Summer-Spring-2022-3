import datetime
import json

from Laser import Laser
from Mounts import LaserAxisRotationMount, BaseRotationMount, Mount, AdjustableMount, MotorizedLaserAxisRotationMount, \
    MotorizedBaseRotationMount
from Optics import WavePlate, HalfWavePlate, QuarterWavePlate, PolarizingBeamSplitter, QuartzPlate, \
    PreCompensationCrystal, BBOCrystal


class ConfigReader:
    def __init__(self, configuration_file):
        # read config file and populate entries

        config_file = open(configuration_file, 'r')
        self.json_data = json.load(config_file)

        self.title = self.json_data["Title"]
        self.contributors = self.json_data["Contributors"]

        now = datetime.datetime.now()
        day_string = now.strftime("%m-%d-%Y")
        self.base_directory = f"{self.json_data['Documentation']['Base Directory']}/{day_string}"

        self.log_directory = f"{self.base_directory}/{self.json_data['Documentation']['Log Directory']}"
        self.data_directory = f"{self.base_directory}/{self.json_data['Documentation']['Data Directory']}"

        self.experiment_states = self.json_data['Experiments']

        self.alice_hwp_state_ref = self.json_data["Settings"]["Alice_HWP_State_Reference"]
        self.bob_hwp_state_ref = self.json_data["Settings"]["Bob_HWP_State_Reference"]
        self.alice_qwp_state_ref = self.json_data["Settings"]["Alice_QWP_State_Reference"]
        self.bob_qwp_state_ref = self.json_data["Settings"]["Bob_QWP_State_Reference"]

        self.calibrated_ref = self.json_data["Settings"]["Calibrated_PHI_PLUS"]
        self.calibrated_ref_2 = self.json_data["Settings"]["Calibrated_HH"]

        self.unusually_low_purity = self.json_data["Settings"]["Unusually_Low_Purity"]
        self.num_samples_in_calibration_check = self.json_data["Settings"]["Num Samples in Calibration Check"]
