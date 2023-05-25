import numpy as np

from Logger import Logger


class Laser:
    def __init__(self, title, polarization, serial_number):
        self.title = title
        self.polarization = polarization
        self.serial_number = serial_number

        if polarization == "Horizontal":
            self.state_produced = np.matrix(
                [[1, 0],
                 [0, 0]]
            )
        elif polarization == "Vertical":
            self.state_produced = np.matrix(
                [[0, 0],
                 [0, 1]]
            )
        else:
            raise Exception(f"Unknown Polarization Specified: {polarization}")

    def __repr__(self):
        return f"{self.title}"
