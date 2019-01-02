from framework.common.testing import Test
from framework.tools.config import configget
from framework.tools.device import CommandResult
import time


class SetGateway(Test):
    def __init__(self, dut):
        super().__init__(dut, "Set Gateway")

    def test(self):
        ''' This function is to set the gat eway the bike'''
        gateway =  configget("PERSO","gateway_url")

        cmd_text = "gateway_get"
        res = CommandResult.parse(self.dut.execute_command(cmd_text,5000)[1])
        if res.rc == 0 and gateway == res.data['gateway']:
            self.logger.info( "CSVFILE Get_Gateway ok ok pass")
            self.logger.info( "CSVFILE Set_Gateway ok ok pass")
            return True
        else:
            self.logger.info( "CSVFILE Get_Gateway ok ng fail")
            cmd_text = "gateway_set -u %s"%gateway
            r,text = self.dut.execute_command(cmd_text,5000)
            if r != 0:
                self.logger.info( "CSVFILE Set_Gateway ok ng fail")
                return False
            self.logger.info( "CSVFILE Set_Gateway ok ok pass")
            return True
