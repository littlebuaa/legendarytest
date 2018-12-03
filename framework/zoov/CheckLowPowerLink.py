from framework.common.testing import Test
from framework.tools.device import CommandResult
from framework.tools.utils import colorprint,question_timeout, get_encoding, op_messager
import locale

class CheckLowPowerLink(Test):
    def __init__(self, dut):
        super().__init__(dut, "Check Low Power Link flag")
        ENCODING = get_encoding()
        if ENCODING == 1 or ENCODING == 2:
            # Language setting
            self.message = (
            "LOW POWER LINK 檢測",
            "請量測 Low Power Pin測點電壓。",
            "電壓是否穩定在3V左右，Yes/No?",
            "電壓是否降到0V，Yes/No?",
            "測試結束，進入下一項。。。",
        )
        else:
            self.message = (
            "Ready to do the LOW POWER LINK test? Go？",
            "Measure the voltage of low power link pin!!!",
            "Is low power flag PIN around 3V? Yes/No? ",
            "Is low power flag PIN falls to 0V? Yes/No? ",
            "Turn off the switch, Test finished, Press ENTER...",
        )

    def test(self):

        message = self.message
        colorprint(message[0],"YELLOW")
        flag = False


        # Turn on light 
        res = CommandResult.parse(self.dut.execute_command("low_power_check on", 4000)[1])
        if res.rc == 0:
            op_messager(message[1])
            input()
            reponse = question_timeout(message[2], 60)
            if reponse[0] and (reponse[1].strip().lower()[0] == "y"):
                self.dut.execute_command("low_power_check off", 4000)
                reponse = question_timeout(message[3],60)
                if reponse[0] and (reponse[1].strip().lower()[0] == "y"):
                    self.logger.info( "CSVFILE check_low_power_link ok ok pass")
                    flag = True

        self.logger.info( "CSVFILE check_low_power_link ok ng fail")

        colorprint(message[4],"GREEN")
        return flag



