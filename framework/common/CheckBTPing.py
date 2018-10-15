from framework.common.testing import Test
from framework.tools.device import CommandResult,DUT

class CheckBTPing(Test):
    def __init__(self, dut):
        super().__init__(dut, "Check BT Ping")
    
    def test(self):
        ''' This function is to proceed bt ping test, a Ref golden sample is a must to serve as the BT server.'''
        ref_com =  configget("COM","REF")
        ref = DUT("ref",ref_com)
        if not ref.open():
            self.logger.info("Drive board UART Problem, COM port open failed!!")
            return False
        mac_ref = ref.get_mac()
        temp = hex(int(mac_ref[-2:], 16) + 1)
        mac_ref_bt = mac_ref[:-2] + temp[-2:]
        ref.send_command("bt listen")

        rc, text = self.dut.execute_command("bt up 2")
        rc, text = self.dut.execute_command("bt l2ping %s 5"%mac_ref_bt)
        s = text.splitlines()
        for line in s:
            x = line.split(" ")
            if len(x) ==4:
                try:
                    y = int(x[2].lstrip())
                    if y> 0:
                        self.logger.info( "CSVFILE bt_ping %d [0;2000] pass"%(y))
                        return True
                except:
                    continue
        self.logger.info( "CSVFILE bt_ping no_data [0;3000] fail")
        return False
