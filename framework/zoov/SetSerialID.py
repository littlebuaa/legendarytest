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
        ## read mac file, search for secret
        cmd_text = "bike_serial_number_set -s %s"%serial_input
        r,text = self.dut.execute_command(cmd_text,5000)
        if r != 0:
            self.logger.info( "CSVFILE Set_Serial_ID ok ng fail")
            return False
        time.sleep(1)
        res = CommandResult.parse(self.dut.execute_command("bike_serial_number_get", 5000)[1])
        if res.rc == 0 and res.data["serial number"] == serial_input:
            self.logger.info( "CSVFILE Set_Serial_ID ok ok pass")
            return True
        else:
            self.logger.info( "CSVFILE Set_Serial_ID ok ng fail")
            return False