from subprocess import Popen
from framework.common.testing import Test
from framework.tools.device import CommandResult, DUT
from framework.tools.config import configget

import time


class FlashBootlodaer(Test):
    def __init__(self, dut):
        super().__init__(dut, "Flash Bootloader")

    def test(self):
        self.logger.info("Firmware need to be updated according to the config.")
        self.logger.info("COM port closed, ready to Flash")
        self.logger.info("++++++++++++++++++++++++  Flash Begin  +++++++++++++++++++++++++++++++")
        jtag_flash = configget("TOOL","JTAG")
        path = "MCU_FLASH"
        script_name="flash_bl_512.jlink"
        # flash_cmd = jtag_flash + " " +path + os.sep + script_name
        flash_cmd = path + os.sep + "jlink_burn.bat"
        self.logger.info("====>%s"%flash_cmd)
       
        ret = os.system(flash_cmd)
        print("ret is %d"%ret)
        ###################################

        ###################################
        if ret == 0 or ret==1:
            self.logger.info("++++++++++++++++++++++++  Flash End  +++++++++++++++++++++++++++++++")
            self.logger.info("Flash end! Wait for reboot! 15s")
            wait_time = 20
            self.logger.info("++++++++++++++++++++++++  Flash End +++++++++++++++++++++++++++++++")
            return True
        else:
            self.logger.error("Flash programe fail!!")
            self.logger.info("++++++++++++++++++++++++  Flash End +++++++++++++++++++++++++++++++")
            return False
            
