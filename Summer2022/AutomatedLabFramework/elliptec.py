# imports 

from time import sleep
import numpy as np
import serial
import thorlabs_apt as apt

# motor info dictionary

MOTORS = dict()
COM_PORTS = dict()

class Motor:
    ''' Base class for all motors.

    Essentially just manages the MOTORS dict and supplies methods that will be implemented by each motor type.

    Parameters
    ----------
    name : str
        The unique name for the motor.
    type : str
        The type of motor.

    Raises
    ------
    AttributeError
        If the name is not unique.
    '''
    def __init__(self, name:str, type:str):
        # check name is unique
        if name in MOTORS:
            raise AttributeError(f"Motor with name \"{name}\" already exists.")

        # set attributes
        self.name = name
        self.type = type

        # add self to MOTORS dict
        MOTORS[self.name] = self

    def __repr__(self):
        return f"Motor-{self.name}"
    
    def __str__(self):
        return self.__repr__()

    def rotate_relative(self, angle_radians:float, blocking:bool=True) -> None:
        ''' Rotates the motor by a relative angle.

        Parameters
        ----------
        angle_radians : float
            The angle to rotate by, in radians.
        blocking : bool, optional
            Whether to block until the motor has finished rotating. Default is True.
        '''
        raise NotImplementedError

    def rotate_absolute(self, angle_radians:float, blocking:bool=True):
        ''' Rotates the motor to an absolute angle.

        Parameters
        ----------
        angle_radians : float
            The angle to rotate by, in radians.
        blocking : bool, optional
            Whether to block until the motor has finished rotating. Default is True.
        '''
        raise NotImplementedError

    def home(self, blocking=True):
        ''' Bring the motor to its home position. '''
        raise NotImplementedError

    def get_position(self) -> float:
        ''' Get the position of the motor. '''
        raise NotImplementedError

class ElliptecMotor(Motor):
    ''' Elliptec Motor class.
    
    Parameters
    ----------
    name : str
        The unique name for the motor.
    com_port : str
        The COM port the motor is connected to.
    address : bytes
        The address of the motor, a single byte.
    '''
    def __init__(self, name:str, com_port:str, address:bytes):
        # call superclass
        super().__init__(name, 'Elliptec')

        # set attributes
        self.com_port = self._get_com_port(com_port) # gets serial object
        self.address = address
        self.ppmu = self._get_ppmu() # pulse per measurement unit

    # status codes
    ELLIPTEC_STATUS_CODES = {
        b'00': 'ok',
        b'01': 'communication time out',
        b'02': 'mechanical time out',
        b'03': 'invalid command',
        b'04': 'value out of range',
        b'05': 'module isolated',
        b'06': 'module out of isolation',
        b'07': 'initializing error',
        b'08': 'thermal error',
        b'09': 'busy',
        b'10': 'sensor error',
        b'11': 'motor error',
        b'12': 'out of range error',
        b'13': 'over current error'}

    # built in methods

    def __repr__(self) -> str:
        return f'ElliptecMotor-{self.name}'
    
    # helper functions

    def _get_com_port(self, com_port:str) -> serial.Serial:
        ''' Retrieves the COM port Serial object. Opens a connection if necessary. '''
        # check if COM port is already open
        if com_port in COM_PORTS:
            return COM_PORTS[com_port]
        # otherwise open COM port
        else:
            try:
                ser = serial.Serial(com_port, timeout=2)
            except:
                raise RuntimeError(f'Failed to connect to serial port {com_port} for motor {self.__repr__()}.')
            COM_PORTS[com_port] = ser
            return ser

    def _send_instruction(self, inst:bytes, data:bytes) -> None:
        ''' Sends an instruction to the motor. '''
        # send instruction
        self.com_port.write(self.address + inst + data)
    
    def _get_response(self, inst:bytes, data:bytes=b'', require_len:int=None, require_resp_code:bytes=None) -> bytes:
        ''' Get a response from the motor.

        Parameters
        ----------
        inst : bytes
            The instruction to send, should be 2 bytes long.
        data : bytes, optional
            The data to send, if applicable.
        require_len : int, optional
            The length of the response to require. If None, no length check is performed.
        require_resp_code : bytes, optional
            The response code to require. If None, no response code check is performed.

        Returns
        -------
        bytes
            The response from the motor.
        '''
        # send the instruction and get the response
        self._send_instruction(inst, data)
        resp = self.com_port.readall().split(b'\r\n')[-1]
        
        # check that it is for us
        if resp[0] != self.address:
            raise ValueError(f"Got response {resp} that is not for this motor ({self.__repr__()}).")
        
        # check the length
        if require_len is not None:
            assert len(resp) == require_len, f'Response {resp} to instruction {self.address + inst + data} should be {require_len} bytes long.'

        # check response code
        if require_resp_code is not None:
            assert resp[1:3] == require_resp_code, f'Response {resp} to instruction {self.address + inst + data} should start with {require_resp_code}.'
        
        # return the response
        return resp

    def _get_ppmu(self) -> int:
        ''' Contact the motor and get the pulse per measurement unit. '''
        # send instruction asking for info
        self.com_port.write(self.address + b'in')
        # get the last response
        resp = self.com_port.readall().split(b'\r\n')[-1]
        # pulse/m.u. is bytes 25-32
        return int.from_bytes(resp[25:32], 'big')

    def _radians_to_bytes(self, angle_radians:float, num_bytes:int=8) -> bytes:
        ''' Converts an angle in radians to a hexidecimal byte string. '''
        # convert to degrees
        deg = np.rad2deg(angle_radians)
        # convert to pulses
        pulses = deg * self.ppmu
        # convert to hex
        hexPulses = hex(int(pulses))[2:].upper()
        # pad with zeros
        hexPulses = hexPulses.zfill(num_bytes*2)
        # convert to bytes
        return hexPulses.encode('utf-8')

    def _bytes_to_radians(self, angle_bytes:bytes) -> float:
        ''' Converts a hexidecimal byte string to an angle in radians. '''
        # convert to bytes
        pulses = int(angle_bytes, 16)
        # convert to degrees
        deg = pulses / self.ppmu
        # convert to radians
        return np.deg2rad(deg)

    # public methods

    def get_status(self) -> str:
        ''' Retrieve the status of the motor. '''
        # get and check response
        resp = self._get_response(b'gs', require_len=5, require_resp_code=b'gs')
        # return the status
        if resp[3:5] in self.ELLIPTEC_STATUS_CODES:
            return self.ELLIPTEC_STATUS_CODES[resp[3:5]]
        else:
            return 'UNKNOWN STATUS CODE'

class ThorLabsMotor(Motor):
    ''' ThorLabs Motor class.
    
    Parameters
    ----------
    name : str
        The unique name for the motor.
    serial_num : int
        The serial number of the motor.
    '''
    def __init__(self, name:str, serial_num:int):
        # call superclass
        super().__init__(name, 'Elliptec')

        # set attributes
        self.serial_num = serial_num
        self._motor_apt = apt.Motor(serial_num)
    
    def __repr__(self) -> str:
        return f'ThorLabsMotor-{self.name}'

    def rotate_relative(self, angle_radians:float, blocking:bool=True) -> None:
        ''' Rotates the motor by a relative angle.

        Parameters
        ----------
        angle_radians : float
            The angle to rotate by, in radians.
        blocking : bool, optional
            Whether to block until the motor has finished rotating. Default is True.
        '''
        # convert to degrees and send instruction
        angle = np.rad2deg(angle_radians)
        self._motor_apt.move_relative(angle)
        # (maybe) wait for move to finish
        if blocking:
            while self._motor_apt.is_in_motion():
                sleep(0.1)

    def rotate_absolute(self, angle_radians:float, blocking:bool=True) -> None:
        ''' Rotates the motor to an absolute angle.

        Parameters
        ----------
        angle_radians : float
            The angle to rotate by, in radians.
        blocking : bool, optional
            Whether to block until the motor has finished rotating. Default is True.
        '''
        # convert to degrees and send instruction
        angle = np.rad2deg(angle_radians)
        self._motor_apt.move_to(angle)
        # (maybe) wait for move to finish
        if blocking:
            while self._motor_apt.is_in_motion():
                sleep(0.1)

    def home(self, blocking:bool=True) -> None:
        ''' Bring the motor to its home position. 
        
        Parameters
        ----------
        blocking : bool, optional
            Whether to block until the motor has finished rotating. Default is True.
        '''
        # convert to degrees and send instruction
        self._motor_apt.move_home()
        # (maybe) wait for move to finish
        if blocking:
            while self._motor_apt.is_in_motion():
                sleep(0.1)

    def get_position(self) -> float:
        ''' Get the position of the motor.
        
        Returns
        -------
        float
            The position of the motor, in radians.
        '''
        return np.deg2rad(self._motor_apt.position())

UVHWP = ElliptecMotor('UVHWP', 'COM5', b'A')
QP = ElliptecMotor('QP', 'COM5', b'B')
PCC = ElliptecMotor('PCC', 'COM5', b'C')
B_CHWP = ElliptecMotor('B_CHWP', 'COM7', b'A')


