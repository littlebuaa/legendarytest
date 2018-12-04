from framework.common.testing import Test
from framework.tools.device import CommandResult
from framework.tools.utils import colorprint,question_box
import os
import locale



class CheckCableConduct(Test):
    def __init__(self, dut):
        super().__init__(dut, "Check conductivity of the cable")

    def test(self): 
        msg = "                                                         \n" + \
              "Please Use Multimter to Bipbip check the Following Points\n" + \
              "CAN EXTERNAL HIGH    CAN EXTERNAL LOW\n"+ \
              "BRAKE LEFT and RIGHT\n" + \
              "STACK_NEXT_BIKE_DETECT\n" + \
              "                                                         \n"

        colorprint(msg,"YELLOW")
        input()

        msg = "Is all Right, Did you hear all the DiDi?? Yes/No? " 
        if question_box(msg):
            self.logger.info( "CSVFILE cable_soudering ok ok pass")
            return True
        self.logger.info( "CSVFILE cable_soldering ok fail fail")
        return False
