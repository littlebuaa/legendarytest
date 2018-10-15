from framework.common.testing import Test
from framework.tools.device import CommandResult
from framework.tools.utils import compare_value


class CheckBatteryTest(Test):
    def __init__(self, dut):
        super().__init__(dut, "check battery")

    def test(self):
       #get limit from config.ini
        battery_mv_min = int(configget("TEST_ITEMS", "BATTERY_MV_MIN"))
        battery_mv_max = int(configget("TEST_ITEMS", "BATTERY_MV_MAX"))
        
        #get battery level value
        rc, text = self.dut.execute_command("get_battery",2000)
        if rc != 0:
            self.logger.info( "CSVFILE get_battery ok   fail")
            self.logger.info( "CSVFILE get_battery_mv [0;6000] -1 fail")
            self.logger.info( "CSVFILE get_battery_percent [0;100] -1 fail")
            return False
        else:
            self.logger.info( "CSVFILE get_battery ok ok pass")
            res = CommandResult.parse(text)
            voltage_mv = int(res.data["voltage_mv"])
            percent = res.data["percent"]
            self.logger.info( "CSVFILE get_battery_percent [0;100] "+ percent + " pass")
            rt = compare_value("get_battery_voltage", voltage_mv, battery_mv_min, battery_mv_max)
            return True if rt==0 else False
