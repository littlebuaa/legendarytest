from framework.common.testing import Test
from framework.tools.config import configget

class SetCustomization(Test):
    def __init__(self, dut):
        super().__init__(dut, "Set Customization")

    def test(self):
        '''This function is to set Customization ID, very important for iOS installation.''' 
        cust_id_target =  configget("PERSO","CUSTOM_ID")
        cmd_set = "customization_id set %s"%cust_id_target
        r,text_ = self.dut.execute_command(cmd_set,2000)
        if r != 0:
            self.logger.info( "set_customization finished, FAIL")
            self.logger.info( "CSVFILE set_customization ok ng fail")
            return False
        else:
            self.logger.info( "set_customization finished, OK")
            self.logger.info( "CSVFILE set_customization ok ok pass")
            return True
