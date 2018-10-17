from framework.common.testing import Test
from framework.tools.device import CommandResult
from framework.tools.utils import colorprint,question_timeout
import time
import locale,os

class CheckSound(Test):
    def __init__(self, dut):
        super().__init__(dut, "Check Sound Bip")

    def test(self): 
        if locale.getdefaultlocale()[0] == 'zh_CN':
            colorprint("请准备开始测试")
        else:
            colorprint("please ready to listen to the beep sound, press Enter to Begin the test...","YELLOW")

        rc, text = self.dut.execute_command("play_sound", 10000)
        if rc == 0:
            # msg = ("Did you hear Bipbip sound? Yes/No","YELLOW")
            msg = "Did you hear Bipbip sound? Yes/No? " 
            reponse = question_timeout(msg,10)
            print(reponse)
            if reponse[0] and (reponse[1].strip().lower() == "y"):
                self.logger.info( "CSVFILE play_sound ok ok pass")
                return True

        self.logger.info( "CSVFILE play_sound ok fail fail")
        return False
