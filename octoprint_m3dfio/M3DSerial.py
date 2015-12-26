# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import serial
import serial.tools.list_ports
import traceback
import time

from .gcode import Gcode

class M3DSerial():
    # Feed rate conversion pre-processor settings
    MAX_FEED_RATE_PER_SECOND = 60.0001

    # Constructor
    def __init__(self, comm_instance, port, baudrate, read_timeout, logger=None, *args, **kwargs):
        self._comm_instance = comm_instance
        self._logger = logger
        self._log("M3DSerial.__init__()")
        self._connection = None

        if port is None or port == 'AUTO':
            # no known port, try auto detection
            self._comm_instance._changeState(comm_instance.STATE_DETECT_SERIAL)
            port = self._getPort()
            self._log("Detected printer on {0}".format(port))

        if baudrate == 0:
            # no baudrate, try 115200
            baudrate = 115200
            self._log("Trying baudrate {0}".format(baudrate))

        connection = serial.Serial(str(port), baudrate, timeout=20, writeTimeout=20, parity=serial.PARITY_NONE)

        # Check if not in bootloader mode
        while True:
            connection.write("M115")
            firstByte = connection.read()
            connection.read(connection.inWaiting())
            self._log("  first byte = {0}".format(firstByte))

            if firstByte == "B":
                # Bootloader mode, try to switch to G-code processing mode
                self._log("  switching to G-code processing mode")
                connection.write("Q")
                connection.close()
                time.sleep(1)
                port = self._getPort()
                connection = serial.Serial(str(port), baudrate, timeout=20, writeTimeout=20, parity=serial.PARITY_NONE)
            elif firstByte == "e":
                # G-code processing mode
                self._log("  in G-code processing mode")
                break

        # reopen connection for real
        connection.close()
        time.sleep(1)
        self._connection = serial.Serial(str(port), baudrate, timeout=read_timeout, writeTimeout=10000, parity=serial.PARITY_NONE)

    # Get port
    def _getPort(self):
        # Go through all connected serial ports
        for port in list(serial.tools.list_ports.comports()):
            # Check if port contains the correct VID and PID
            if port[2].upper().startswith("USB VID:PID=03EB:2404"):
                # Return port
                return port[0]

    def _log(self, text):
        self._comm_instance._log(text)
        self._logger.info(text)

    def readline(self, size=None, eol='\n'):
        self._log("M3DSerial.readline(size={0}, eol={1})".format(size, eol))
        try:
            assert(eol == '\n')
            assert(size is None)
            return self._connection.readline()
        except:
            self._log(traceback.format_exc())
            raise

    def write(self, data):
        self._log("M3DSerial.write({0})".format(data))
        if data == "M110\n" or data == "M21\n" or data == "M84\n" :
            data = "M115"

        gcode = Gcode()
        gcode.parseLine(data)
        data = gcode.getBinary()
        self._log("  sending {0}".format(gcode.getAscii()))
        try:
            self._connection.write(data)
        except:
            self._log(traceback.format_exc())
            raise

    def close(self):
        self._log("M3DSerial.close()")
        if self._connection:
            self._connection.close()
            self._connection = None

    @property
    def baudrate(self):
        return self._connection.baudrate()

    @baudrate.setter
    def baudrate(self, rate):
        self._connection.baudrate(rate)

    @property
    def timeout(self):
        return self._connection.timeout()

    @timeout.setter
    def timeout(self, delay):
        self._connection.timeout(delay)

    def __str__(self):
        return "M3DSerial object"
