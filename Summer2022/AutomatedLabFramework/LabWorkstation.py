import csv
import datetime
from genericpath import exists
import time
import os
from typing import List, Union
from unittest import result

import numpy as np
import serial

from CCU import CCU
from Enums import RecordType, Experiment
from Logger import Logger
from ConfigurationReader import ConfigReader
from Laser import Laser
from Motors import ElliptecMotor, MotorHub, ElliptecMotorHub, ThorLabsMotorHub
from Mounts import Mount, MotorizedBaseRotationMount, BaseRotationMount, MotorizedLaserAxisRotationMount, \
    LaserAxisRotationMount, AdjustableMount
from Optics import WavePlate, HalfWavePlate, QuarterWavePlate, QuartzPlate, PolarizingBeamSplitter, \
    PreCompensationCrystal, BBOCrystal
from Orientation import Orientation
from QuantumHelperFunctions import evolve_density_matrix, devolve_density_matrix, calculate_expectation_value


class LabWorkstation:
    def __init__(self, config_file, debug=False):
        self._config = ConfigReader(configuration_file=config_file)
        Logger(self._config)

        self._ccu = CCU(self._config)
        self._ccu.run_log()
        time.sleep(5)  # Sleep in order to give the log time to start up.
        self._ccu.run_monitor()

        self.laser = LabWorkstation._parse_laser(self._config.json_data["Equipment"]["Laser"])

        self._motor_reference = {}

        hub_dicts = self._config.json_data["Equipment"]["Motors"]
        self._motor_hubs = []
        for raw_hub_dict_key in hub_dicts:
            if hub_dicts[raw_hub_dict_key]["Enabled"]:
                hub = LabWorkstation._parse_motor_hubs(hub_dicts[raw_hub_dict_key])
                self._motor_hubs.append(hub)

                for motor in hub.get_motors():
                    self._motor_reference[motor.id] = motor
            else:
                pass

        self._adjustable_component_reference = {}

        self._pre_pair_production_components = {}
        for raw_component_dict in self._config.json_data["Equipment"]["Pre-Pair Production Components"]:
            component = self._parse_mount(
                raw_component_dict
            )
            self._pre_pair_production_components[component.component_id] = component

            if isinstance(component, AdjustableMount):
                self._adjustable_component_reference[component.component_id] = component
                self._adjustable_component_reference[component.name] = component

        self._post_pair_production_components = {
            "Alice": {},
            "Bob": {}
        }
        for raw_component_dict in self._config.json_data["Equipment"]["Post-Pair Production Components"]["Alice"]:
            component = self._parse_mount(raw_component_dict)
            self._post_pair_production_components["Alice"][component.component_id] = component

            if isinstance(component, AdjustableMount):
                self._adjustable_component_reference[component.component_id] = component
                self._adjustable_component_reference[component.name] = component
        for raw_component_dict in self._config.json_data["Equipment"]["Post-Pair Production Components"]["Bob"]:
            component = self._parse_mount(raw_component_dict)
            self._post_pair_production_components["Bob"][component.component_id] = component

            if isinstance(component, AdjustableMount):
                self._adjustable_component_reference[component.component_id] = component
                self._adjustable_component_reference[component.name] = component

        self._pair_measurement_components = {
            "Alice": {},
            "Bob": {}
        }
        for raw_component_dict in self._config.json_data["Equipment"]["Pair Measurement Components"]["Alice"]:
            component = self._parse_mount(raw_component_dict)
            self._pair_measurement_components["Alice"][component.component_id] = component

            if isinstance(component, AdjustableMount):
                self._adjustable_component_reference[component.component_id] = component
                self._adjustable_component_reference[component.name] = component
        for raw_component_dict in self._config.json_data["Equipment"]["Pair Measurement Components"]["Bob"]:
            component = self._parse_mount(raw_component_dict)
            self._pair_measurement_components["Bob"][component.component_id] = component

            if isinstance(component, AdjustableMount):
                self._adjustable_component_reference[component.component_id] = component
                self._adjustable_component_reference[component.name] = component

        if not debug:
            self.check_calibration()

        self.take_workstation_snapshot()

        self.measurement_basis = None

    @Logger.log_wrap
    def take_calibration_measurements_1d(
            self,
            initial_orientation: Orientation,
            final_orientation: Orientation,
            num_steps: int,
            num_samples: int,
            component_name: Union[str, None] = None,
            component_id: Union[str, None] = None
    ):
        """
        Sweeps over orientations of a component and takes measurements at each orientation.
        :param num_samples: Number of samples to take at each orientation.
        :param component_id: Specify the component by id.
        :param component_name: Specify the component by name.
        :param initial_orientation: The initial orientation for the component.
        :param final_orientation: The final orientation for the component.
        :param num_steps: Number of steps to take between initial and final.
        :return:
        """

        component = self._get_adjustable_component(
            component_id=component_id,
            component_name=component_name
        )

        date_string = self.get_time_stamp_long()
        this_run_name = f"{date_string}__{component.component_id}__fr{initial_orientation}__to{final_orientation}__n{num_steps}"
        os.makedirs(f"{self._config.data_directory}/{this_run_name}", exist_ok=True)

        summary_file = open(
            f"{self._config.data_directory}/{this_run_name}/{date_string}__SUMMARY.csv", 'w', newline=''
        )
        csv_writer = csv.writer(summary_file)
        csv_writer.writerow(
            ["Theta",
             "Phi",
             "C0 (A)",
             "C0 (A) uncertainty",
             "C1 (B)",
             "C1 (B) uncertainty",
             "C2 (A')",
             "C2 (A') uncertainty",
             "C3 (B')",
             "C3 (B') uncertainty",
             "C4",
             "C4 uncertainty",
             "C5",
             "C5 uncertainty",
             "C6",
             "C6 uncertainty",
             "C7",
             "C7 uncertainty"]
        )

        # Creates a list of orientations parameterized from the initial to final orientation
        orientations: List[Orientation] = [
            final_orientation * (x / num_steps) + initial_orientation * (1 - x / num_steps) for x in
            range(num_steps + 1)
        ]

        for orientation in orientations:
            component.rotate_absolute(orientation=orientation)

            time.sleep(3)  # Arbitrarily chosen sleep time to wait for the motor to settle. May not be necessary.

            file_name = f"{self.get_time_stamp_long()}__{component.component_id}__{orientation}.csv"
            file_path = f"{self._config.data_directory}/{this_run_name}/{file_name}"

            self._ccu.run_record(
                num_samples=num_samples,
                file_path=file_path
            )

            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file)

                lines = list(csv_reader)
                final_line = lines[-1]

                csv_writer.writerow(
                    [orientation.theta, orientation.phi] + final_line[2:]
                )

    @Logger.log_wrap
    def run_measurement_experiment(
            self,
            experiment: Experiment,
            num_samples: int,
            sub_dir=None,
            name_extension=None,
            measurement_states=None
    ):
        """
        Runs a predefined experiment that measures a particular state in a variety of basis.
        :param measurement_states:
        :param name_extension:
        :param sub_dir:
        :param experiment: The experiment to be run.
        :param num_samples: The number of samples to take for each basis measurement.
        :return:
        """

        if experiment == Experiment.CUSTOM:
            if measurement_states is None:
                raise Exception("Custom experiment must have specified measurement states.")
            experiment_name = "-".join(measurement_states)
        else:
            if measurement_states is not None:
                Logger.log(
                    RecordType.Warning,
                    "A non-custom experiment will ignore measurement states listed in function call."
                )
            experiment_name = experiment.name
            measurement_states = self._config.experiment_states[experiment.name]

        this_run_name = f"{self.get_time_stamp_long()}__{experiment_name}__n{num_samples}"
        if name_extension:
            this_run_name += f"__{name_extension}"

        if not sub_dir:
            sub_dir = self.create_subdata_directory(this_run_name)
        else:
            sub_dir = f"{sub_dir}/{this_run_name}"
            os.makedirs(sub_dir, exist_ok=True)

        return self._take_measurements(sub_dir, this_run_name, measurement_states, num_samples)

    @Logger.log_wrap
    def check_calibration(self):
        """
        This method checks whether or not the calibration measurement has strayed from the original calibration by
        moving to the calibrated values and taking a purity measurement.
        :return:
        """

        self.reposition_optical_component(
            orientation=Orientation(self._config.calibrated_ref["C_UVHWP"], 0),
            component_name="C_UVHWP"
        )
        self.reposition_optical_component(
            orientation=Orientation(0, self._config.calibrated_ref["C_QP"]),
            component_name="C_QP"
        )
        self.reposition_optical_component(
            orientation=Orientation(self._config.calibrated_ref["C_PCC"], 0),
            component_name="C_PCC"
        )
        self.reposition_optical_component(
            orientation=Orientation(self._config.calibrated_ref["B_C_HWP"], 0),
            component_name="B_C_HWP"
        )

        result_dict = self.run_measurement_experiment(
            experiment=Experiment.PURITY,
            num_samples=self._config.num_samples_in_calibration_check
        )

        aa = float(result_dict["AA"])
        ad = float(result_dict["AD"])
        dd = float(result_dict["DD"])
        da = float(result_dict["DA"])
        total = aa + ad + dd + da
        purity = (dd + aa - da - ad) / total

        if purity < self._config.unusually_low_purity:
            raise Exception(f"Purity is Unusually Low at Calibration Check: {purity}")
        else:
            Logger.log(RecordType.Detail, f"Purity: {purity}")
            return purity

    @Logger.log_wrap
    def reposition_optical_component(
            self,
            orientation: Orientation,
            component_id: Union[str, None] = None,
            component_name: Union[str, None] = None
    ):
        """
        Will reposition an optical component to a new orientation.
        :param orientation: The orientation to move the component to.
        :param component_id: Specify the component by id.
        :param component_name: Specify the component by name.
        :return:
        """

        component = self._get_adjustable_component(
            component_id=component_id,
            component_name=component_name
        )

        component.rotate_absolute(orientation)
        time.sleep(2)

    @Logger.log_wrap
    def configure_bell_pair_production(self, correlation, theta, phi):
        """
        Will actuate motors or instruct the user in order to produce the desired photon pair.
        :param correlation: control whether the state should be correlated or anti-correlated
        :param theta: controls relative abundance of HH and VV or HV and VH
        :param phi: controls relative phase between HH and VV or HV and VH
        :return:
        """

        # I orginally wanted to make this function general but for simplicity it will be specific to our setup.

        if correlation:
            alpha = 0
        else:
            alpha = np.pi / 2

        self.reposition_optical_component(
            component_name="C_UVHWP",
            orientation=Orientation(theta=theta / 2, phi=0)
        )
        self.reposition_optical_component(
            component_name="C_QP",
            orientation=Orientation(theta=0, phi=phi)
        )
        self.reposition_optical_component(
            component_name="B_C_HWP",
            orientation=Orientation(theta=alpha / 2, phi=0)
        )

    @Logger.log_wrap
    def configure_measurement_basis(self, alice_basis, bob_basis):
        """
        Will actuate motors or instruct the user in order to set the desired measurement basis.
        :param alice_basis:
        :param bob_basis:
        :return:
        """

        raise Exception("This method is untested and unfinished. Use configure_measurement_basis_preset instead.")

        # The data type for alice_basis and bob_basis need to be updated they are not proper rn.
        # self._configure_measurement_bases_single("Alice", alice_basis[0], alice_basis[1])
        # self._configure_measurement_bases_single("Bob", bob_basis[0], bob_basis[1])

    @Logger.log_wrap
    def configure_measurement_basis_preset(self, state):
        """
        Set the measurement components to detect the specified states.
        :param state: A two character uppercase string that specifies two states. Ex: HD
        :return:
        """

        alice_hwp_angle = self._config.alice_hwp_state_ref[state[0]] * 2 * np.pi / 360
        bob_hwp_angle = self._config.bob_hwp_state_ref[state[1]] * 2 * np.pi / 360
        alice_qwp_angle = self._config.alice_qwp_state_ref[state[0]] * 2 * np.pi / 360
        bob_qwp_angle = self._config.bob_qwp_state_ref[state[1]] * 2 * np.pi / 360

        self.reposition_optical_component(
            component_name="A_M_HWP",
            orientation=Orientation(alice_hwp_angle, 0)
        )
        self.reposition_optical_component(
            component_name="B_M_HWP",
            orientation=Orientation(bob_hwp_angle, 0)
        )
        self.reposition_optical_component(
            component_name="A_M_QWP",
            orientation=Orientation(alice_qwp_angle, 0)
        )
        self.reposition_optical_component(
            component_name="B_M_QWP",
            orientation=Orientation(bob_qwp_angle, 0)
        )

    @Logger.log_wrap
    def get_pair_in_production(self):
        """
        Calculates and returns the state that is theoretically being produced.
        :return:
        """

        state = self.laser.state_produced  # Could add some amount of noise to this.

        for component_key in self._pre_pair_production_components:
            component = self._pre_pair_production_components[component_key]
            operator = component.get_jones_matrix()
            state = evolve_density_matrix(state, operator)

        for component_key in self._post_pair_production_components["Alice"]:
            component = self._post_pair_production_components["Alice"][component_key]
            operator = np.kron(component.get_jones_matrix(), np.matrix([[1, 0], [0, 1]]))
            state = evolve_density_matrix(state, operator)

        for component_key in self._post_pair_production_components["Bob"]:
            component = self._post_pair_production_components["Bob"][component_key]
            operator = np.kron(np.matrix([[1, 0], [0, 1]]), component.get_jones_matrix())
            state = evolve_density_matrix(state, operator)

        return state

    @Logger.log_wrap
    def get_measurement_basis(self):
        """
        Calculates the state that is theoretically being detected by the measurement components.
        :return:
        """

        measurement_basis = np.matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        operator = np.kron(np.matrix([[1, 0], [0, 1]]), np.matrix([[1, 0], [0, 1]]))
        for component_key in self._pair_measurement_components["Alice"]:
            component = self._pair_measurement_components["Alice"][component_key]
            operator = np.kron(component.get_jones_matrix(), np.matrix([[1, 0], [0, 1]])) * operator
            print(operator)
        measurement_basis = devolve_density_matrix(measurement_basis, operator)

        operator = np.kron(np.matrix([[1, 0], [0, 1]]), np.matrix([[1, 0], [0, 1]]))
        for component_key in self._pair_measurement_components["Bob"]:
            component = self._pair_measurement_components["Bob"][component_key]
            operator = np.kron(np.matrix([[1, 0], [0, 1]]), component.get_jones_matrix()) * operator
        measurement_basis = devolve_density_matrix(measurement_basis, operator)

        return measurement_basis

    @Logger.log_wrap
    def get_theoretical_counts(self):
        """
        Calculates the theoretical number of counts that we'd expect to see for a state.
        :return:
        """
        state = self.get_pair_in_production()

        for component_key in self._pair_measurement_components["Alice"]:
            component = self._pair_measurement_components["Alice"][component_key]
            operator = np.kron(np.matrix([[1, 0], [0, 1]]), component.get_jones_matrix())
            state = evolve_density_matrix(state, operator, normalize=False)

        for component_key in self._pair_measurement_components["Bob"]:
            component = self._pair_measurement_components["Bob"][component_key]
            operator = np.kron(np.matrix([[1, 0], [0, 1]]), component.get_jones_matrix())
            state = evolve_density_matrix(state, operator, normalize=False)

        return calculate_expectation_value(
            state,
            np.kron(
                np.matrix([
                    [1, 0],
                    [0, 0]
                ]),
                np.matrix([
                    [1, 0],
                    [0, 0]
                ])
            )
        )

    @Logger.log_wrap
    def take_workstation_snapshot(self, filepath=None):
        """
        This method writes the current position of each component to a file and saves it.
        :param filepath: Where to save the snapshot.
        :return:
        """
        if filepath:
            pass
        else:
            filepath = self._config.log_directory
        with open(f"{filepath}/{self.get_time_stamp_long()}__snapshot.csv", 'w', newline='') as snapshot_file:
            csv_writer = csv.writer(snapshot_file)
            csv_writer.writerow([
                "Component", "Orientation"
            ])
            csv_writer.writerows(
                [[f"{mount}", f"{self._adjustable_component_reference[mount].get_orientation()}"] for mount in
                 self._adjustable_component_reference if not (type(mount) is int)]
            )

    def create_subdata_directory(self, run_name):
        """
        Creates a folder for a particular run of measurements.
        :param run_name: Name of directory.
        :return:
        """
        subdirectory = f"{self._config.data_directory}/{run_name}"
        os.makedirs(subdirectory, exist_ok=True)

        return subdirectory

    def _configure_measurement_bases_single(self, path, gamma, phi):
        """
        Configures a single measurement pathway (Bob or Alice) to detect a specific single qubit state.
        :param path: Can be Bob or Alice.
        :param gamma: Skew parameter in single qubit expression.
        :param phi: Phase parameter in single qubit expression.
        :return:
        """

        if phi == np.pi / 2:
            alpha = gamma
            beta = 0
        elif gamma == np.pi / 2:
            alpha = 0
            beta = gamma
        else:
            A = (np.tan(gamma)) ** 2
            B = - np.tan(phi)

            if A == 0 or B == 0:
                x = 0
            else:
                C = A ** 2 + 1 + (A + 1) ** 2 / B ** 2
                x = np.sqrt(C + np.sqrt((C ** 2 - 4 * A ** 2)) / (2 * A))

            y = np.sqrt((x - A ** 2) / (A * x ** 2 - 1))

            alpha = np.arctan(x)
            beta = np.arctan(y)

        theta = 1 / 2 * (alpha + beta)

        # HWP
        component_name = path[0] + "_M_HWP"
        orientation = Orientation(theta=theta, phi=0)
        self.reposition_optical_component(
            component_name=component_name,
            orientation=orientation
        )

        # QWP
        component_name = path[0] + "_M_QWP"
        orientation = Orientation(theta=alpha, phi=0)
        self.reposition_optical_component(
            component_name=component_name,
            orientation=orientation
        )

    def _get_adjustable_component(self, component_id=None, component_name=None):
        """
        Takes in the two options for specifying a component and finds that component (if it is adjustable).
        :param component_id: Specify component by id.
        :param component_name: Specify component by name
        :return:
        """
        try:
            if component_id:
                component = self._adjustable_component_reference[component_id]
            elif component_name:
                component = self._adjustable_component_reference[component_name]
            else:
                raise Exception("No Component ID or Component Name Provided.")
        except KeyError:
            raise Exception("Component Could Not Be Identified. It may not be an adjustable component.")

        return component

    def _take_measurements(self, sub_dir, run_name, measurement_states, num_samples):
        """
        Takes all the measurements corresponding to the states in measurement states. Saves them in specified dir.
        :param sub_dir:
        :param run_name:
        :param measurement_states:
        :param num_samples:
        :return:
        """

        summary_file = open(f"{sub_dir}/{run_name}__SUMMARY.csv", 'w', newline='')
        csv_writer = csv.writer(summary_file)
        csv_writer.writerow(
            [
                "State",
                "C0 (A)",
                "C0 (A) uncertainty",
                "C1 (B)",
                "C1 (B) uncertainty",
                "C2 (A')",
                "C2 (A') uncertainty",
                "C3 (B')",
                "C3 (B') uncertainty",
                "C4",
                "C4 uncertainty",
                "C5",
                "C5 uncertainty",
                "C6",
                "C6 uncertainty",
                "C7",
                "C7 uncertainty"
            ]
        )

        results_dict = {}

        for state in measurement_states:
            self.configure_measurement_basis_preset(state)

            time.sleep(2)  # Arbitrarily chosen sleep time to wait for the motor to settle. May not be necessary.

            file_name = f"{self.get_time_stamp_long()}__{state}.csv"
            file_path = f"{sub_dir}/{file_name}"

            self._ccu.run_record(
                num_samples=num_samples,
                file_path=file_path
            )

            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file)

                lines = list(csv_reader)
                final_line = lines[-1]

                csv_writer.writerow(
                    [state] + final_line[2:]
                )

                results_dict[state] = float(final_line[10])

        return results_dict

    def _parse_mount(self, raw_mount_dict):
        optical_component = LabWorkstation._parse_optic(raw_mount_dict["Optic"])
        component_id = raw_mount_dict["Component ID"]
        name = raw_mount_dict["Name"]

        if raw_mount_dict["Type"] == "Laser Axis Rotation Mount":
            mount = LaserAxisRotationMount(
                component_id=component_id,
                name=name,
                optic=optical_component,
                placement_orientation=LabWorkstation._parse_orientation(raw_mount_dict["Placement Orientation"])
            )
        elif raw_mount_dict["Type"] == "Motorized Laser Axis Rotation Mount":
            try:
                motor = self._motor_reference[raw_mount_dict["Motor ID"]]
                mount = MotorizedLaserAxisRotationMount(
                    component_id=component_id,
                    name=name,
                    optic=optical_component,
                    placement_orientation=LabWorkstation._parse_orientation(raw_mount_dict["Placement Orientation"]),
                    motor=motor
                )
            except KeyError:
                mount = LaserAxisRotationMount(
                    component_id=component_id,
                    name=name,
                    optic=optical_component,
                    placement_orientation=LabWorkstation._parse_orientation(raw_mount_dict["Placement Orientation"])
                )
        elif raw_mount_dict["Type"] == "Base Rotation Mount":
            mount = BaseRotationMount(
                component_id=component_id,
                name=name,
                optic=optical_component,
                placement_orientation=LabWorkstation._parse_orientation(raw_mount_dict["Placement Orientation"])
            )
        elif raw_mount_dict["Type"] == "Motorized Base Rotation Mount":
            try:
                motor = self._motor_reference[raw_mount_dict["Motor ID"]]
                mount = MotorizedBaseRotationMount(
                    component_id=component_id,
                    name=name,
                    optic=optical_component,
                    placement_orientation=LabWorkstation._parse_orientation(raw_mount_dict["Placement Orientation"]),
                    motor=motor
                )
            except KeyError:
                mount = BaseRotationMount(
                    component_id=component_id,
                    name=name,
                    optic=optical_component,
                    placement_orientation=LabWorkstation._parse_orientation(raw_mount_dict["Placement Orientation"])
                )
        elif raw_mount_dict["Type"] == "Standard":
            mount = Mount(
                component_id=component_id,
                name=name,
                optic=optical_component
            )
        else:
            raise Exception(f"Unknown Mount Type Specified: {raw_mount_dict['Type']}")

        return mount

    @staticmethod
    def get_time_stamp_long():
        now = datetime.datetime.now()
        date_string = now.strftime("%m-%d-%Y_%H-%M-%S")
        return date_string

    @staticmethod
    def get_time_stamp_short():
        now = datetime.datetime.now()
        date_string = now.strftime("%m-%d-%Y")
        return date_string

    @staticmethod
    def _parse_laser(raw_laser_dict):
        if raw_laser_dict["Type"] == "Standard":
            return Laser(
                title=raw_laser_dict["Title"],
                polarization=raw_laser_dict["Polarization"],
                serial_number=raw_laser_dict["Serial Number"]
            )
        else:
            raise Exception(f"Unknown Laser Type Specified: {raw_laser_dict['Type']}")

    @staticmethod
    def _parse_orientation(raw_orientation_dict):
        return Orientation(**raw_orientation_dict)

    @staticmethod
    def _parse_motor_hubs(raw_motor_hub_dict):
        if raw_motor_hub_dict["Type"] == "Elliptec":
            com_port = raw_motor_hub_dict["Com Port"]
            addresses = raw_motor_hub_dict["Addresses"]
            motor_hub = ElliptecMotorHub(
                id=raw_motor_hub_dict["ID"],
                com_port=com_port,
                motor_dict=addresses
            )
        elif raw_motor_hub_dict["Type"] == "Thor Labs":
            motor_hub = ThorLabsMotorHub(
                id=raw_motor_hub_dict["ID"],
                motor_dict=raw_motor_hub_dict["Motor"]
            )
        else:
            raise Exception(f"Unknown Mount Type Specified: {raw_motor_hub_dict['Type']}")
        return motor_hub

    @staticmethod
    def _parse_optic(raw_optic_dict):
        if raw_optic_dict["Type"] == "WP":
            optic = WavePlate(phase_shift=raw_optic_dict["Phase Shift"])
        elif raw_optic_dict["Type"] == "HWP":
            optic = HalfWavePlate()
        elif raw_optic_dict["Type"] == "QWP":
            optic = QuarterWavePlate()
        elif raw_optic_dict["Type"] == "QP":
            optic = QuartzPlate(
                thickness=raw_optic_dict["Thickness(mm)"],
                linear_phase_shift_density=raw_optic_dict["Linear Phase Shift Density(rad/mm)"]
            )
        elif raw_optic_dict["Type"] == "PBS":
            optic = PolarizingBeamSplitter()
        elif raw_optic_dict["Type"] == "PCC":
            optic = PreCompensationCrystal(
                wavelength_dependent_internal_phase_shift=raw_optic_dict["Wavelength Dependent Internal Phase Shift"]
            )
        elif raw_optic_dict["Type"] == "BBO":
            optic = BBOCrystal(
                internal_phase_shift=raw_optic_dict["Internal Phase Shift"],
                wavelength_dependent_internal_phase_shift=raw_optic_dict["Wavelength Dependent Internal Phase Shift"]
            )
        else:
            raise Exception(f"Unknown Optic Type Specified: {raw_optic_dict['Type']}")

        return optic

    def __repr__(self):
        return f"{self._config.title}: Lab Automation Framework"

    def __del__(self):
        self.take_workstation_snapshot(
            filepath=self._config.log_directory
        )
