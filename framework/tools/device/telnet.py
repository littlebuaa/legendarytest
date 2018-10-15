import re
import time
import serial
#from misctools import *
import logging
import telnetlib
from framework.tools.config import configget
from framework.tools.utils import colorprint

class TelnetDevice(object):
    def __init__(self, name, host, port):
        self.logger = get_logger()
        self.__name = name
        self.__mac = None
        self.__telnet = telnetlib.Telnet(host,port)

        self.__logfile = None
        self.__backlog = bytes()

        self.__logname = ""
        self.prop = dict()  # Store custom properties
        if not self.__logname:
            self.create_log_file()
        else:
            filename = self.__logname
            self.__logfile = open(filename, "a+b")
            # Flush the backlog
            self.__logfile.write(self.__backlog)
            self.__backlog = None


    def create_log_file(self):
        # Create logger directory, if needed
        log_dirname = './dut_telnet_logs'
        if not os.path.isdir(log_dirname):
            os.makedirs(log_dirname)

        # Create logger file
        date = time.strftime("%Y%m%d_%H%M%S",time.localtime())
        filename = '%s/%s_%s.log' % (log_dirname, self.__name, date)
        self.__logname = filename
        self.__logfile = open(filename, "a+b")

        # Flush the backlog
        self.__logfile.write(self.__backlog)
        self.__backlog = None

    def log(self, stripped_uart_bytes):
        # Strip "\n" to avoid "doubled" carriage returns
        # stripped_uart_bytes = uart_bytes.replace('\n', '')
        # stripped_uart_bytes += "\n"
        if(self.__logfile):
            self.__logfile.write(stripped_uart_bytes.encode())
        else:
            self.__backlog += stripped_uart_bytes.encode()

    def get_name(self):
        return self.__name

    def get_log(self):
        return self.__logname

    def get_mac(self):
        return self.__mac

    def close(self):
        self.__telnet.close()
        if not self.__logfile:
            pass
        elif (not self.__logfile.closed):
                self.__logfile.close()

    def send_command(self, cmd):
        tx_log = "tx>>>" + cmd
        self.log(tx_log)
        self.logger.debug("Dut <%s> TX :" % self.__name)
        self.logger.debug("\t%s" % cmd)
        cmd += '\n'
        self.__telnet.write(cmd.encode('utf-8'))

    def get_result(self,prompt = "\n"):
        text = ""
        rt = -1
        self.logger.debug("Dut <%s> RX :" % self.__name)
        self.logger.debug("-----------------------------")
        text = self.__telnet.read_very_eager().decode('utf-8')
        if text.find(prompt) != -1:
            self.logger.debug("\t-->Return found!")
            rt = 0
        elif len(text) == 0:
            text = "--------None--------\n"
            self.logger.debug("\t-->Nothing Returned")
        self.log(text)
        self.logger.debug("-----------------------------")
        return(rt, text)

    def get_parsed_result(self):
        rt,text = self.get_result()
        res = CommandResult.parse(text)
        return res

    def execute_command(self, cmd, time_out = 0.1):
        self.send_command(cmd)
        time.sleep(time_out)
        rt, text = self.get_result()
        return(rt, text)