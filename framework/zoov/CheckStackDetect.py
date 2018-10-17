from framework.common.testing import Test
from framework.tools.device import CommandResult
from framework.tools.utils import colorprint
import locale,os

class CheckStackDetect(Test):
    def __init__(self, dut):
        super().__init__(dut, "Check Check Stack Detect")

    def test(self): 
        if locale.getdefaultlocale()[0] == 'zh_CN':
            colorprint("请准备开始测试")
        else:
            colorprint("Ready to do the STACK DETECT test? Go! 准备好测试了吗？","YELLOW")
        print()
        input()

        flag = True


        # Switch OFF, 
        colorprint("First make sure switch is off, Bike is off stack!!! 准备好了吗？","YELLOW")
        input()
        res = CommandResult.parse(self.dut.execute_command("stack_check", 5000)[1])
        if res.rc == 0 and res.data["in_stack"] == "0":
            self.logger.info( "CSVFILE stack_check_off_stack ok ok pass")
        else:
            self.logger.info( "CSVFILE stack_check_off_stack ok ng fail")
            flag = False
        
        colorprint("Now turn on the switch, Bike is in stack!!! 准备好了吗？","YELLOW")
        input()

        # Switch ON, 
        res = CommandResult.parse(self.dut.execute_command("stack_check", 5000)[1])
        if res.rc == 0 and res.data["in_stack"] == "1":
            self.logger.info( "CSVFILE stack_check_in_stack ok ok pass")
        else:
            self.logger.info( "CSVFILE stack_check_in_stack ok ng fail")



        return flag
