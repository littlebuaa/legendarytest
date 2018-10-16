import time
from framework.common.testing import Test

class WaitShellConnect(Test):
    def __init__(self, dut, timeout=25000):
        super().__init__(dut, "wait shell")
        self.timeout = timeout

    def test(self):
        start_time = time.time()
        self.logger.info("----------Waiting for shell>>>>>")
        prompt = self.dut.get_name() + ">"
        key = self.dut.get_shell(prompt, self.timeout)
        if key:
            self.logger.info("Shell Found!")
            self.logger.info("CSVFILE wait_shell" + " shell_found shell_found pass")
            r,text_ = self.dut.execute_command("connect",10000)
            if r==0:
                self.logger.info("CSVFILE connect" + " 0 0 pass")
                return True
            else:
                self.logger.info("CSVFILE connect" + " 0 %d fail"%r)
                return False
        else:
            self.logger.info("No shell found, Timeout!")
            self.logger.info("CSVFILE wait_shell" + " shell_found no_uart_detected fail")
            return False
