#python v3.4; coding:UTF-8

import time
from framework.common.testing import Test
from framework.tools.device import CommandResult, Fluke
from framework.tools.config import configget
from framework.tools.utils import compare_value
class CheckVoltageTest(Test):
  
    def __init__(self, dut):
        super().__init__(dut, "check voltage")      
    
    def test(self):       
        #check V_SYS    
        F1 = Fluke(configget("COM","fluke1"))
        # if not F1.open():
            # self.logger.info("FLUKE_V_SYS UART Problem, COM port open failed!!")
            # return False
        # else:
        time.sleep(2)
        v_sys = F1.get_voltage()
        res1 = compare_value("V_SYS",v_sys,2.00,5.00)
        #return True if res1==0 else False
            
        #check V3_SW
        F2 = Fluke(configget("COM","fluke2"))
        # if not F2.open():
            # self.logger.info("FLUKE_V3_SW UART Problem, COM port open failed!!")
            # return False
        # else:
        time.sleep(2)
        v3_sw = F2.get_voltage()
        res2 = compare_value("V3_SW",v3_sw,0,4.05)
        return True if res1&res2==0 else False

        
    


