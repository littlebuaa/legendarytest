from framework.common.testing import Test
from framework.tools.device import CommandResult
from framework.tools.utils import colorprint,question_timeout
import locale

class CheckPowerLED(Test):
    def __init__(self, dut):
        super().__init__(dut, "Check POWER LED")

    def test(self): 
        if locale.getdefaultlocale()[0] == 'zh_CN':
            colorprint("请准备开始测试")
        else:
            colorprint("Ready to do the POWER LED check test? Go! 准备好测试了吗？","YELLOW")
        input()

        flag = False


        # Turn on light 
        res = CommandResult.parse(self.dut.execute_command("power_led on", 4000)[1])
        if res.rc == 0:
            colorprint("check the RED POWER LED is on or off 准备好测试了吗？","YELLOW")
            input()
            msg = "Did you see the POWER LED on? Yes/No? " 
            reponse = question_timeout(msg,15)
            if reponse[0] and (reponse[1].strip().lower()[0] == "y"):
                self.logger.info( "CSVFILE check_power_led ok ok pass")
                flag = True

        self.dut.execute_command("power_led off", 4000)
        if not flag:
            self.logger.info( "CSVFILE check_power_led ok ng fail")
        return flag


