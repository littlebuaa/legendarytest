import re
import time
import serial
#from misctools import *
import logging
from framework.tools.config import configget
from framework.tools.utils import colorprint
from framework.tools.device import UARTDevice
import os


class Zoovstation(UARTDevice):
    """Device under test, i.e. the product to be tested."""
    def __init__(self, port, serial_id="XXXX",baudrate=115200):
        super().__init__(port, baudrate, 0.1)
        station_name = configget("TEST_STATION", "station_name").lower()
        self.name = station_name
        self.__logfile = None
        self.__backlog = bytes()
        self.__pass = None # Pass/Fail status (tristate: None, True, False)
        self.__failure_reason = None # Reason of failure if __pass = False
        self.__logname = ""
        self.__test = True
        self.serial_id = serial_id

    def create_log_file(self, station_number):
        """Create and open a log file."""
        # Create logger directory, if needed
        log_dirname = './' + configget("TEST_STATION", "LOCAL_LOG") + os.sep + "serial_log"
        if not os.path.isdir(log_dirname):
            os.makedirs(log_dirname)

        # Create logger file
        date = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        filename = '%s/%s_%s_%s.log' % (log_dirname, self.name, station_number, date)
        self.__logname = filename
        self.__logfile = open(filename, "a+b")

        # Flush the backlog
        self.__logfile.write(self.__backlog)
        self.__backlog = None

    def log(self, uart_bytes):
        """Log data."""
        # Strip "\n" to avoid "doubled" carriage returns
        stripped_uart_bytes = uart_bytes.replace('\n', '')
        if self.__logfile:
            self.__logfile.write(stripped_uart_bytes.encode())
        else:
            self.__backlog += stripped_uart_bytes.encode()

    def get_name(self):
        """Return device name."""
        return self.name

    def get_log(self):
        """Return device log file name."""
        return self.__logname

    def get_uart(self):
        """Return device UART connexion."""
        return self.uart

    def get_shell(self,prompt,timeout=20000):
        self.uart.flushInput()
        self.send_command("")
        shell = self.get_result(timeout,prompt)
        if shell[0] >= 0:
            return (True,shell[1])
        else:
            return (False,shell[1])

    def zoov_login(self,timeout_ms = 12000):
        station_name = configget("TEST_STATION", "station_name").lower()
        station_version = configget("TEST_STATION", "station_version").lower()
        
        time_start = time.time()
        self.uart.flushInput()
        while True:
            msg_returned = self.get_shell(self.name,2000)
            if msg_returned[0]:
                return True
            if "test-station login" in msg_returned[1]:
                self.send_command("teststation")
                probe_result, text = self.get_result(4000,"Password")
                self.send_command("test")
                probe_result, text = self.get_result(4000,"station name")
            elif "station name" in msg_returned[1]:
                self.logger.info("======>>>>>>>>>>>>>> Login with station information")

            self.send_command("zoov01-%s"%station_name)
            time.sleep(0.5)
            self.send_command(station_version)
            probe_result, text = self.get_result(6000,station_name)
            if probe_result >=0:
                return True
            elapsed_time = (time.time() - time_start) * 1000
            if elapsed_time > timeout_ms:
                self.logger.warn("-->timeout: %d ms", elapsed_time)
                colorprint("cmd timeout", "RED")
                return False
            
    def open(self):
        # Open UART
        super(Zoovstation, self).open()
        self.uart.flushInput()
        station_number = configget("TEST_STATION", "station_number").lower()
        
        # need login with "test station"
        if not self.zoov_login():
            return False
        # Open logfile
        if not self.__logname:
            self.create_log_file(station_number)
        else:
            filename = self.__logname
            self.__logfile = open(filename, "a+b")
            # Flush the backlog
            self.__logfile.write(self.__backlog)
            self.__backlog = None
        return True

    def close(self):
        super(Zoovstation, self).close()
        if not self.__logfile:
            pass
        elif not self.__logfile.closed:
            self.__logfile.close()

    def send_command(self, cmd):
        self.logger.debug("<%s> TX command sent: \t<%s>"%(self.name,cmd))
        self.uart.flushInput()
        self.uart.flushOutput()
        # Workaround : the byte should be sent slowly...
        #self.__uart.write("%s\r" % cmd)
        if len(cmd) > 0:
            for byte in cmd + '\r':
                self.uart.write(byte.encode())
                time.sleep(0.001)
        else:
            eol = "\r"
            self.uart.write(eol.encode())
            time.sleep(0.001)

    def get_result(self, timeout_ms, prompt="shell>",displayRX = True):
        ''' This function returns the status and result of UART after sending the cmd
            rt =  0: good
            rt =  1: shell found, but rc is not 0
            rt = -1: time_out
            text: all the content
        '''
        text = ""
        text_pos = 0
        return_value = -1
        time_start = time.time()
        self.logger.debug("--------------- %s RX start ---------------", self.name)
        while True:
            chunk = self.uart.read(512)
            elapsed_time = (time.time() - time_start) * 1000
            # Do we need to decode/encode !?
            # Replace non-ascii characters with '?' because we sometimes receive - because of a bad uart connection ? -
            # non-ascii characters from the DUT
            text += chunk.decode('ascii', 'replace')
            #### Display board RX in logs, in "realtime"
            if displayRX:
                while True:
                    cr_pos = text.find("\r", text_pos)
                    if cr_pos == -1:
                        break
                    stripped = text[text_pos:cr_pos].strip('\r\n')
                    if len(stripped) > 0:
                        self.logger.debug("  %s", stripped)
                    text_pos = cr_pos + 1

            ### Return on shell prompt, or timeout
            if text.find(prompt) != -1:
                return_value = 1 if text.find('rc=0') == -1 else 0
                break
            if elapsed_time > timeout_ms:
                self.logger.warn("-->timeout: %d ms", elapsed_time)
                colorprint("cmd timeout", "RED")
                break

        self.log(text)
        ## Flush Display RX in logs
        if displayRX:
            stripped = text[text_pos:].strip('\r\n')
            if len(stripped) > 0:
                self.logger.debug("  %s", stripped)
        if return_value == 0:
            resume = "==>> prompt found, and rc=0"
        elif return_value == 1:
            resume = "==>> prompt found, but no 'rc=0'"
        else:
            resume = None
        self.logger.debug(resume)
        self.logger.debug("--------------- %s RX end ---------------", self.name)
        return(return_value, text)

    def get_parsed_result(self, timeout_ms=10000):
        """Get result and parse, returning the parsed result."""
        return_value, text = self.get_result(timeout_ms)
        res = CommandResult.parse(text)
        return res

    def receive_command(self, timeout_ms=10000, ignore_rc=False):
        res = None
        temp = self.get_result(timeout_ms)
        res = CommandResult.parse(temp[1])
        if (not ignore_rc) and (res.rc != 0):
            raise ValueError("cmd failed, rc=%d" % res.rc)
        return res

    def execute_command(self, cmd, timeout_ms=10000):
        prompt = self.name
        self.send_command(cmd)
        rc, text = self.get_result(timeout_ms,prompt)
        return(rc, text)

class CommandResult(object):
    def __init__(self, rc, data):
        '''rc : (int) cmd return code
           data : (dict) key = value result'''
        if not isinstance(rc, int):
            raise ValueError('rc is not a int')
        if not isinstance(data, dict):
            raise ValueError('data is not a dict')
        self.rc = rc
        self.data = data

    @staticmethod
    def parse(string, separator='='):
        """Parse command results with shape 'xxx = yyy' in a dict."""
        return_code = -1
        data = dict()
        lines = string.splitlines()
        for line in lines:
            keyval = line.split(separator, 1)
            if len(keyval) == 2:
                data[keyval[0].strip()] = keyval[1].strip()

        # Parse cmd "rc=xxx"
        if 'rc' in data:
            return_code = int(data['rc'])
            del data['rc']

        #logger.debug("rc=%s" % rc)
        return CommandResult(return_code, data)
