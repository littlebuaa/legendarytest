from framework.common.testing import Test
from framework.tools.device import CommandResult
from framework.tools.utils import colorprint,question_timeout, get_encoding, op_messager
import locale

class CheckPowerLED(Test):
    def __init__(self, dut):
        super().__init__(dut, "Check POWER LED")
        ENCODING = get_encoding()
        if ENCODING == 1 or ENCODING == 2:
            # Language setting
            self.message = (
            "電池架上紅色 POWER 指示燈檢測，按Enter鍵繼續",
            "請注意查看POWER燈是否點亮，並按鍵確認",
            "紅色POWER燈是否正常點亮？Yes/No?",
            "測試結束，進入下一項。。。",
        )
        else:
            self.message = (
            "Ready to do the POWER LED check test? Go!!",
            "check the RED POWER LED is on or off!",
            "Did you see the POWER LED on? Yes/No?",
            "Test finished, Next...",
        )

    def test(self): 
            
        message = self.message
        flag = False
        colorprint(message[0],"YELLOW")


        # Turn on light 
        res = CommandResult.parse(self.dut.execute_command("power_led on", 4000)[1])
        if res.rc == 0:
            op_messager(message[1])
            input()
            reponse = question_timeout(message[2],60)
            if reponse[0] and (reponse[1].strip().lower()[0] == "y"):
                self.logger.info( "CSVFILE check_power_led ok ok pass")
                flag = True

        self.dut.execute_command("power_led off", 4000)
        if not flag:
            self.logger.info( "CSVFILE check_power_led ok ng fail")
        colorprint(message[3],"GREEN")
        return flag


