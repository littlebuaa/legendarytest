from framework.common.testing import Test
from framework.tools.device import CommandResult
from framework.tools.utils import colorprint, op_messager, get_encoding
import os
import locale



class CheckBatteryDetect(Test):
    def __init__(self, dut):
        super().__init__(dut, "Check Battery Detect")

    def test(self):
        ENCODING = get_encoding()
        if ENCODING == 1 or ENCODING == 2:
            op_messager("動力電池檢測，按Enter鍵繼續 >>> ")
        else:
            op_messager("Battery Detect, please put the personal battery on the holder, or Turn on 36V power supply, Then press ENTER...")
        flag = True

        res = CommandResult.parse(self.dut.execute_command("batt_detect", 5000)[1])
        if res.rc == 0 and res.data["value"] == "0":
            self.logger.info( "CSVFILE Battery_detect ok ok pass")
        else:
            self.logger.info( "CSVFILE Battery_detect ok ng fail")
            flag = False

        colorprint("Test finished, Press ENTER...","GREEN")
        return flag