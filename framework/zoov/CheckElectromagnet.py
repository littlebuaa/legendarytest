from framework.common.testing import Test
from framework.tools.device import CommandResult
from framework.tools.utils import colorprint,question_timeout
import locale

class CheckElectromagnet(Test):
    def __init__(self, dut):
        super().__init__(dut, "Chec Electromagnet")

    def test(self): 
        if locale.getdefaultlocale()[0] == 'zh_CN':
            colorprint("请准备开始测试")
        else:
            colorprint("Ready to do the electromagnet check test? Go!","YELLOW")
        flag = False


        # Turn on electromagnet 
        res = CommandResult.parse(self.dut.execute_command("electromagnet on", 4000)[1])
        if res.rc == 0:
            colorprint("Measure the voltage of Electromagnet OUTPUT","YELLOW")
            input()
            msg = "Is voltage around 24V? Yes/No? " 
            reponse = question_timeout(msg,15)
            if reponse[0] and (reponse[1].strip().lower()[0] == "y"):
                self.logger.info( "CSVFILE check_electromagnet ok ok pass")
                flag = True

        self.dut.execute_command("electromagnet off", 4000)
        if not flag:
            self.logger.info( "CSVFILE check_electromagnet ok ng fail")
        return flag


