from framework.common.testing import Test
from framework.tools.device import CommandResult
from framework.tools.utils import colorprint, question_timeout, op_messager, ENCODING
import os
import locale



class CheckBatteryDetect(Test):
    def __init__(self, dut):
        super().__init__(dut, "Check Battery Detect")

    def test(self):
        if ENCODING == 1 or ENCODING == 2:
            op_messager("動力電池檢測，請將動力電池裝在車上，或者啟動36V電源，然後按Enter鍵")
        else:
            op_messager("Battery Detect Test, please put the personal battery on the holder, or Turn on 36V power supply, Then press ENTER...")
        flag = True
        input()

        res = CommandResult.parse(self.dut.execute_command("batt_detect", 5000)[1])
        if res.rc == 0 and res.data["value"] == "0":
            self.logger.info( "CSVFILE Battery_detect ok ok pass")
        else:
            self.logger.info( "CSVFILE Battery_detect ok ng fail")
            flag = False

        colorprint("Test finished, please remove the battery, Then press ENTER...","GREEN")
        input()
        return flag