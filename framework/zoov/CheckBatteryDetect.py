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

        flag = True
        msg = "Is 36v battery well mounted?? " 
        reponse = question_timeout(msg,30)
        if reponse[0] and (reponse[1].strip().lower()[0] == "y"):
            self.logger.info( "CSVFILE Battery_detect ok ok pass")
        else:
            self.logger.info( "CSVFILE Battery_detect ok fail fail")
            flag = False

        colorprint("Test finished, please remove the battery, Then press ENTER...","YELLOW")
        return flag