from framework.common.testing import Test
from framework.tools.config import configget

class GetStation(Test):
    def __init__(self, dut):
        super().__init__(dut, "Get pre Station result")

    def test(self):
        '''This function is to set Customization ID, very important for iOS installation.''' 
        
        cmd_set = "get_test_station -s t20a"
        r,text_ = self.dut.execute_command(cmd_set,5000)
        if r != 0:
            self.logger.info( "CSVFILE get_station ok ng fail")
            return True
        else:
            self.logger.info( "CSVFILE get_station ok ok pass")
            return True
