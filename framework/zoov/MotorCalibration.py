from framework.common.testing import Test
from framework.tools.config import configget
from framework.tools.utils import colorprint, op_messager, get_encoding



class MotorCalibration(Test):
    def __init__(self, dut):
        super().__init__(dut, "Do Motor Calibration test")
        ENCODING = get_encoding()
        if ENCODING == 1 or ENCODING == 2:
            # Language setting
            self.message = (
                "馬達校準測試，按Enter繼續",
            )
        else:
            self.message = (
                "Motor Calibration, Press ENTER to begin: pay attention to hold the motor",
            )

    def test(self):
        '''To run the motor calibration test'''
        message = self.message
        op_messager(message[0])
        
        cmd_set = "motor_calibration"
        r,text_ = self.dut.execute_command(cmd_set,70000)
        if r != 0:
            self.logger.info( "CSVFILE Motor_Calibration ok ng fail")
            return False
        else:
            self.logger.info( "CSVFILE Motor_Calibration ok ok pass")
            return True
