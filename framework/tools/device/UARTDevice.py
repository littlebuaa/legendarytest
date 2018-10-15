import re
import time
import serial
#from misctools import *
import logging
from framework.tools.config import configget
from framework.tools.utils import colorprint

class UARTDevice(object):
    """Generic representation of a UART device."""

    def __init__(self, port, baudrate=115200, timeout=0.5, parity="N", stopbits=1):
        self.logger = logging.getLogger()
        self.name = "UART"
        self.port = port
        self.uart = serial.Serial(self.port)
        self.uart.baudrate = baudrate
        self.uart.parity = parity
        self.uart.stopbits = stopbits
        self.uart.timeout = timeout
        if self.uart.isOpen():
            self.uart.close()
        self.uart.open()

    def open(self):
        """Open UART connexion to device."""
        if self.uart.isOpen():
            self.close()
        self.uart.open()
        self.logger.info("%s connexion on port %s was successfully opened.", self.name, self.port)

    def close(self):
        """Close UART connexion."""
        if self.uart.isOpen():
            self.uart.close()
        self.logger.info("%s connexion on port %s was successfully closed.", self.name, self.port)

    def send_command(self, cmd):
        """Send a command to the UART device."""
        self.logger.debug("Sending command to %s:\t%s", self.name, cmd)
        self.uart.flushInput()
        self.uart.flushOutput()
        if len(cmd) > 0:
            for byte in cmd + '\r':
                self.uart.write(byte.encode())
                time.sleep(0.001)
        else:
            eol = "\r"
            self.uart.write(eol.encode())
            time.sleep(0.001)

    def get_result(self, timeout_ms):
        """Get result from a command sent to the UART device."""
        text = ""
        start_time = time.time()
        self.logger.debug("--------------- %s RX start ---------------", self.name)
        while True:
            chunk = self.uart.read(512)
            elapsed_time = (time.time() - start_time) * 1000
            text += chunk.decode('ascii', 'replace')
            if (elapsed_time > timeout_ms) or len(chunk) == 0:
                self.logger.debug("Finish reading")
                self.logger.debug(text)
                break
        self.logger.debug("--------------- %s RX end ---------------", self.name)
        return text