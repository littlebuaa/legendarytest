
from framework.common.WaitShell import WaitShell
from subprocess import Popen
from framework.common.testing import Test
from framework.tools.device import CommandResult, DUT
from framework.tools.config import configget

class FlashFirmware(Test):
    def __init__(self, dut):
        super().__init__(dut, "Flash firmware")

    def test(self):
        toFlash = configget("PERSO","FIRMWARE_BL_UPDATE")
        if toFlash == "N":
            self.logger.info("No need Flash,config to disabled.")
        elif  toFlash == "Y":
            targetversion = int(configget("PERSO","SOFT_VERSION"))
            com_port = configget("COM","dut")
            try:
                targetBinName = configget("PERSO","SOFT_BIN")
                wsflash = configget("TOOL","WSFLASH")
            except:
                self.logger.info("Config miss item: firmware binary path and/or the wsflash path.")
                return False

            self.logger.info("Firmware need to be updated according to the config.")
            self.dut.uart.close()
            self.logger.info("COM port closed, ready to Flash")
            self.logger.info("++++++++++++++++++++++++  Flash Begin  +++++++++++++++++++++++++++++++")
            flash_cmd = "%s -f %s -s %s -e"%(wsflash,targetBinName,com_port)
            self.logger.info("====>%s"%flash_cmd)
            ret = os.system(flash_cmd)
            ###################################

            ###################################
            if ret == 0:
                self.logger.info("++++++++++++++++++++++++  Flash End  +++++++++++++++++++++++++++++++")
                self.logger.info("Flash end! Wait for reboot! 15s")
                wait_time = 14
                for x in range(wait_time):
                    self.logger.info("========================= count down %d ============================"%(wait_time-x))
                    time.sleep(1)
                try:
                    self.dut.uart.open()
                except:
                    self.logger.error("UART COM port re-open failed, Firmware flash Fail")
                    self.logger.info("++++++++++++++++++++++++  Flash End +++++++++++++++++++++++++++++++")
                    return False
                result = WaitShell(self.dut).test(False)
                if result:
                    self.logger.info("Firmware flash finished")
                    self.logger.info("++++++++++++++++++++++++  Flash End +++++++++++++++++++++++++++++++")
                    return True
                else:
                    self.logger.error("DUT not rebooted properly, Firmware flash Fail")
                    self.logger.info("++++++++++++++++++++++++  Flash End +++++++++++++++++++++++++++++++")
                    return False
            else:
                self.logger.error("Flash programe fail!!")
                self.logger.info("++++++++++++++++++++++++  Flash End +++++++++++++++++++++++++++++++")
                return False
                
