from framework.common.testing import Test
from framework.tools.device import CommandResult
from framework.tools.utils import colorprint,question_timeout, op_messager, get_encoding
import locale

class CheckElectromagnet(Test):
    def __init__(self, dut):
        super().__init__(dut, "Chec Electromagnet")
        ENCODING = get_encoding()
        if ENCODING == 1 or ENCODING == 2:
            # Language setting
            self.message = (
            "電磁鐵檢測",
            "請確認車子右側，前後兩端的磁鐵正常工作,準備好後按Enter鍵繼續 ",
            "請確認車子右側，前後兩端的磁鐵均已失效",
            "磁鐵是否失效？？，Yes/No?",
            "測試結束，下一項。。。"
        )
        else:
            self.message = (
            "Ready to do the electromagnet check test? Go!",
            "Check if the Magnet of the stack on the right side works, Then press ENTER...",
            "Measure the voltage of Electromagnet OUTPUT, Or check the status of the Magnet",
            "Is voltage around 24V? Does the magnet lose its attraction?? Yes/No?",
            "Test finished, please remove the battery, Then press ENTER..."
        )

    def test(self):
        flag = False
        timeout = 60
        message = self.message
        colorprint(message[0],"YELLOW")
        op_messager(message[1])
        input()
        # Turn on electromagnet 
        res = CommandResult.parse(self.dut.execute_command("electromagnet on", 4000)[1])
        if res.rc == 0:
            op_messager(message[2])
            reponse = question_timeout(message[3],timeout)
            if reponse[0] and (reponse[1].strip().lower()[0] == "y"):
                self.logger.info( "CSVFILE check_electromagnet ok ok pass")
                flag = True

        self.dut.execute_command("electromagnet off", 4000)
        if not flag:
            self.logger.info( "CSVFILE check_electromagnet ok ng fail")
        colorprint(message[4],"GREEN")
        return flag


