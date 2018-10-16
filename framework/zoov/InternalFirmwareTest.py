from framework.common.testing import Test
from framework.tools.config import configget

class InternalFirmwareTest(Test):
    def __init__(self, dut):
        super().__init__(dut, "Do internal firmware test")

    def test(self):
        '''This function is to set Customization ID, very important for iOS installation.''' 
        
        cmd_set = "internal_firmware_test"
        r,text_ = self.dut.execute_command(cmd_set,10000)
        if r != 0:
            self.logger.info( "CSVFILE Internal_Firmware_Test ok ng fail")
            return False
        else:
            self.logger.info( "CSVFILE Internal_Firmware_Test ok ok pass")
            return True
