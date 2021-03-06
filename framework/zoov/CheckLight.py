from framework.common.testing import Test
from framework.tools.device import CommandResult
from framework.tools.utils import colorprint,question_box, get_encoding, op_messager
import locale

class CheckLight(Test):
    def __init__(self, dut):
        super().__init__(dut, "Check Front and Rear light")
        ENCODING = get_encoding()
        if ENCODING == 1 or ENCODING == 2:
            # Language setting
            self.message = (
            "車燈檢測，按Enter鍵繼續",
            "請注意查看前後車燈是否點亮，並按鍵確認",
            "車證是否正常？Yes/No?",
            "測試結束，進入下一項。。。",
        )
        else:
            self.message = (
            "Ready to do the Light check test? Go!",
            "Check Light",
            "Are both the Front and Rear Light ON?? Yes/No?",
            "Turn off the switch, Test finished, Press ENTER...",
        )


    def test(self):
        
        flag = False
        message = self.message
        op_messager(message[1])
        # Turn on light 
        res = CommandResult.parse(self.dut.execute_command("frontlight on", 4000)[1])
        # op_messager(message[1])
        if res.rc == 0:
            if question_box(message[2]):
                self.logger.info( "CSVFILE check_light ok ok pass")
                flag = True

        self.dut.execute_command("frontlight off", 4000)
        if not flag:
            self.logger.info( "CSVFILE check_light ok ng fail")
        colorprint(message[3],"GREEN")
        return flag


