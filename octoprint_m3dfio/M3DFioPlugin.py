# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import traceback

from .M3DSerial import M3DSerial

class M3DFioPlugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.ShutdownPlugin,
    ):

    # Rom decryption and encryption tables
    ROM_DECRYPTION_TABLE = [0x26, 0xE2, 0x63, 0xAC, 0x27, 0xDE, 0x0D, 0x94, 0x79, 0xAB, 0x29, 0x87, 0x14, 0x95, 0x1F, 0xAE, 0x5F, 0xED, 0x47, 0xCE, 0x60, 0xBC, 0x11, 0xC3, 0x42, 0xE3, 0x03, 0x8E, 0x6D, 0x9D, 0x6E, 0xF2, 0x4D, 0x84, 0x25, 0xFF, 0x40, 0xC0, 0x44, 0xFD, 0x0F, 0x9B, 0x67, 0x90, 0x16, 0xB4, 0x07, 0x80, 0x39, 0xFB, 0x1D, 0xF9, 0x5A, 0xCA, 0x57, 0xA9, 0x5E, 0xEF, 0x6B, 0xB6, 0x2F, 0x83, 0x65, 0x8A, 0x13, 0xF5, 0x3C, 0xDC, 0x37, 0xD3, 0x0A, 0xF4, 0x77, 0xF3, 0x20, 0xE8, 0x73, 0xDB, 0x7B, 0xBB, 0x0B, 0xFA, 0x64, 0x8F, 0x08, 0xA3, 0x7D, 0xEB, 0x5C, 0x9C, 0x3E, 0x8C, 0x30, 0xB0, 0x7F, 0xBE, 0x2A, 0xD0, 0x68, 0xA2, 0x22, 0xF7, 0x1C, 0xC2, 0x17, 0xCD, 0x78, 0xC7, 0x21, 0x9E, 0x70, 0x99, 0x1A, 0xF8, 0x58, 0xEA, 0x36, 0xB1, 0x69, 0xC9, 0x04, 0xEE, 0x3B, 0xD6, 0x34, 0xFE, 0x55, 0xE7, 0x1B, 0xA6, 0x4A, 0x9A, 0x54, 0xE6, 0x51, 0xA0, 0x4E, 0xCF, 0x32, 0x88, 0x48, 0xA4, 0x33, 0xA5, 0x5B, 0xB9, 0x62, 0xD4, 0x6F, 0x98, 0x6C, 0xE1, 0x53, 0xCB, 0x46, 0xDD, 0x01, 0xE5, 0x7A, 0x86, 0x75, 0xDF, 0x31, 0xD2, 0x02, 0x97, 0x66, 0xE4, 0x38, 0xEC, 0x12, 0xB7, 0x00, 0x93, 0x15, 0x8B, 0x6A, 0xC5, 0x71, 0x92, 0x45, 0xA1, 0x59, 0xF0, 0x06, 0xA8, 0x5D, 0x82, 0x2C, 0xC4, 0x43, 0xCC, 0x2D, 0xD5, 0x35, 0xD7, 0x3D, 0xB2, 0x74, 0xB3, 0x09, 0xC6, 0x7C, 0xBF, 0x2E, 0xB8, 0x28, 0x9F, 0x41, 0xBA, 0x10, 0xAF, 0x0C, 0xFC, 0x23, 0xD9, 0x49, 0xF6, 0x7E, 0x8D, 0x18, 0x96, 0x56, 0xD1, 0x2B, 0xAD, 0x4B, 0xC1, 0x4F, 0xC8, 0x3A, 0xF1, 0x1E, 0xBD, 0x4C, 0xDA, 0x50, 0xA7, 0x52, 0xE9, 0x76, 0xD8, 0x19, 0x91, 0x72, 0x85, 0x3F, 0x81, 0x61, 0xAA, 0x05, 0x89, 0x0E, 0xB5, 0x24, 0xE0]

    ROM_ENCRYPTION_TABLE = [0xAC, 0x9C, 0xA4, 0x1A, 0x78, 0xFA, 0xB8, 0x2E, 0x54, 0xC8, 0x46, 0x50, 0xD4, 0x06, 0xFC, 0x28, 0xD2, 0x16, 0xAA, 0x40, 0x0C, 0xAE, 0x2C, 0x68, 0xDC, 0xF2, 0x70, 0x80, 0x66, 0x32, 0xE8, 0x0E, 0x4A, 0x6C, 0x64, 0xD6, 0xFE, 0x22, 0x00, 0x04, 0xCE, 0x0A, 0x60, 0xE0, 0xBC, 0xC0, 0xCC, 0x3C, 0x5C, 0xA2, 0x8A, 0x8E, 0x7C, 0xC2, 0x74, 0x44, 0xA8, 0x30, 0xE6, 0x7A, 0x42, 0xC4, 0x5A, 0xF6, 0x24, 0xD0, 0x18, 0xBE, 0x26, 0xB4, 0x9A, 0x12, 0x8C, 0xD8, 0x82, 0xE2, 0xEA, 0x20, 0x88, 0xE4, 0xEC, 0x86, 0xEE, 0x98, 0x84, 0x7E, 0xDE, 0x36, 0x72, 0xB6, 0x34, 0x90, 0x58, 0xBA, 0x38, 0x10, 0x14, 0xF8, 0x92, 0x02, 0x52, 0x3E, 0xA6, 0x2A, 0x62, 0x76, 0xB0, 0x3A, 0x96, 0x1C, 0x1E, 0x94, 0x6E, 0xB2, 0xF4, 0x4C, 0xC6, 0xA0, 0xF0, 0x48, 0x6A, 0x08, 0x9E, 0x4E, 0xCA, 0x56, 0xDA, 0x5E, 0x2F, 0xF7, 0xBB, 0x3D, 0x21, 0xF5, 0x9F, 0x0B, 0x8B, 0xFB, 0x3F, 0xAF, 0x5B, 0xDB, 0x1B, 0x53, 0x2B, 0xF3, 0xB3, 0xAD, 0x07, 0x0D, 0xDD, 0xA5, 0x95, 0x6F, 0x83, 0x29, 0x59, 0x1D, 0x6D, 0xCF, 0x87, 0xB5, 0x63, 0x55, 0x8D, 0x8F, 0x81, 0xED, 0xB9, 0x37, 0xF9, 0x09, 0x03, 0xE1, 0x0F, 0xD3, 0x5D, 0x75, 0xC5, 0xC7, 0x2D, 0xFD, 0x3B, 0xAB, 0xCD, 0x91, 0xD1, 0x4F, 0x15, 0xE9, 0x5F, 0xCB, 0x25, 0xE3, 0x67, 0x17, 0xBD, 0xB1, 0xC9, 0x6B, 0xE5, 0x77, 0x35, 0x99, 0xBF, 0x69, 0x13, 0x89, 0x61, 0xDF, 0xA3, 0x45, 0x93, 0xC1, 0x7B, 0xC3, 0xF1, 0xD7, 0xEB, 0x4D, 0x43, 0x9B, 0x05, 0xA1, 0xFF, 0x97, 0x01, 0x19, 0xA7, 0x9D, 0x85, 0x7F, 0x4B, 0xEF, 0x73, 0x57, 0xA9, 0x11, 0x79, 0x39, 0xB7, 0xE7, 0x1F, 0x49, 0x47, 0x41, 0xD9, 0x65, 0x71, 0x33, 0x51, 0x31, 0xD5, 0x27, 0x7D, 0x23]
		
    # Bed dimensions
    BED_LOW_MAX_X = 113.0
    BED_LOW_MIN_X = 0.0
    BED_LOW_MAX_Y = 107.0
    BED_LOW_MIN_Y = 0.0
    BED_LOW_MAX_Z = 5.0
    BED_LOW_MIN_Z = 0.0
    BED_MEDIUM_MAX_X = 110.2
    BED_MEDIUM_MIN_X = 2.8
    BED_MEDIUM_MAX_Y = 107.0
    BED_MEDIUM_MIN_Y = -6.6
    BED_MEDIUM_MAX_Z = 73.5
    BED_MEDIUM_MIN_Z = BED_LOW_MAX_Z
    BED_HIGH_MAX_X = 82.0
    BED_HIGH_MIN_X = 2.35
    BED_HIGH_MAX_Y = 92.95
    BED_HIGH_MIN_Y = 20.05
    BED_HIGH_MAX_Z = 112.0
    BED_HIGH_MIN_Z = BED_MEDIUM_MAX_Z
		
    # Chip details
    CHIP_NAME = "ATxmega32C4"
    CHIP_PAGE_SIZE = 0x80
    CHIP_NRWW_SIZE = 0x20
    CHIP_NUMBER_OF_PAGES = 0x80
    CHIP_TOTAL_MEMORY = CHIP_NUMBER_OF_PAGES * CHIP_PAGE_SIZE * 2

    # Constructor
    def __init_(self):
        pass

    def on_after_startup(self):
        self._logger.info("on_after_startup()")

    def on_shutdown(self):
        self._logger.info("on_shutdown()")

    def serial_factory(self, comm_instance, port, baudrate, read_timeout, *args, **kwargs):
        self._logger.info("serial_factory()")
        try:
            return M3DSerial(comm_instance, port, baudrate, read_timeout, *args, logger=self._logger, **kwargs)
        except:
            self._logger.error(traceback.format_exc())
            comm_instance._log("Failed to create serial object:")
            comm_instance._log(traceback.format_exc())
            comm_instance._errorValue = 'Failed to create serial object.'
            comm_instance._changeState(comm_instance.STATE_ERROR)
            eventManager().fire(Events.ERROR, {"error": comm_instance.getErrorString()})
            return None

    def queuing(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
        self._logger.info("queuing: {0} (gcode = {1})".format(cmd, gcode))
        comm_instance._log("queuing: {0} (gcode = {1})".format(cmd, gcode))
        if cmd == "G1 X1.0000 F1946":
            comm_instance._log("  zig-zag")
            return [
                ("G1 Y10.0000 F1946", None),
                ("G1 Y-10.0000 F1946", None),
                ("G1 X1.0000 F1946", None),
                ]
        else:
            return [(cmd, cmd_type)]
