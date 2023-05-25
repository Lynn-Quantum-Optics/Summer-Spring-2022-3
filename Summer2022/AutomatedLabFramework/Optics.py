import numpy as np

from Orientation import Orientation


class Optic:
    def __init__(self, jones_matrix_func):
        """
        An arbitrary optic.
        :param jones_matrix_func:
        """
        self._jones_matrix_func = jones_matrix_func

    def get_jones_matrix(self, orientation: Orientation):
        return self._jones_matrix_func(orientation)

    def get_reverse_jones_matrix(self, orientation: Orientation):
        reverse_orientation = Orientation(
            theta=-orientation.theta,
            phi=-orientation.phi
        )
        return self._jones_matrix_func(reverse_orientation)

    def __repr__(self):
        return f"{self.__class__}"


class WavePlate(Optic):
    def __init__(self, phase_shift):
        """
        A general form for a wave plate that produces a specified phase shift.
        :param phase_shift:
        """
        def wp_jones_matrix_func(orientation: Orientation):
            if orientation.phi != 0:
                raise Exception("Framework does not support non-perpendicular wave plates.")

            coeff = np.exp(-1 * phase_shift * 1j / 2)
            matrix = np.matrix([
                [(np.cos(orientation.theta))**2 + np.exp(phase_shift * 1j) * (np.sin(orientation.theta))**2,
                 (1 - np.exp(phase_shift * 1j)) * np.sin(orientation.theta) * np.cos(orientation.theta)],

                [(1 - np.exp(phase_shift * 1j)) * np.sin(orientation.theta) * np.cos(orientation.theta),
                 (np.sin(orientation.theta))**2 + np.exp(phase_shift * 1j) * (np.cos(orientation.theta))**2]
            ])
            return coeff * matrix

        super().__init__(wp_jones_matrix_func)


class HalfWavePlate(WavePlate):
    def __init__(self):
        """
        A wave plate that specifically adds a pi/2 phase shift
        """
        super().__init__(phase_shift=np.pi)


class QuarterWavePlate(WavePlate):
    def __init__(self):
        """
        A wave plate that specifically adds a pi/4 phase shift
        """
        super().__init__(phase_shift=np.pi / 2)


class QuartzPlate(Optic):
    def __init__(self, thickness, linear_phase_shift_density):
        """
        A Quartz Plate is similar to a HWP or a QWP but instead of adjusting the laser axis rotation of the crystal we adjust the base rotation angle in order to make the path that light takes through the crystal somewhat longer or shorter thereby adjusting the phase shift introduces by the plate.
        :param thickness:
        :param linear_phase_shift_density:
        """

        self._thickness = thickness
        self._linear_phase_shift_density = linear_phase_shift_density

        def qp_jones_matrix_func(orientation: Orientation):
            if orientation.theta != 0:
                raise Exception("Framework does not support laser axis rotation of quartz plates.")

            light_path_length = self._thickness / np.cos(orientation.phi)
            phase_shift = light_path_length * self._linear_phase_shift_density

            return np.matrix([
                [1, 0],
                [0, np.exp(1j * phase_shift)]
            ])
            # raise NotImplementedError

        super().__init__(qp_jones_matrix_func)

    def phase_shift_to_orientation(self, phase_shift):
        path_length = phase_shift / self._linear_phase_shift_density

        step = 2 * np.pi / self._linear_phase_shift_density
        while path_length < self._thickness:
            path_length += step

        phi = np.arccos(self._thickness / path_length)

        return Orientation(theta=0, phi=phi)


class PolarizingBeamSplitter(Optic):
    def __init__(self):
        """
        A polarizing beam splitter allows horizontally polarized light to pass through and reflects vertically polarized light perpendicularly. In our application it is functioning only as a horizontal polarizing filter because we are not using the beam of vertically polarized light. This comment is too specific to our application and doesn't belong in this docstring.
        """

        def pbs_jones_matrix_func(orientation: Orientation):
            return np.matrix([
                [1, 0],
                [0, 0]
            ])

        super().__init__(pbs_jones_matrix_func)


class PreCompensationCrystal(Optic):
    def __init__(self, wavelength_dependent_internal_phase_shift):
        """
        A PreCompensation Crystal applies a wavelength dependent phase shift in order to compensate for the wavelength depended phase shift in the subsequent BBO Crystal.
        """

        self._wavelength_dependent_internal_phase_shift = wavelength_dependent_internal_phase_shift

        def pcc_jones_matrix_func(orientation: Orientation):
            if orientation.theta != 0 or orientation.phi != 0:
                raise Exception("Framework does not alternate orientations of a PCC crystal")
            return np.matrix([
                [1, 0],
                [0, np.exp(1j * self._wavelength_dependent_internal_phase_shift)]
            ])
            # raise NotImplementedError

        super().__init__(pcc_jones_matrix_func)


class BBOCrystal(Optic):
    def __init__(self, internal_phase_shift, wavelength_dependent_internal_phase_shift):
        """
        A BBO crystal will (occasionally) convert |H> to |HH> and |V> to e^(i theta(lambda) + i phi)|VV> where theta and phi are constants of the crystal. In this class "internal_phase_shift" = phi and "wavelength_dependent_internal_phase_shift" = theta. This phase shift is wavelength dependent which is not represented in the model this framework uses.
        :param internal_phase_shift:
        """

        self._internal_phase_shift = internal_phase_shift
        self._wavelength_dependent_internal_phase_shift = wavelength_dependent_internal_phase_shift

        def bbo_jones_matrix_func(orientation: Orientation):
            if orientation.theta != 0 or orientation.phi != 0:
                raise Exception("Framework does not alternate orientations of a BBO crystal")
            return np.matrix([
                [0, np.exp(1j * self._internal_phase_shift + 1j * self._wavelength_dependent_internal_phase_shift)],
                [0, 0],
                [0, 0],
                [1, 0]
            ])
            # raise NotImplementedError

        super().__init__(bbo_jones_matrix_func)