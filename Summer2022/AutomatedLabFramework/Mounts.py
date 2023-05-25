from Logger import Logger
from Motors import Motor
from Optics import Optic
from Orientation import Orientation


class Mount:
    def __init__(self, component_id, name, optic: Optic):
        self.component_id = component_id
        self.name = name
        self.optic = optic

        # Should replace this line with a method that finds its current orientation relative to home in the case that its position has been forgotten.
        self._orientation = Orientation(theta=0, phi=0)

    @Logger.log_wrap
    def get_jones_matrix(self):
        return self.optic.get_jones_matrix(orientation=self._orientation)

    @Logger.log_wrap
    def get_orientation(self):
        return self._orientation

    def __repr__(self):
        return f"{self.name}"


class AdjustableMount(Mount):
    def __init__(self, component_id, name, optic: Optic, placement_orientation: Orientation):
        super().__init__(component_id, name, optic)
        
        self._placement_orientation = placement_orientation

        # Should replace this line with a method that finds its current orientation relative to home in the case that its position has been forgotten.
        self._orientation = Orientation(theta=0, phi=0)

    @Logger.log_wrap
    def rotate_relative(self, delta_orientation):
        raise NotImplementedError

    @Logger.log_wrap
    def rotate_absolute(self, orientation):
        raise NotImplementedError

    @Logger.log_wrap
    def get_jones_matrix(self):
        return self.optic.get_jones_matrix(orientation=self._orientation)


class LaserAxisRotationMount(AdjustableMount):
    def __init__(self, component_id, name, optic: Optic, placement_orientation):
        super().__init__(component_id, name, optic, placement_orientation)

        # Should replace this line with a method that finds its current orientation relative to home in the case that its position has been forgotten.
        self._orientation = Orientation(theta=0, phi=0)

    @Logger.log_wrap
    def rotate_relative(self, delta_orientation):
        if delta_orientation.phi != 0:
            raise Exception("Motorized Laser Axis Rotation Mounts cannot change their phi direction.")

        input(f"Rotate {self.component_id} by {self._orientation.theta}")
        self._orientation = self._orientation + delta_orientation

    @Logger.log_wrap
    def rotate_absolute(self, orientation):
        if orientation.phi != 0:
            raise Exception("Motorized Laser Axis Rotation Mounts cannot have non-zero phi direction.")

        adjusted_orientation = orientation - self._placement_orientation

        input(f"Rotate {self.component_id} to {adjusted_orientation.theta}")
        self._orientation = orientation

    @Logger.log_wrap
    def get_jones_matrix(self):
        return self.optic.get_jones_matrix(orientation=self._orientation)


class MotorizedLaserAxisRotationMount(LaserAxisRotationMount):
    def __init__(self, component_id, name, optic: Optic, placement_orientation, motor: Motor):
        super().__init__(component_id, name, optic, placement_orientation)

        self._motor = motor

        # Should replace this line with a method that finds its current orientation relative to home in the case that its position has been forgotten.
        self._orientation = Orientation(theta=0, phi=0)

    # Might want to redo this part because relative orientation changes would be better represented by a matrix.
    @Logger.log_wrap
    def rotate_relative(self, delta_orientation: Orientation):

        if delta_orientation.phi != 0:
            raise Exception("Motorized Laser Axis Rotation Mounts cannot change their phi direction.")

        self._motor.rotate_relative(delta_orientation.theta)
        self._orientation = self._orientation + delta_orientation

    @Logger.log_wrap
    def rotate_absolute(self, orientation):

        if orientation.phi != 0:
            raise Exception("Motorized Laser Axis Rotation Mounts cannot have non-zero phi direction.")

        adjusted_orientation = orientation - self._placement_orientation

        self._motor.rotate_absolute(adjusted_orientation.theta)
        self._orientation = orientation


class BaseRotationMount(AdjustableMount):
    def __init__(self, component_id, name, optic: Optic, placement_orientation):
        super().__init__(component_id, name, optic, placement_orientation)

        # Should replace this line with a method that finds its current orientation relative to home in the case that its position has been forgotten.
        self._orientation = Orientation(theta=0, phi=0)

    @Logger.log_wrap
    def rotate_relative(self, delta_orientation):
        if delta_orientation.theta != 0:
            raise Exception("Motorized Base Rotation Mounts cannot change their theta direction.")

        input(f"Rotate {self.component_id} by {self._orientation.phi}")
        self._orientation = self._orientation + delta_orientation

    @Logger.log_wrap
    def rotate_absolute(self, orientation):
        if orientation.theta != 0:
            raise Exception("Motorized Base Rotation Mounts cannot have non-zero theta direction.")

        adjusted_orientation = orientation - self._placement_orientation

        input(f"Rotate {self.component_id} to {adjusted_orientation.phi}")
        self._orientation = orientation

    @Logger.log_wrap
    def get_jones_matrix(self):
        return self.optic.get_jones_matrix(orientation=self._orientation)


class MotorizedBaseRotationMount(BaseRotationMount):
    def __init__(self, component_id, name, optic: Optic, placement_orientation, motor):
        super().__init__(component_id, name, optic, placement_orientation)

        self._motor = motor

        # Should replace this line with a method that finds its current orientation relative to home in the case that its position has been forgotten.
        self._orientation = Orientation(theta=0, phi=0)

    @Logger.log_wrap
    def rotate_relative(self, delta_orientation):
        if delta_orientation.theta != 0:
            raise Exception("Motorized Base Rotation Mounts cannot change their theta direction.")

        self._motor.rotate_relative(delta_orientation.phi)
        self._orientation = self._orientation + delta_orientation

    @Logger.log_wrap
    def rotate_absolute(self, orientation):
        if orientation.theta != 0:
            raise Exception("Motorized Base Rotation Mounts cannot have non-zero theta direction.")

        adjusted_orientation = orientation - self._placement_orientation

        self._motor.rotate_absolute(adjusted_orientation.phi)
        self._orientation = orientation
