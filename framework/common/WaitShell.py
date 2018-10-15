import time
from framework.common.testing import Test

class WaitShell(Test):
    def __init__(self, dut, timeout=25000):
        super().__init__(dut, "wait shell")
        self.timeout = timeout

    def test(self):
        start_time = time.time()
        self.logger.info("----------Waiting for shell>>>>>")
        key = self.dut.get_shell(self.timeout)
        if key:
            self.logger.info("Shell Found!")
            self.logger.info("CSVFILE wait_for_shell" + " shell_found shell_found pass")
            return True
        else:
            self.logger.info("No shell found, Timeout!")
            self.logger.info("CSVFILE wait_for_shell" + " shell_found no_uart_detected fail")
            return False
