import serial as ser
import functools as ft
import numpy as np
import time
import abc
from . import config


class BaseCcuController(abc.ABC):
    """
    Not-that-abstract abstract class providing a basic controller
    interface for serial-based CCUs.

    :param port: serial port (e.g. 'COM1' on windows, or
        '/dev/ttyUSB1' on unix)
    :param baud: serial communication baud rate (19200 for the Altera
        DE2 FPGA CCU, as found from scraping the
    """

    UPDATE_PERIOD = 0.1

    def __init__(self,
                 port=config.DEFAULTS['port'],
                 baud=config.DEFAULTS['baud']):

        self.port = port
        self.baud = baud

    @abc.abstractmethod
    def __next__(self):
        pass

    def flush(self):
        pass

    def clean(self):
        pass

    def read(self, size=1):
        self.flush()
        self.clean()
        return np.row_stack(next(self) for _ in range(size))

    def __enter__(self):
        return self

    def __iter__(self):
        return self

    def __exit__(self, e_type=None, e_value=None, e_traceback=None):
        pass

    def close(self):
        self.__exit__()


class DummyCcuController(BaseCcuController):
    """
    Dummy controller class to help with code debugging and testing.
    """

    def __next__(self):
        time.sleep(self.UPDATE_PERIOD)
        return np.random.randint(0, 256, size=8)


class FpgaCcuController(BaseCcuController):
    """
    Main controller for the Altera DE2 FPGA CCU.
    """

    TERMINATION = 0xff

    def __init__(self,
                 port=config.DEFAULTS['port'],
                 baud=config.DEFAULTS['baud']):
        super().__init__(port=port, baud=baud)

        self.connection = ser.Serial(self.port, self.baud)

    def __next__(self):
        return self.read_packet()

    def read_packet(self):
        """
        Reads a single "packet" of data, containing counts from each
        of the 8 counter channels over one update period (0.1 sec).

        Each packet comprises 41 bytes.  The bytes are "partitioned"
        into 8 chunks of 5 bytes each, one for each counter, with the
        last byte reserved for a termination byte (``0xff``, or
        ``0b11111111``) marking the end of the data packet::

            [5 bytes encoding counter 0]
            [5 bytes encoding counter 1]
            [5 bytes encoding counter 2]
            [5 bytes encoding counter 3]
            [5 bytes encoding counter 4]
            [5 bytes encoding counter 5]
            [5 bytes encoding counter 6]
            [5 bytes encoding counter 7]
            [1 termination byte]

        For each counter, the 5 bytes encode some sort of a multi-byte
        unsigned integer, little-endian (i.e. least-significant byte
        first).  To avoid clashing with termination bytes, only the
        first 7 bits of each byte are used (the 8th bit is always a
        ``0``).  Thus, in total, there are up to 35 bits for storing
        each counter value (the original manual claims each counter to
        be encoded as a 32-bit number; not sure how that works).  For
        example, the counter value ``4321``, with binary
        representation ``0b1000011100001``, would be sent as::

            01100001 00100001 00000000 00000000 00000000

        The first byte contains the first (i.e. least significant) 7
        bits, padded on the left by a delimiting ``0`` bit.  The next
        byte contains the next 7 bits, and so on.  Thus the byte-wise
        encoding of each counter value forms a base-128
        representation, such that, if the bytes were denoted ``b_0``,
        ``b_1``, ..., ``b_4``, the counter value would be found as::

            b_0 + b_1 * 128 + b_2 * 128^2 + b_3 * 128^3 + b_4 * 128^4.

        An example representation of a data packet containing counter
        values [2718, 281828, 4, 59045, 235, 360, 2874, 71352] is
        (first row highlights delimiter ``0`` bit columns as ``0`` and
        actual data bits as ``x``)::

            0xxxxxxx 0xxxxxxx 0xxxxxxx 0xxxxxxx 0xxxxxxx
            -------- -------- -------- -------- --------
            00011110 00010101 00000000 00000000 00000000
            01100100 00011001 00010001 00000000 00000000
            00000100 00000000 00000000 00000000 00000000
            00100101 01001101 00000011 00000000 00000000
            01101011 00000001 00000000 00000000 00000000
            01101000 00000010 00000000 00000000 00000000
            00111010 00010110 00000000 00000000 00000000
            00111000 00101101 00000100 00000000 00000000 11111111
        """

        buffer = np.zeros(8)

        # read 8-counter measurements
        for i in range(8):
            packet = self.connection.read(size=5)

            # each byte should be 8 bits, but somehow bitshifting by 7
            # gives us more "correct" agreement with the original
            # LabVIEW interface provided by the Altera DE2 designers.
            # The original designers also bitshift by 7, not 8, in the
            # LabVIEW code.
            buffer[i] = ft.reduce(lambda v, b: (v << 7) + b,
                                  reversed(packet))

        # skip termination character
        assert self.connection.read()[0] == self.TERMINATION, \
            'misplaced termination character'

        return buffer

    def flush(self):
        """
        Resets the connection by "flushing" any buffers, clearing up
        any data accumulated in the buffers and thereby allowing new,
        live data to be collected.
        """

        self.connection.reset_input_buffer()

        # skip leftover data, in case the buffer is flushed mid-read,
        # until next termination
        while self.connection.read()[0] != self.TERMINATION:
            pass

    def __exit__(self, e_type=None, e_value=None, e_traceback=None):
        self.close()

    def close(self):
        self.connection.close()
