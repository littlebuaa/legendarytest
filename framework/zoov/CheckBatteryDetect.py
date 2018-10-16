from framework.common.testing import Test
from framework.tools.device import CommandResult
from framework.tools.utils import colorprint
import os
import locale



class CheckBatteryDetect(Test):
    def __init__(self, dut):
        super().__init__(dut, "Check Battery Detect")

    def test(self): 
        if locale.getdefaultlocale()[0] == 'zh_CN':
            colorprint("请准备开始测试")
        else:
            colorprint("Battery Detect Test, please put the personal battery on the holder, Then press ENTER...","YELLOW")
        os.system("pause")

        rc, text = self.dut.execute_command("batt_detect", 3000)
        res = CommandResult.parse(text)
        if res.rc == 0 and res.data["value"] == "0":
            self.logger.info( "CSVFILE Battery_detect ok ok pass")
            colorprint("Test finished, please remove the battery, Then press ENTER...","YELLOW")
            os.system("pause")
            return True
        else:
            self.logger.info( "CSVFILE Battery_detect ok fail fail")
            colorprint("Test finished, please remove the battery, Then press ENTER...","YELLOW")
            os.system("pause")
            return False
