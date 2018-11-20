import time
from framework.common.testing import Test
from framework.tools.device import CommandResult

class WaitShellConnect(Test):
    def __init__(self, dut, timeout=25000):
        super().__init__(dut, "wait shell")
        self.timeout = timeout

    def test(self):
        flag = False
        start_time = time.time()
        self.logger.info("----------Waiting for shell>>>>>")
        prompt = self.dut.get_name() + ">"
        key = self.dut.get_shell(prompt, self.timeout)
        if key:
            self.logger.info("Shell Found!")
            self.logger.info("CSVFILE wait_shell" + " shell_found shell_found pass")
            r,text_ = self.dut.execute_command("connect",10000)
            if r==0:
                flag = True
            else:
                self.logger.info("CSVFILE connect" + " 0 %d fail"%r)
        else:
            self.logger.info("No shell found, Timeout!")
            self.logger.info("CSVFILE wait_shell" + " shell_found no_uart_detected fail")

        if flag:
            res = CommandResult.parse(self.dut.execute_command("factory_mode_get",5000)[1])
            if int(res.data["main01_factory_mode"]) == 4 and int(res.data["controller01_factory_mode"]) == 4:
                self.logger.info("Factory Mode 4, correct! Continue...")
                self.logger.info("CSVFILE connect" + " 0 0 pass")
            else:
                self.dut.execute_command("factory_mode_set --mode 4",5000)
                self.dut.execute_command("reboot",3000)
                time.sleep(5)
                r,text_ = self.dut.execute_command("connect",self.timeout)
                if r == 0:
                    self.logger.info("CSVFILE connect" + " 0 0 pass")
                else:
                    self.logger.info("CSVFILE connect" + " 0 %d fail"%r)
                    flag = False
        return flag
