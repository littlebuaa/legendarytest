from framework.common.testing import Test
from framework.tools.device import CommandResult


class CheckMacTest(Test):
    def __init__(self, dut):
        super().__init__(dut, "check MAC")

    def test(self):
        ''' This function is to check the MAC scaned and MAC probe '''
        ## get value
        mac_label = self.dut.prop["mac_label"]
        mac_probe = self.dut.prop["mac"]

        self.logger.info("MAC scanned is %s"%mac_label)
        self.logger.info("MAC in the flash is %s"%mac_probe)

        if mac_probe.replace(':','') != mac_label.replace(':',''): # ATTENTION: upper/lower sensible
            self.logger.info("Internal flash MAC does not match scanned label MAC!")
            self.logger.info("CSVFILE mac_checking " + mac_label + " " + mac_probe + " fail")
            return False
        else:
            self.logger.info( "Internal flash MAC = scanned label MAC, MAC checking OK!")
            self.logger.info( "CSVFILE mac_checking " + mac_label + " " + mac_probe + " pass")
            return True
