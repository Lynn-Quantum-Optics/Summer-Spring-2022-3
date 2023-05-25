from enum import Enum


class RecordType(Enum):
    Error = 0,
    Warning = 1,
    Message = 2,
    Action = 3,
    Call = 4,
    Detail = 5,
    Return = 6


class ElliptecStatus(Enum):
    OK = 0
    COMMUNICATION_TIMEOUT = 1
    MECHANICAL_TIMEOUT = 2
    COMMAND_ERROR = 3
    VALUE_OUT_OF_RANGE = 4
    MODULE_ISOLATED = 5
    MODULE_OUT_OF_ISOLATION = 6
    INITIALIZING_ERROR = 7
    THERMAL_ERROR = 8
    BUSY = 9
    SENSOR_ERROR = 10
    MOTOR_ERROR = 11
    OUT_OF_RANGE = 12
    OVER_CURRENT_ERROR = 13


class Experiment(Enum):
    FULL_TOMOGRAPHY = 0
    PURITY = 1
    STEERING_MEASUREMENT = 2
    HV_BASIS = 3
    CIRCULAR = 4
    BELL = 5
    DIAGONAL_SMILEYFACE = 6
    ANTIDIAGONAL_SAILBOAT = 7
    CUSTOM = 8
