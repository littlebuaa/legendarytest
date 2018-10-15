import re
import time
import logging
import telnetlib
from framework.tools.config import configget
from framework.tools.utils import colorprint
from framework.tools.device import TelnetDevice


class Freq_Meter(TelnetDevice):
    def __init__(self,host, port):
        super.__init__("Frequency Meter",host, port)
        self.logger = get_logger()
        self.__name = super().get_name()
        self.logger.info("-----  %s  Created -----"%self.__name)
        #Frequency Counter
        DEFAULT_PORT_NUMBER_FREQUENCY_COUNTER_TELNET = "5042"
        REST_DELAY_TO_ALLOW_FREQUENCY_COUNTER_TO_RESPOND = 0.1
        self.TRIG_COUNT = 50
        self.SAMPLE_COUNT = 1
        self.gateTimeParameter = 0.1
        #Frequency Counter commands list
        self.askId = "*idn?"
        self.resetFrequencyCounter = "*RST"
        self.clearEventregister = "*CLS" #Clear event registers and error queue.
        self.clearServiceRequest = "*SRE 0"  #Clear service request enable register.
        self.clearEventStatus = "*ESE 0" #Clear event status enable register.
        self.preSetStatus = "STATus:PRESet" #Read preset status

        self.setChannel = "CONF:FREQ 20E3, (@1)" #// Configures for frequency measurement at Ch-1.
        self.trigCount = "TRIG:COUN "+str(self.TRIG_COUNT)   #// Configure Trigger Count to TRIG_COUNT
        self.sampleCount = "SAMP:COUN "+str(self.SAMPLE_COUNT)   #// Configure Sample Count to SAMPLE_COUNT
        self.gateSource = "SENS:FREQ:GATE:SOUR TIME" #// Configures Gate Source to TIME.
        self.gateTime = "SENS:FREQ:GATE:TIME "+str(self.gateTimeParameter) #// Configures Gate Time to 0.001 for mhz resolution

        self.smoothingDisable = "CALC:SMO:STAT OFF" #// No smoothing
        self.scaling = "CALC:SCAL:FUNC SCAL" #// Scaling Mx-B activated
        self.gainScale = "CALC:SCAL:GAIN 2.0" #// gain du scale à 2
        self.offsetScale = "CALC:SCAL:OFFS 0.0" #// offset du scale à 0
        self.enableScaling = "CALC:SCAL:STAT ON" #// enable scaling
        self.calculAverage = "CALC:AVER:STAT ON" #// calculer l'average
        self.enableCalcul = "CALC:STAT ON" #// Enable Calculate1 subsystem.

        self.preMeasurement = "INIT" #// lance les mesures
        self.readMeasurement = "CALC:AVER:ALL?" #// read de la mesure d'average

    def execute_command_ack(self, cmd):
        #errorCheckStatement="SYST:ERR?"
        self.execute_command(cmd)
        self.logger.debug("Request of stauts checking!")
        rt, text2 = self.execute_command("SYST:ERR?",0.5)
        if (text2.find("No error"))!=-1:
            flag = True
            msg = "\t%s => Done & Good!"%cmd
        else:
            flag = False
            msg = text2
        self.logger.info(msg)
        return flag

    def init_meter(self):
        flag = True
        # PRESet process,
        self.logger.info("Reset the meter, clear the status!")
        self.execute_command(self.resetFrequencyCounter,0.2)
        self.execute_command(self.askId)
        command_reset = [
            self.clearEventregister,
            self.clearServiceRequest,
            self.clearEventStatus,
        ]
        for cmd in command_reset:
            flag = self.execute_command_ack(cmd)
            if not flag:
                return False
        return flag

    def set_measurement(self):
        flag = True
        # Measurement config, channel, scale, sample_nb, etc
        self.logger.info("Set the configuration, channel, scale, triger, average, etc!")
        command_config = [
            self.setChannel,
            self.trigCount,
            self.sampleCount,
            self.gateSource,
            self.gateTime,
            self.smoothingDisable,
            self.scaling,
            self.gainScale,
            self.offsetScale,
            self.enableScaling,
            self.calculAverage,
            self.enableCalcul,
        ]

        for cmd in command_config:
            flag = self.execute_command_ack(cmd)
            if not flag:
                return False
        return True

    def init_measurement(self):
        self.init_meter()
        res = self.set_measurement()
        return res

    def save_as_default_state(self):

        sav_dat = "*SAV 1"
        select_as_def = "MEM:STAT:REC:SEL 1"
        set_auto_recall = "MEM:STAT:REC:AUTO ON"
        rt = self.execute_command_ack(sav_dat)
        rt = self.execute_command_ack(select_as_def)
        rt = self.execute_command_ack(set_auto_recall)

    def read_value(self):
        # send init to frequency meter
        self.execute_command(self.preMeasurement)
        time.sleep(0.5)
        rt, res = self.execute_command(self.readMeasurement,0.5)
        print(res)
        try:
            mean,deviation,min,max=res.split(',')
            mean = int(float(mean)*1000)
            return mean
        except:
            self.logger.error("Error, Read Frequecy Value Failed!")
            return 0


class TelnetDevice:
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