from framework.common.testing import Test
from framework.tools.config import configget
from framework.tools.device import CommandResult
import time


class SetSerialID(Test):
    def __init__(self, dut):
        super().__init__(dut, "Set Serial ID")
        
    def test(self):
        ''' This function is to set Serial ID to the bike'''
        ''' Global MAC_label must be valide'''
        serial_input=  self.dut.serial_id

        cmd_text = "bike_serial_number_set -s %s"%serial_input
        r,text = self.dut.execute_command(cmd_text,5000)
        if r != 0:
            self.logger.info( "CSVFILE Set_Serial_ID ok ng fail")
            return False

        self.logger.info( "CSVFILE Set_Serial_ID ok ok pass")
        return True
