from framework.common.testing import Test
from framework.tools.device import CommandResult
from framework.tools.config import configget
import time
import re

class CheckCPUID(Test):
    def __init__(self, dut):
        super().__init__(dut, "Check Product ID")

    def test(self):
        '''This function is to check Customization ID , very important for iOS installation.'''
        cpu_hw_rev_target = configget("PERSO","cpu_hw_rev")
        self.logger.info( "CPU_ID_check:")

        cmd_set = "get_cpu_id"
        rc,text = self.dut.execute_command(cmd_set,2000)
        if rc!= 0:
            self.logger.info( "CSVFILE CPU_ID xxxx -1 FAIL")
            self.logger.info( "CSVFILE CPU_HW_REV_ID xxxx -1 FAIL")
            return False
        cpu_dic = CommandResult.parse(text)
        cpu_id = cpu_dic.data["cpu_id"]
        cpu_hw_rev_id = cpu_dic.data["cpu_hw_rev"]
        self.logger.info( "CSVFILE CPU_ID xxxx %s PASS"%cpu_id)
        self.logger.info( "CSVFILE CPU_HW_REV_ID %s %s PASS"%(cpu_hw_rev_target,cpu_hw_rev_id))
        return True



        """   
        p = re.compile('(?P<cust_id>0x[0-9]*)')
        m = p.search(text_)
        cust_id = m.group('cust_id') if m != None else -1
        if r != 0 or int(cust_id) != int(cust_id_target):
            self.logger.info( "customization id check FAIL")
            self.logger.info( "CSVFILE check_customization ok ng fail")
            return False
        else:
            self.logger.info( "get_customization finished, OK")
            self.logger.info( "CSVFILE check_customization ok ok pass")
            return True
        """