from typing import Union

import numpy as np


class Orientation:
    def __init__(self, theta, phi):
        """
        An orientation is defined in spherical coordinates where the laser path is the "top"
        :param theta:
        :param phi:
        """
        self.theta = theta
        self.phi = phi

    def __add__(self, other):
        return Orientation(
            theta=self.theta + other.theta,
            phi=self.phi + other.phi
        )

    def __sub__(self, other):
        return Orientation(
            theta=self.theta - other.theta,
            phi=self.phi - other.phi
        )

    def __mul__(self, other: Union[int, float]):
        return Orientation(
            theta=self.theta * other,
            phi=self.phi * other
        )

    def __repr__(self):
        # prints in degrees
        return f"thet{int(360/(2* np.pi) * self.theta)}_ph{int(360/(2*np.pi) * self.phi)}"