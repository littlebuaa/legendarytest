from framework.common.testing import Test

class CheckFlashTest(Test):
    def __init__(self, dut):
        super().__init__(dut, "Check Flash Test")

    def test(self):
        rc, text = self.dut.execute_command("spiflash memtest 0 8",25000)
        
        if rc != 0:
            self.logger.info( "CSVFILE SPIFLASH_MEMTEST 0 -1 FAIL")
            return False
        else:
            self.logger.info( "SPIFLASH_MEMTEST 0 0 PASS")
            return True 
