from framework.common.testing import Test
from framework.tools.device import CommandResult


class CheckLightsensorTest(Test):
    def __init__(self, dut):
        super().__init__(dut, "check light sensor")

    def test(self):
        rc, text = self.dut.execute_command("light_sensor request",2000)
        if rc != 0:
            self.logger.info( "CSVFILE LIGHT_SENSOR_REQUEST 0 -1 FAIL")
            return False
        else:
            self.logger.info( "CSVFILE LIGHT_SENSOR_REQUEST 0 0 PASS")
            rc, text = self.dut.execute_command("light_sensor get",2000)
            if rc != 0:
                self.logger.info( "CSVFILE VALUE_LIGHT_OFF 0 -1 FAIL")
                return False
            else:
                res = CommandResult.parse(text)
                light_value = str(res.data["value"])    
                self.logger.info( "CSVFILE VALUE_LIGHT_OFF "+ light_value + " [0;4000] PASS")
                while True : 
                    answer = input("Please switch on the light and press ENTER when done:")
                    if not answer:
                        break
                time.sleep(2)
                rc, text = self.dut.execute_command("light_sensor get",2000)
                if rc != 0:
                    self.logger.info( "CSVFILE VALUE_LIGHT_ON 0 -1 FAIL")
                    return False
                else:
                    res_on = CommandResult.parse(text)
                    light_value_on = str(res.data["value"])    
                    self.logger.info( "CSVFILE VALUE_LIGHT_ON "+ light_value_on + " [0;4000] PASS")
                    rc, text = self.dut.execute_command("light_sensor release",2000)
                    if rc != 0:
                        self.logger.info( "CSVFILE LIGHT_SENSOR_RELEASE 0 -1 FAIL")
                        return False
                    else:
                        self.logger.info( "CSVFILE LIGHT_SENSOR_RELEASE 0 0 PASS")
                        print("Please switch of the light")
                        time.sleep(2)
                        return True 
                
