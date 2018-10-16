from framework.common.testing import Test
from framework.tools.device import CommandResult
from framework.tools.utils import colorprint,question_timeout
import locale

class CheckLight(Test):
    def __init__(self, dut):
        super().__init__(dut, "Check Front and Rear light")

    def test(self): 
        if locale.getdefaultlocale()[0] == 'zh_CN':
            colorprint("请准备开始测试")
        else:
            colorprint("Ready to do the Light check test? Go! 准备好测试了吗？","YELLOW")
        input()

        flag = False


        # Turn on light 
        res = CommandResult.parse(self.dut.execute_command("frontlight on", 4000)[1])
        if res.rc == 0:
            colorprint("Measure the voltage of Front and Rear light? or check the light is on or off 准备好测试了吗？","YELLOW")
            input()
            msg = "Did you see the light or is voltage around 6V? Yes/No? " 
            reponse = question_timeout(msg,15)
            if reponse[0] and (reponse[1].strip().lower()[0] == "y"):
                self.logger.info( "CSVFILE check_light ok ok pass")
                flag = True

        self.dut.execute_command("frontlight off", 4000)
        if not flag:
            self.logger.info( "CSVFILE check_light ok ng fail")
        return flag


