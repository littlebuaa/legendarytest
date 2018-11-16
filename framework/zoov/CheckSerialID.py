from framework.common.testing import Test
from framework.tools.config import configget
from framework.tools.device import CommandResult
import time


class CheckSerialID(Test):
    def __init__(self, dut):
        super().__init__(dut, "Check Serial ID")
        
    def test(self):
        ''' This function is to set Serial ID to the bike'''
        ''' Global MAC_label must be valide'''

        res = CommandResult.parse(self.dut.execute_command("bike_serial_number_get", 5000)[1])
        if res.rc == 0 and res.data["serial number"] == self.dut.serial_id:
            self.logger.info( "CSVFILE Check_Serial_ID ok ok pass")
            return True
        else:
            self.logger.info( "CSVFILE Check_Serial_ID ok ng fail")
            return False