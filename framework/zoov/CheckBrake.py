from framework.common.testing import Test
from framework.tools.device import CommandResult
from framework.tools.utils import colorprint, op_messager, ENCODING
import locale,os

class CheckBrake(Test):
    def __init__(self, dut):
        super().__init__(dut, "Check Brake Detect")
        if ENCODING == 1 or ENCODING == 2:
            # Language setting
            self.message = (
                "------------------------- \n煞車Brake檢測，準備好後按Enter鍵繼續\n----------------------------",
                "請捏緊左邊的前煞，同時按Enter鍵",
                "請捏緊右邊的後煞，同時按Enter鍵",
                "測試結束，下一項。。。"
            )
        else:
            self.message = (
                "Ready to do the Brake DETECT test? Go!",
                "Apply Only the Left Brake, and at the same time, press ENTER...",
                "Apply Only the Left Brake, and at the same time, Press ENTER!!!",
                "Test finished, please remove the battery, Then press ENTER..."
            )

    def test(self):
        flag = True
        message = self.message
        colorprint(message[0],"YELLOW")
        input()

        # No Brake OFF, 
        res = CommandResult.parse(self.dut.execute_command("brake_check", 5000)[1])
        if res.rc == 0 and res.data["left_brake"] == "0" and res.data["right_brake"] == "0":
            self.logger.info( "CSVFILE left_brake_off ok ok pass")
            self.logger.info( "CSVFILE right_brake_off ok ok pass")
        else:
            self.logger.info( "CSVFILE left_brake_off ok ng fail")
            self.logger.info( "CSVFILE right_brake_off ok ng fail")
            flag = False
        
        # Left Brake ON,
        op_messager(message[1])
        input()
        res = CommandResult.parse(self.dut.execute_command("brake_check", 5000)[1])
        if res.rc == 0 and res.data["left_brake"] == "1" and res.data["right_brake"] == "0":
            self.logger.info( "CSVFILE left_brake_on ok ok pass")
        else:
            self.logger.info( "CSVFILE left_brake_on ok ng fail")
            flag = False


        # Right Brake ON, 
        op_messager(message[2])
        input()

        res = CommandResult.parse(self.dut.execute_command("brake_check", 5000)[1])
        if res.rc == 0 and res.data["left_brake"] == "0" and res.data["right_brake"] == "1":
            self.logger.info( "CSVFILE right_brake_on ok ok pass")
        else:
            self.logger.info( "CSVFILE right_brake_on ok ng fail")
            flag = False


        colorprint(message[3],"GREEN")
        return flag
