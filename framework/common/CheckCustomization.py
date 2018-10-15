from framework.common.testing import Test
from framework.tools.device import CommandResult
from framework.tools.config import configget
import time
import re

class CheckCustomization(Test):
    def __init__(self, dut):
        super().__init__(dut, "Check Customization")

    def test(self):
        '''This function is to check Customization ID , very important for iOS installation.'''
        cust_id_target = configget("PERSO","CUSTOM_ID")
        self.logger.info( "customization id check:")
        cmd_set = "customization_id get"
        r,text_ = self.dut.execute_command(cmd_set,2000)
        p = re.compile('(?P<cust_id>0x[0-9]*)')
        m = p.search(text_)
        cust_id = m.group('cust_id') if m != None else -1
        if r != 0 or int(cust_id) != int(cust_id_target):
            self.logger.info( "customization id check FAIL")
            self.logger.info( "CSVFILE check_customization ok ng fail")
            return False
        else:
            self.logger.info( "get_customization finished, OK")
            self.logger.info( "CSVFILE check_customization ok ok pass")
            return True
