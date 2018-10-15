import re
import time
import serial
#from misctools import *
import logging
from framework.tools.config import configget
from framework.tools.utils import colorprint
from framework.tools.device import UARTDevice
import os


class DUT(UARTDevice):
    """Device under test, i.e. the product to be tested."""
    def __init__(self, name, port, mac_label = "",baudrate=1000000):
        super().__init__(port, baudrate, 0.1)
        self.name = name
        self.__mac = None
        self.__logfile = None
        self.__backlog = bytes()
        self.__pass = None # Pass/Fail status (tristate: None, True, False)
        self.__failure_reason = None # Reason of failure if __pass = False
        self.__logname = ""
        self.__test = True
        mac_label = mac_label.replace(":","").lower()
        self.prop = {"mac_label": mac_label}  # Store custom properties


    def create_log_file(self, mac):
        """Create and open a log file."""
        # Create logger directory, if needed
        log_dirname = './' + configget("TEST_STATION", "LOCAL_LOG") + os.sep + "serial_log"
        if not os.path.isdir(log_dirname):
            os.makedirs(log_dirname)

        # Create logger file
        date = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        filename = '%s/%s_%s_%s.log' % (log_dirname, mac, date, self.name)
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

    def get_mac(self):
        """Return device MAC."""
        return self.__mac

    def get_shell(self, timeout=20000):
        self.uart.flushInput()
        self.send_command("")
        shell = self.get_result(timeout)
        if shell[0] >= 0:
            self.logger.info("Shell>> Found!!")
            return True
        else:
            self.logger.info("Shell not found, Sommething wrong with the UART connection!!")
            return False

    def open(self):
        # Open UART
        super(DUT, self).open()
        self.uart.flushInput()

        if self.uart.baudrate == 1000000:
            # Serial Device Withings, Get DUT MAC address
            if not self.get_shell():
                return False
            # get probe info
            self.send_command("probe")
            probe_result = self.get_parsed_result(1000)

            if probe_result.rc != 0:
                self.logger.warn("Probing <%s> failed, rc=%d !", self.name, probe_result.rc)
                self.__test = False
                return False
            self.prop.update(probe_result.data)
            # Set mac attribute
            self.__mac = self.prop["mac"]

            # Open logfile
            if not self.__logname:
                self.create_log_file(self.__mac.replace(":", ""))
            else:
                filename = self.__logname
                self.__logfile = open(filename, "a+b")
                # Flush the backlog
                self.__logfile.write(self.__backlog)
                self.__backlog = None
            return True
        elif self.uart.baudrate == 115200:
            # other device, like Raspberry Pi
            self.send_command("\r")
            time.sleep(0.1)
            probe_result, text = self.get_result(1000, "pi@raspberrypi")
            if "pi@raspberrypi" in text:
                return True
            elif "raspberrypi login" in text:
                self.send_command("pi")
                time.sleep(0.1)
                probe_result, text = self.get_result(2000, "Password")
                self.send_command("pi")
                time.sleep(0.1)
                probe_result, text = self.get_result(4000, "pi@raspberrypi")
                if "pi@raspberrypi" in text:
                    return True
                else:
                    return False

    def close(self):
        super(DUT, self).close()
        if not self.__logfile:
            pass
        elif not self.__logfile.closed:
            self.__logfile.close()

    def send_command(self, cmd):
        self.logger.debug("Dut <%s> TX send command: \t<%s>"%(self.name,cmd))
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
                self.logger.debug("-->prompt found")
                if text.find('rc=0') == -1:
                    return_value = 1
                    self.logger.debug("-->rc=0 NOT FOUND!!")
                else:
                    return_value = 0
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

    def execute_command(self, cmd, timeout_ms=10000,prompt="shell>"):
        self.send_command(cmd)
        rc, text = self.get_result(timeout_ms,prompt)
        return(rc, text)

    def execute_command_magicpy(self,cmd,timeout_ms=10000,prompt = ">>>"):
        rc, text = self.execute_command(cmd,timeout_ms,prompt)
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
