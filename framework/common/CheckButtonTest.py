from framework.common.testing import Test
from framework.tools.device import CommandResult
from framework.tools.utils import colorprint

class CheckButtonTest(Test):
    def __init__(self, dut):
        super().__init__(dut, "Check Button Test")

    def test(self): 
        if locale.getdefaultlocale()[0] == 'zh_CN':
            colorprint("请准备开始测试")
        else:
            colorprint("please press any key to begin the BUTTON TEST...","YELLOW")
        os.system("pause")

        if locale.getdefaultlocale()[0] == 'zh_CN':
            colorprint("请在6秒之内按下按键","YELLOW")
        else:
            colorprint("please press the button within 10 seconds", "YELLOW")

        rc, text = self.dut.execute_command("push_button test 10", 11000)
        if rc == 0:
            self.logger.info( "CSVFILE check_button ok ok pass")
            return True
        else:
            self.logger.info( "Error!! No Button pressing deteced, or Button Test failed")
            self.logger.info( showErrorCode("50301"))
            self.logger.info( "CSVFILE check_button ok fail fail")
            return False
