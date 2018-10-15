from framework.common.testing import Test
from framework.tools.device import CommandResult
from framework.tools.config import configget

class Personalization(Test):
    def __init__(self, dut):
        super().__init__(dut, "Personalization")
        
    def test(self):
        '''This function is to set the MFGID, ws_target, Pubkey, for the DUT'''
        perso_dic = {
                "set_mfgid" : configget("PERSO","MFG_ID").upper(),
                "set_wstarget" : configget("PERSO","wstarget"),
                 "set_pubkey"    : configget("PERSO","pubkey")
                }
        feuvert =  True
        for key,value in perso_dic.items():
            try:
                rt,text = self.dut.execute_command("perso %s %s"%(key,value),20000)
                res = CommandResult.parse(text)
                if res.rc !=0:
                    self.logger.info("CSVFILE Personalization ok %s fail"%key)
                    return False
            except:
                self.logger.info("Exception occurs during Personalization!!")
                self.logger.info("CSVFILE Personalization ok %s fail"%key)
                feuvert =  False
        if feuvert:
            self.logger.info("CSVFILE Personalization ok ok pass")
            return True
        else:
            self.logger.info("CSVFILE Personalization ok ng fail")
            return False