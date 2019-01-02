from framework.common.testing import Test
from framework.tools.config import configget
from framework.tools.device import CommandResult
import time


class GetGateway(Test):
    def __init__(self, dut):
        super().__init__(dut, "Get Gateway")

    def test(self):
        ''' This function is to set the gat eway the bike'''
        gateway =  configget("PERSO","gateway_url")

        cmd_text = "gateway_get"
        res = CommandResult.parse(self.dut.execute_command(cmd_text,5000)[1])
        if res.rc == 0 and gateway == res.data['gateway']:
            self.logger.info( "CSVFILE Set_Gateway ok ok pass")
            return True
        self.logger.info( "CSVFILE Set_Gateway ok ng fail")
        return False