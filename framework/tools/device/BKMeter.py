import re
import time
import serial
import logging
from framework.tools.config import configget
from framework.tools.utils import colorprint
from framework.tools.device import UARTDevice

class BKMeter(UARTDevice):
    """Represent a BK multimeter, helper functions for configuration and operations."""

    def __init__(self, port,baudrate=9600):
        super().__init__(port, baudrate, 0.1)
        self.name = "BK meter"
        self.configure = {
            "50_MA"  : ":disp:enable 1;:func curr:dc;:curr:dc:rang:upp 0.05;:curr:dc:nplc 10",
            "5_MA"   : ":disp:enable 1;:func curr:dc;:curr:dc:rang:upp 0.005;:curr:dc:nplc 10",
            "500_MA" : ":disp:enable 1;:func curr:dc;:curr:dc:rang:upp 0.5;:curr:dc:nplc 10",
            "5_V"    : ":disp:enable 1;:func volt:dc;:volt:dc:rang:upp 5;:volt:dc:nplc 10"
        }
        self.open()
        self.logger.info("BK meter connexion was successfully opened.")

    def set_range(self, range_str):
        """Set BK meter measuring range."""
        self.send_command(self.configure[range_str])
        self.logger.info("BK meter range set to :\t%s", range_str)

    def get_current(self):
        """Get measured current from BK."""
        query = ":fetch?"
        self.send_command(query)
        ttx = self.get_result(1000)
        # pattern return string like":fetch?\r1.2341e-4\n"
        pattern = re.compile(r"(?P<value>[0-9-.]{3,7})e(?P<index>\-?[0-9]?).*")
        match = pattern.search(ttx)
        if match:
            value = match.group('value')
            index = int(match.group('index'))
            if index < 4:
                current = float((value+"e"+"%d")%index)*1e3
                self.logger.info("Value is %.3fmA", current)
                return current
            else:
                current = float((value+"e"+"-%d")%index)*1e6
                self.logger.info("Value is %.3fuA", current)
                return current
        else:
            print([ttx])
            return None

    def get_voltage(self):
        """Get measured voltage from BK."""
        query = ":fetch?"
        self.send_command(query)
        ttx = self.get_result(1000)
        # return string like":fetch?\r1.2341e-4\n"
        pattern = re.compile(r'(?P<value>[0-9-.]{3,7})e(?P<index>\-?[0-9]?).*')
        match = pattern.search(ttx)
        if match:
            value = match.group('value')
            index = int(match.group('index'))
            voltage = float((value+"e"+"%d")%index)
            self.logger.info("Value is %.3fV", voltage)
            return voltage
        else:
            print([ttx])
            return None
