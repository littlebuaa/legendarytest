from framework.common.testing import Test
from framework.tools.device import CommandResult
from framework.tools.utils import colorprint,question_timeout, get_encoding, op_messager
import time
import locale,os

class CheckSound(Test):
    def __init__(self, dut):
        super().__init__(dut, "Check Sound Bip")
        ENCODING = get_encoding()
        if ENCODING == 1 or ENCODING == 2:
            # Language setting
            self.message = (
            "Speak 喇叭測試 ",
            "請聽是否有BiBi聲，並按鍵確認",
            "是否聽到BiBi聲？？Yes/No?",
            "測試結束，進入下一項。。。",
        )
        else:
            self.message = (
            "Ready to do the SPEAKER test? Go!!",
            "Please ready to listen to the beep sound, press Enter to Begin...",
            "Did you hear the BipBip? Yes/No?",
            "Test finished, Next...",
        )

    def test(self):
        flag = False
        message = self.message
        colorprint(message[0],"YELLOW")
        op_messager(message[1])
        input()

        rc, text = self.dut.execute_command("play_sound", 10000)
        if rc == 0:
            reponse = question_timeout(message[2],40)
            if reponse[0] and (reponse[1].strip().lower() == "y"):
                self.logger.info( "CSVFILE play_sound ok ok pass")
                flag = True

        self.logger.info( "CSVFILE play_sound ok fail fail")
        colorprint(message[3],"GREEN")
        
        return flag
