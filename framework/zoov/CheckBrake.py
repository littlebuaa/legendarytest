from framework.common.testing import Test
from framework.tools.device import CommandResult
from framework.tools.utils import colorprint
import locale,os

class CheckBrake(Test):
    def __init__(self, dut):
        super().__init__(dut, "Check Brake Detect")

    def test(self): 
        if locale.getdefaultlocale()[0] == 'zh_CN':
            colorprint("请准备开始测试")
        else:
            colorprint("Ready to do the Brake DETECT test? Go!","YELLOW")
        flag = True


        # No Brake OFF, 
        res = CommandResult.parse(self.dut.execute_command("brake_check", 5000)[1])
        if res.rc == 0 and res.data["left_brake"] == "0" and res.data["right_brake"] == "0":
            self.logger.info( "CSVFILE left_brake_off ok ok pass")
            self.logger.info( "CSVFILE right_brake_off ok ok pass")
        else:
            self.logger.info( "CSVFILE left_brake_off ok ng fail")
            self.logger.info( "CSVFILE right_brake_off ok ng fail")
            flag = False
        
        colorprint("Apply Only the Left Brake, and Press Enter!!!","YELLOW")
        input()

        # Left Brake ON, 
        res = CommandResult.parse(self.dut.execute_command("brake_check", 5000)[1])
        if res.rc == 0 and res.data["left_brake"] == "1" and res.data["right_brake"] == "0":
            self.logger.info( "CSVFILE left_brake_on ok ok pass")
        else:
            self.logger.info( "CSVFILE left_brake_on ok ng fail")
            flag = False

        

        # Right Brake ON, 
        colorprint("Apply Right Brake Now, and Press Enter!!!","YELLOW")
        input()
        res = CommandResult.parse(self.dut.execute_command("brake_check", 5000)[1])
        if res.rc == 0 and res.data["left_brake"] == "0" and res.data["right_brake"] == "1":
            self.logger.info( "CSVFILE right_brake_on ok ok pass")
        else:
            self.logger.info( "CSVFILE right_brake_on ok ng fail")
            flag = False

        return flag
