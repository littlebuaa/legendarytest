from framework.common.testing import Test

class ExecuteCommand(Test):
    def __init__(self, dut, command):
        super().__init__(dut, "execute command " + command)
        self.command = command

    def test(self):
        return_code, text = self.dut.execute_command(self.command)
        if return_code != 0:
            self.logger.info("CSVFILE " + self.name.replace(" ", "_") + " ok fail fail")
            return False
        self.logger.info("CSVFILE " + self.name.replace(" ", "_") + " ok ok pass")
        return True