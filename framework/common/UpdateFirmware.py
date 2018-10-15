from framework.common.WaitShell import WaitShell
from framework.common.testing import Test
from framework.tools.device import CommandResult, DUT
from framework.tools.config import configget

class UpdateFirmware(Test):
    def __init__(self, dut):
        super().__init__(dut, "Update firmware")

    def test(self):
        '''This function is to update firmware, put the DUT to reset and reboot with "boot hello" so that the wsflash can work'''
        toFlash = configget("PERSO","FIRMWARE_BL_UPDATE")
        if toFlash == "N":
            self.logger.info("Firmware update disabled.")
            self.logger.info("CSVFILE firmware_update good good pass")
        elif  toFlash == "Y":
            targetversion = int(configget("PERSO","SOFT_VERSION"))
            com_port = configget("COM","dut")
            try:
                targetBinName = configget("PERSO","SOFT_BIN")
                wsflash = configget("TOOL","WSFLASH")
            except:
                self.logger.info("Config miss item: firmware binary path and/or the wsflash path.")
                self.logger.info("CSVFILE firmware_update ng good fail")
                return False
                
            if int(self.dut.prop["soft_version"]) < targetversion:
                '''if firmware is smaller than config, to flash'''
                self.logger.info("Firmware need to be updated according to the config.")
                self.dut.execute_command("mem write 32 0x4003E000 0x0")
                self.dut.send_command("standby 2")
                self.dut.uart.close()
                self.logger.info("COM port closed, ready to Flash")
                self.logger.info("++++++++++++++++++++++++  Flash Begin  +++++++++++++++++++++++++++++++")
                flash_cmd = "%s -f %s -s %s -e"%(wsflash,targetBinName,com_port)
                self.logger.info("====>%s"%flash_cmd)
                ret = os.system(flash_cmd)
                if ret == 0:
                    self.logger.info("++++++++++++++++++++++++  Flash End  +++++++++++++++++++++++++++++++")
                    self.logger.info("Flash end! Wait for reboot! 15s")
                    wait_time = 16
                    for x in range(wait_time):
                        self.logger.info("========================= count down %d ============================"%(wait_time-x))
                        time.sleep(1)
                    try:
                        self.dut.uart.open()
                    except:
                        self.logger.error("UART COM port re-open failed, Firmware update Fail")
                        self.logger.info("CSVFILE firmware_update ng good fail")
                        return False
                    result = WaitShell(self.dut).test(False)
                    if result:
                        self.logger.info("CSVFILE firmware_update good good pass")
                        return True
                    else:
                        self.logger.error("DUT not rebooted properly, Firmware update Fail")
                        self.logger.info("CSVFILE firmware_update ng good fail")
                        return False
                else:
                    self.logger.error("Flash programe fail, Firmware update Fail")
                    self.logger.info("CSVFILE firmware_update ng good fail")
                    return False
                    
