from framework.common.testing import Test
from framework.tools.device import CommandResult
from framework.tools.utils import colorprint, op_messager, ENCODING

class CheckStackDetect(Test):
    def __init__(self, dut):
        super().__init__(dut, "Check Check Stack Detect")

        if ENCODING == 1 or ENCODING == 2:
            # Language setting
            self.message = (
            "停車入樁測試",
            "按下開關，短接單車右側兩個電磁鐵金屬觸點，按Enter鍵繼續 ",
            "打開開關，測試結束，按Enter下一項。。。"
        )
        else:
            self.message = (
            "Ready to do the STACK DETECT test? Go!",
            "Now turn on the switch, Bike is in stack!!!",
            "Turn off the switch, Test finished, Press ENTER...",
        )

    def test(self): 

        flag = True
        message = self.message
        colorprint(message[0],"YELLOW")

        # Switch OFF, 
        res = CommandResult.parse(self.dut.execute_command("stack_check", 5000)[1])
        if res.rc == 0 and res.data["in_stack"] == "0":
            self.logger.info( "CSVFILE stack_check_off_stack ok ok pass")
        else:
            self.logger.info( "CSVFILE stack_check_off_stack ok ng fail")
            flag = False


        # Switch ON
        op_messager(message[1])
        input()

        res = CommandResult.parse(self.dut.execute_command("stack_check", 5000)[1])
        if res.rc == 0 and res.data["in_stack"] == "1":
            self.logger.info( "CSVFILE stack_check_in_stack ok ok pass")
        else:
            self.logger.info( "CSVFILE stack_check_in_stack ok ng fail")
            flag = False

        colorprint(message[2],"GREEN")
        input()
        return flag
