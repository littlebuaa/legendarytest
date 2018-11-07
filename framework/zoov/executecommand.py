from framework.common.testing import Test

class ExecuteCommand(Test):
    def __init__(self, dut, command, timeout=10000):
        super().__init__(dut, "exec" + command)
        self.command = command
        self.timeout = timeout

    def test(self):
        return_code, text = self.dut.execute_command(self.command,self.timeout)
        if return_code != 0:
            self.logger.info("CSVFILE " + self.name.replace(" ", "_") + " ok fail fail")
            return False
        self.logger.info("CSVFILE " + self.name.replace(" ", "_") + " ok ok pass")
        return True