from framework.common.testing import Test
from framework.tools.device import CommandResult
from framework.tools.utils import colorprint,question_timeout
import locale

class CheckLowPowerLink(Test):
    def __init__(self, dut):
        super().__init__(dut, "Check Low Power Link flag")

    def test(self):
        if locale.getdefaultlocale()[0] == 'zh_CN':
            colorprint("请准备开始测试")
        else:
            colorprint("Ready to do the Low power link test? Go! 准备好测试了吗？","YELLOW")
        input()

        flag = False


        # Turn on light 
        res = CommandResult.parse(self.dut.execute_command("low_power_check on", 4000)[1])
        if res.rc == 0:
            colorprint("Measure the voltage of low power link pin!!! 准备好测试了吗？","YELLOW")
            input()
            msg = "Is low power flag on? Yes/No? " 
            reponse = question_timeout(msg,15)
            if reponse[0] and (reponse[1].strip().lower()[0] == "y"):
                self.dut.execute_command("low_power_check off", 4000)
                msg = "Is low power flag off? Yes/No? " 
                reponse = question_timeout(msg,15)
                if reponse[0] and (reponse[1].strip().lower()[0] == "y"):
                    self.logger.info( "CSVFILE check_low_power_link ok ok pass")
                    return True

        self.logger.info( "CSVFILE check_low_power_link ok ng fail")
        return False



