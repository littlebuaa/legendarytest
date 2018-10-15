from framework.common.testing import Test
from framework.tools.device import CommandResult

import time

class CheckPLS(Test):
    def __init__(self, dut):
        super().__init__(dut, "Check PLS")

    def test(self):
        '''This function is to check the previous utc is set, then set the current station pls to 0''' 
        cur_station=configget("PLS_INFO","current_station_id")
        pre_station=configget("PLS_INFO","pre_station_id")

        if cur_station=="10":
            self.logger.info( "Current station is T10, only set to zero!")
            rt,text_ = self.dut.execute_command("pls set %s 0"%(cur_station),1000)
            if rt == 0:
                self.logger.info( "CSVFILE set_current_pls_0 ok ok pass")
                return True
            else:
                self.logger.info( "CSVFILE set_current_pls_0 ok ng fail")
                self.logger.info( "set current station utc to 0 fail.")
                return False

        # Check Prestation UTC
        rc,text = self.dut.execute_command("pls list",3000)
        if rc!= 0:
            self.logger.info( "CSVFILE pls_list ok ng fail")
            return False
        res = CommandResult.parse(text)
        self.logger.info( "CSVFILE pls_list ok ok pass")

        pre_key = "station[00%s].utc"%pre_station
        if (pre_key in res.data and len(res.data[pre_key]) == 10 and int(res.data[pre_key]) < int(time.time())):
            self.logger.info( "CSVFILE pls_prestation_utc [1470636488;[ %s pass"%res.data[pre_key])
            rt,text_ = self.dut.execute_command("pls set %s 0"%(cur_station),1000)
            if rt == 0:
                self.logger.info( "CSVFILE set_current_pls_0 ok ok pass")
                self.logger.info( "Current station utc set to 0")
                return True
            else:
                self.logger.info( "CSVFILE set_current_pls_0 ok ng fail")
                self.logger.info( "set Current station utc to 0 fail.")
                return False

        else:
            self.logger.info( "CSVFILE pls_prestation_utc [1470636488;[ no_data fail")
            self.logger.info( "PLS set to 0 failed!!!")
            return False