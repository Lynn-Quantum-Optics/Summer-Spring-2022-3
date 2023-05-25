from serial import Serial
from typing import List, Dict
from time import sleep

import numpy as np

from ElliptecResponseParser import parse_elliptec_response
from Logger import Logger

try:
    import thorlabs_apt as apt

except:
    print("You are probably on a MAC aren't you?")


class MotorHub:
    def __init__(self, id):
        self.id = id
        pass

    @Logger.log_wrap
    def get_motors(self):
        raise NotImplementedError

    @Logger.log_wrap
    def close(self):
        raise NotImplementedError

    def __repr__(self):
        return f"MotorHub-{self.id}"


class ElliptecMotorHub(MotorHub):
    def __init__(self, id, com_port, motor_dict):
        super().__init__(id)

        self._com_port = com_port
        try:
            self._ser = Serial(com_port, timeout=2)
        except:
            self._ser = None
            print("Failed to open Serial Port")

        self._motors: Dict[str, Motor] = {
            address: ElliptecMotor(
                id=motor_dict[address]["ID"],
                serial_port=self._ser,
                address=address
            ) for address in motor_dict
        }

    @Logger.log_wrap
    def get_motors(self):
        return list(self._motors.values())

    @Logger.log_wrap
    def close(self):
        self._ser.close()


class ThorLabsMotorHub(MotorHub):
    def __init__(self, id, motor_dict):
        super().__init__(id)

        self._serial_number = motor_dict["Serial Number"]

        self._motor = ThorLabsMotor(
            id=motor_dict["ID"],
            serial_number=self._serial_number
        )

    @Logger.log_wrap
    def get_motors(self):
        return [self._motor]

    @Logger.log_wrap
    def close(self):
        raise NotImplementedError


class Motor:
    def __init__(self, id):
        self.id = id
        pass

    @Logger.log_wrap
    def rotate_relative(self, angle_radians, blocking=True):
        raise NotImplementedError

    @Logger.log_wrap
    def rotate_absolute(self, angle_radians, blocking=True):
        raise NotImplementedError

    @Logger.log_wrap
    def home(self, blocking=True):
        raise NotImplementedError

    @Logger.log_wrap
    def get_position(self):
        raise NotImplementedError

    @staticmethod
    def _radians_to_degrees(radians):
        return 360 * radians / (2 * np.pi)

    @staticmethod
    def _degrees_to_radians(degrees):
        return 2 * np.pi * degrees / 360

    def __repr__(self):
        return f"Motor-{self.id}"


class ThorLabsMotor(Motor):
    def __init__(self, id, serial_number):
        super().__init__(id)

        self._serial_number = serial_number

        self._motor_interface = apt.Motor(self._serial_number)

    @Logger.log_wrap
    def rotate_relative(self, angle_radians, blocking=True):
        angle = self._radians_to_degrees(angle_radians)
        self._motor_interface.move_by(angle)
        while self._motor_interface.is_in_motion and blocking:
            sleep(0.5)  # Arbitrarily chosen sleep time

    @Logger.log_wrap
    def rotate_absolute(self, angle_radians, blocking=True):
        angle = self._radians_to_degrees(angle_radians)
        self._motor_interface.move_to(angle)
        while self._motor_interface.is_in_motion and blocking:
            sleep(0.5)  # Arbitrarily chosen sleep time

    @Logger.log_wrap
    def home(self, blocking=True):
        self._motor_interface.move_home()
        while not self._motor_interface.has_homing_been_completed and blocking:
            sleep(0.5)  # Arbitrarily chosen sleep time

    @Logger.log_wrap
    def get_position(self):
        return self._degrees_to_radians(self._motor_interface.position)


class ElliptecMotor(Motor):
    def __init__(self, id, serial_port, address):
        super().__init__(id)

        self._ser = serial_port
        self._address = address

        self.home()
        sleep(10)

    @Logger.log_wrap
    def rotate_relative(self, angle_radians, blocking=True):
        self._ser.write(bytes(self._address, "utf-8") + b'mr' + self._radians_to_byte(angle_radians, 8))
        sleep(3)
        while self._in_motion() and blocking:
            sleep(0.5)

    @Logger.log_wrap
    def rotate_absolute(self, angle_radians, blocking=True):
        self._ser.write(bytes(self._address, "utf-8") + b'ma' + self._radians_to_byte(angle_radians, 8))
        sleep(3)
        while self._in_motion() and blocking:
            sleep(0.5)

    @Logger.log_wrap
    def home(self, direction=0, blocking=True):
        direction_byte = b'0' if direction == 0 else b'1'
        self._ser.write(bytes(self._address, "utf-8") + b'ho' + direction_byte)
        sleep(3)
        while self._in_motion() and blocking:
            sleep(0.5)

    @Logger.log_wrap
    def get_position(self):
        return self._degrees_to_radians(self._get_position())

    @staticmethod
    def _radians_to_byte(radians, num_bytes=8):

        degrees = Motor._radians_to_degrees(radians)

        # convert degrees to steps
        # modulo 360 because we have no use for winding and also want to specify negative angles
        decimalSteps = (degrees % 360)*(143360/360)  # 143360 steps per rotation
        
        #convert steps to hex
        decimalSteps = int(decimalSteps)
        hexSteps = hex(decimalSteps)
        
        #remove first two characters- 0x
        hexSteps = hexSteps[2:]

        #capitalize all letters 
        hexSteps = hexSteps.upper()

        #add zeroes to beginning
        zeroesNeeded = num_bytes-len(hexSteps)
        zeroString = zeroesNeeded*'0'
        hexString = zeroString+hexSteps

        return hexString.encode()

    @staticmethod
    def _bytes_to_radians(bytes):
        # This method is probably very very wrong
        
        decimalSteps = int(bytes)

        degrees = decimalSteps / (143360/360)

        return Motor._degrees_to_radians(degrees)

    def _in_motion(self):
        return False # parsing isn't fully working so return false for now.
        # self._ser.write(bytes(self._address, "utf-8") + b'i1')
        # response = ((self._ser.readall()).split(b'\r\n'))[-1]

        # return parse_elliptec_response(response)["motor"]

    def _get_position(self):
        self._ser.write(bytes(self._address, "utf-8") + b'gp')
        sleep(3)
        response = ((self._ser.readall()).split(b'\r\n'))[-1]

        return parse_elliptec_response(response)["position"]