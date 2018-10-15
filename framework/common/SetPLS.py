import time
from framework.common.testing import Test
from framework.tools.config import configget

class SetPLS(Test):
    def __init__(self, dut):
        super().__init__(dut, "Set PLS")

    def test(self):
        '''This function is to set the current station pls to the utc time stamp at the end of the test.''' 
        id = configget("PLS_INFO","CURRENT_STATION_ID")
        current_utc = int(time.time())

        cmd_set_utc = "pls set %s %d"%(id,current_utc)
        r,text_ = self.dut.execute_command("pls set %s %d"%(id,current_utc),2000)
        if r != 0:
            self.logger.info( "CSVFILE pls_set_current_utc ok cmd_fail fail")
            return False
        else:
            self.logger.info( "CSVFILE pls_set_current_utc ok %d pass"%current_utc)
            return True