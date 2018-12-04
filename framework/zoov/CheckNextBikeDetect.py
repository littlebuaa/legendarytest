from framework.common.testing import Test
from framework.tools.device import CommandResult
from framework.tools.utils import colorprint, op_messager, get_encoding

class CheckNextBikeDetect(Test):
    def __init__(self, dut):
        super().__init__(dut, "Check Next Bike Stack Detect")
        ENCODING = get_encoding()
        if ENCODING == 1 or ENCODING == 2:
            # Language setting
            self.message = (
            "有車來泊功能檢測",
            "正常狀態，單車後輪左右兩個觸點連結斷開，按Enter鍵繼續", # 此行不會顯示
            "連結單車後輪兩側的磁鐵觸點，按Enter鍵繼續 ",
            "測試結束，按Enter下一項。。。"
        )
        else:
            self.message = (
            "Ready to do the NEXT Bike DETECT test? Go!",
            "First make sure switch is off, No new bike",
            "Connect (short-circuit) the 2 rear stack point.",
            "Test finished, Press ENTER...",
        )

    def test(self): 

        message = self.message
        colorprint(message[0],"YELLOW")
        flag = True


        # Switch OFF,
        res = CommandResult.parse(self.dut.execute_command("stack_nb_check", 5000)[1])
        if res.rc == 0 and res.data["value"] == "1":
            self.logger.info( "CSVFILE stack_check_next_bike ok ok pass")
        else:
            self.logger.info( "CSVFILE stack_check_next_bike ok ng fail")
            flag = False
        
        op_messager(message[2])
        # Switch ON, 
        res = CommandResult.parse(self.dut.execute_command("stack_nb_check", 5000)[1])
        if res.rc == 0 and res.data["value"] == "0":
            self.logger.info( "CSVFILE stack_check_next_bike ok ok pass")
        else:
            self.logger.info( "CSVFILE stack_check_next_bike ok ng fail")
            flag = False

        colorprint(message[3],"GREEN")
        return flag
