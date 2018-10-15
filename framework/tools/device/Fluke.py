import re
import time
import serial
#from misctools import *
import logging
from framework.tools.config import configget
from framework.tools.utils import colorprint
from framework.tools.device import UARTDevice


class Fluke(UARTDevice):
    """Represent a Fluke multimeter, helper functions for configuration and operations."""

    def __init__(self, port):
        super().__init__(port, 115200)
        self.name = "Fluke meter"
        self.open()
        self.logger.info("Fluke meter connexion was successfully opened.")

    def get_voltage(self):
        """Get measured voltage from Fluke."""
        voltage = float(0)
        query = "QM"
        self.send_command(query)
        ttx = self.get_result(1000)
        list_r = ttx.splitlines()
        print(list_r)
        if list_r[0] != '0':
            self.logger.debug("Fluke read value failed")
        else:
            value = list_r[1].split(',')
            if 'VDC' in list_r[1]:
                voltage = float(value[0])
        return voltage

    def get_current(self):
        """Get measured current from Fluke."""
        current = float(0)
        query = "QM"
        self.send_command(query)
        ttx = self.get_result(1000)
        list_r = ttx.splitlines()
        print(list_r)
        if list_r[0] != '0':
            self.logger.debug("Fluke read value failed")
        else:
            value = list_r[1].split(',')
            if 'ADC' in list_r[1]:
                current = float(value[0])*1000
        return current
