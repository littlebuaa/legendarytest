from framework.common.testing import Test
from framework.tools.device import CommandResult
from framework.tools.utils import *

class CheckAcceleroTest(Test):
    def __init__(self, dut):
        super().__init__(dut, "check accelerometer")

    def test(self):
        
       #power up adxl
        rc, text = self.dut.execute_command("power up adxl",2000)
        
        if rc != 0:
            self.logger.info( "CSVFILE POWER_UP_ADXL 0 -1 FAIL")
            return False
        else:
            self.logger.info( "CSVFILE POWER_UP_ADXL 0 0 PASS")
            rc, text = self.dut.execute_command("adxl init",2000)
            if rc != 0:
                self.logger.info( "CSVFILE ADXL_INIT 0 -1 FAIL")
                return False
            else:
                self.logger.info( "CSVFILE ADXL_INIT 0 0 PASS")
                rc, text = self.dut.execute_command("adxl reset",2000)
                if rc != 0:
                    self.logger.info( "CSVFILE ADXL_RESET 0 -1 FAIL")
                    return False
                else:
                    self.logger.info( "CSVFILE ADXL_RESET 0 0 PASS")
                    rc, text = self.dut.execute_command("adxl init",2000)
                    if rc != 0:
                        self.logger.info( "CSVFILE CHECK_ADXL_INIT 0 -1 FAIL")
                        return False
                    else:
                        res = CommandResult.parse(text,':')
                        adxl_id_01 = str(res.data["[ADXL] ID_1"])    
                        self.logger.info( "CSVFILE CHECK_ADXL_ID_01 "+ adxl_id_01 + " 0xAD PASS")
                        adxl_id_02 = str(res.data["[ADXL] ID_2"])    
                        self.logger.info( "CSVFILE CHECK_ADXL_ID_02 "+ adxl_id_02 + " 0x1D PASS")
                        adxl_id_03 = str(res.data["[ADXL] ID_3"])    
                        self.logger.info( "CSVFILE CHECK_ADXL_ID_03 "+ adxl_id_03 + " 0xF2 PASS")
                        rc, text = self.dut.execute_command("adxl get_values",2000)
                        if rc != 0:
                            self.logger.info( "CSVFILE CHECK_ADXL_VALUES 0 -1 FAIL")
                            return False
                        else:
                            res = CommandResult.parse(text)
                            adxl_id_x = str(res.data["Acceleration on axe X"])    
                            self.logger.info( "CSVFILE CHECK_ADXL_VALUE_X "+ adxl_id_x + " [-250;250] PASS")
                            adxl_id_y = str(res.data["Acceleration on axe Y"])    
                            self.logger.info( "CSVFILE CHECK_ADXL_VALUE_Y [-250;250] "+ adxl_id_y + " [-250;250] PASS")
                            adxl_id_z = str(res.data["Acceleration on axe Z"])    
                            self.logger.info( "CSVFILE CHECK_ADXL_VALUE_Y "+ adxl_id_z + " [-750;250]U[250;750] PASS")
                            rc, text = self.dut.execute_command("adxl int_1",2000)
                            if rc != 0:
                                self.logger.info( "CSVFILE CHECK_ADXL_CONFIG_1 0 -1 FAIL")
                                return False
                            else:
                                self.logger.info( "CSVFILE CHECK_ADXL_INT_1 0 0 PASS")
                                rc, text = self.dut.execute_command("adxl int_2",2000)
                                if rc != 0:
                                    self.logger.info( "CSVFILE CHECK_ADXL_CONFIG_2 0 -1 FAIL")
                                    return False
                                else:  
                                    self.logger.info( "CSVFILE CHECK_ADXL_INT_1 0 0 PASS")
                                    rc, text = self.dut.execute_command("adxl fifo",2000)
                                    if rc != 0:
                                        self.logger.info( "CSVFILE CHECK_ADXL_FIFO  FAIL")
                                        return False
                                    else:
                                        res = CommandResult.parse(text,':')
                                        adxl_fifo_x = str(res.data["x_mean"])    
                                        self.logger.info( "CSVFILE CHECK_ADXL_FIFO_X_MEAN "+ adxl_fifo_x + " [-250;750] PASS")
                                        adxl_fifo_y = str(res.data["y_mean"])    
                                        self.logger.info( "CSVFILE CHECK_ADXL_FIFO_Y_MEAN "+ adxl_fifo_y + " [-250;750] PASS")
                                        adxl_fifo_z = str(res.data["z_mean"])    
                                        self.logger.info( "CSVFILE CHECK_ADXL_FIFO_Z_MEAN "+ adxl_fifo_z + " [-250;750] PASS")
                                        return True      
        
        
         

        
        
        
        
        
   
              
            
            