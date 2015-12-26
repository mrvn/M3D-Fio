# coding=utf-8
from __future__ import absolute_import

from .M3DFioPlugin import M3DFioPlugin

# Plugin details
__author__ = "donovan6000 <donovan6000@exploitkings.com>"
__license__ = "GNU General Public License http://www.gnu.org/licenses/gpl.txt"
__copyright__ = "Copyright (C) 2015 Exploit Kings. All rights reserved."
__plugin_name__ = "M3D-Fio"


def __plugin_load__():
    print("M3D __plugin_load__()")
    global __plugin_implementation__
    __plugin_implementation__ = M3DFioPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
	    "octoprint.comm.transport.serial.factory": __plugin_implementation__.serial_factory,
	    "octoprint.comm.protocol.gcode.queuing": __plugin_implementation__.queuing,
	    }
