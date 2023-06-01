# imports 

from re import S
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
        self.com_port = self._get_com_port(com_port) # sets self.com_port to serial port
        self.address = address
        self._get_info() # sets a ton of stuff like model number and such as well as ppmu and travel

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
                s = serial.Serial(com_port, timeout=2)
                COM_PORTS[com_port] = s
                return s
            except:
                raise RuntimeError(f'Failed to connect to serial port {com_port} for motor {self.__repr__()}.')

    def _send_instruction(self, inst:bytes, data:bytes=b'', resp_len:int=None, require_resp_code:bytes=None) -> 'Union[bytes,None]':
        ''' Sends an instruction to the motor and gets a response if applicable.
        
        Parameters
        ----------
        inst : bytes
            The instruction to send, should be 2 bytes long.
        data : bytes, optional
            The data to send, if applicable.
        resp_len : int, optional
            The length of the response to require. If None, no response is expected.
        require_resp_code : bytes, optional
            The response code to require. If None, no response code check is performed.

        Returns
        -------
        bytes or None
            The response from the motor. None if no response is expected.
        '''
        # clear the queue if we want a response
        if resp_len is not None:
            self.com_port.readall()

        # send instruction
        self.com_port.write(self.address + inst + data)

        if resp_len is not None:
            # read the response
            resp = self.com_port.read(resp_len)
            # check response code if applicable
            if require_resp_code is not None:
                if resp[1:3] != require_resp_code.upper():
                    raise RuntimeError(f'Expected response code {require_resp_code.upper()} but got {resp[2:3]}')
            # return the response
            return resp
    
    def _get_info(self) -> int:
        ''' Requests basic info from the motor. '''
        # return (143360/360)
        # get the info
        resp = self._send_instruction(b'in', resp_len=32, require_resp_code=b'in')
        # parse the info
        self.info = dict(
            ELL = int(resp[3:6]),
            SN = int(resp[5:13]),
            YEAR = int(resp[13:17]),
            FWREL = int(resp[17:19]),
            HWREL = int(resp[19:21])
        )
        # get travel and ppmu
        self.travel = int(resp[21:25], 16)
        self.ppmu = int(resp[25:33], 16)
        return None

    def _radians_to_bytes(self, angle_radians:float, num_bytes:int=8) -> bytes:
        ''' Converts an angle in radians to a hexidecimal byte string.

        Parameters
        ----------
        angle_radians : float
            The angle to convert, in radians.
        num_bytes : int, optional
            The number of bytes to return. Default is 8.
        
        Returns
        -------
        '''
        # convert to 0 to 2pi
        angle_radians = angle_radians % (2*np.pi)
        # convert to degrees
        deg = np.rad2deg(angle_radians)
        # convert to pulses, modulo to 
        pulses = int(deg * self.ppmu) % 360
        # convert to hex
        hexPulses = hex(int(pulses))[2:].upper()
        # pad with zeros
        hexPulses = hexPulses.zfill(num_bytes)
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

    def _get_home_offset(self) -> int:
        ''' Get the home offset of the motor.
        
        Returns
        -------
        int
            The home offset of the motor, in pulses.
        '''
        resp = self._send_instruction(b'go', resp_len=11, require_resp_code=b'ho')
        return int(resp[3:11], 16)

    def _set_home_offset(self) -> float:
        ''' Sets the home to be the current position. 
        
        Returns
        -------
        float
            The current position of the motor, in radians (should be zero or close to it).
        '''
        current_offset = self._get_home_offset()
        # get the position exactly
        pos_resp = self._send_instruction(b'gp', resp_len=11, require_resp_code=b'po')
        pos = int(pos_resp[3:11], 16)
        # get the new offset
        new_offset = hex(current_offset + pos)[2:].upper().encode('utf-8')
        # send the new offset
        self._send_instruction(b'so', data=new_offset)
        # check the new position

    # public methods

    def get_status(self) -> str:
        ''' Retrieve the status of the motor. '''
        # get and check response
        resp = self._send_instruction(b'gs', resp_len=5, require_resp_code=b'gs')
        # return the status
        if resp[3:5] in self.ELLIPTEC_STATUS_CODES:
            return self.ELLIPTEC_STATUS_CODES[resp[3:5]]
        else:
            return 'UNKNOWN STATUS CODE'
    
    def home(self) -> None:
        self._send_instruction(b'ho0')

    def rotate_absolute(self, angle_radians:float, blocking:bool=True) -> float:
        ''' Rotate the motor to an absolute position relative to home.

        Parameters
        ----------
        angle_radians : float
            The absolute angle to rotate to, in radians.
        blocking : bool, optional
            Whether to block until the move is complete. Default is True.
        
        Returns
        -------
        float
            The absolute angle in radians that the motor was moved to. Likely will not be the same as the angle requested.
        '''
        # request the move
        resp = self._send_instruction(b'ma', self._radians_to_bytes(angle_radians, num_bytes=8), resp_len=11)
        # block
        if blocking:
            while self.is_active():
                sleep(0.1)

    def rotate_relative(self, angle_radians:float, blocking:bool=True) -> float:
        ''' Rotate the motor to a position relative to the current one.

        Parameters
        ----------
        angle_radians : float
            The angle to rotate, in radians.
        blocking : bool, optional
            Whether to block until the move is complete. Default is True.
        
        Returns
        -------
        float
            The ABSOLUTE angle in radians that the motor was moved to. Likely will not be the same as the angle requested.
        '''
        # request the move
        self._send_instruction(b'mr', self._radians_to_bytes(angle_radians, num_bytes=8))
        # block
        if blocking:
            while self.is_active():
                sleep(0.1)

    def is_active(self) -> bool:
        ''' Check if the motor is active by querying the status. '''
        resp = self._send_instruction(b'i1', resp_len=24, require_resp_code=b'i1')
        return int(resp[4])

    def get_position(self) -> float:
        ''' Get the current position of the motor in radians.
        
        Returns
        -------
        float
            The absolute position of the motor, in radians.
        '''
        # get the position
        resp = self._send_instruction(b'gp', resp_len=11, require_resp_code=b'po')
        # convert to radians
        return self._bytes_to_radians(resp[3:11])

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


