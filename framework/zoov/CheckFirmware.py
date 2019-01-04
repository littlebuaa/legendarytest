from framework.common.testing import Test
from framework.tools.config import configget
from framework.tools.device import CommandResult

class CheckFirmware(Test):
    def __init__(self, dut):
        super().__init__(dut, "Get Firmware")

    def test(self):
        main01_config =  configget("PERSO","main_build_version")
        controller01_config =  configget("PERSO","controller_build_version")

        cmd_set = "get_firmware_version"
        res = CommandResult.parse(self.dut.execute_command(cmd_set,10000)[1])
        main01 = res.data['main_version']
        controller01 =  res.data['controller_version']

        if res.rc != 0:
            self.logger.info( "CSVFILE Check_Firmware ok ng fail")
            return False
        else:
            self.logger.info( "CSVFILE Check_Firmware ok ok pass")
            return True
