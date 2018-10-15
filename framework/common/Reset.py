from framework.common.WaitShell import WaitShell
from framework.common.testing import Test


class Reset(Test):
    def __init__(self, dut):
        super().__init__(dut, "reset")
        
    def test(self):
        self.dut.send_command("reset")
        return(self.dut.get_shell())

