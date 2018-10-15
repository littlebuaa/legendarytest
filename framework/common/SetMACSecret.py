from framework.common.testing import Test
from framework.tools.config import configget


class SetMACSecret(Test):
    def __init__(self, dut):
        super().__init__(dut, "Set MAC and Secret")
        
    def test(self):
        ''' This function is to set MAC and the secret'''
        ''' Global MAC_label must be valide'''
        mac_input=  self.dut.prop["mac_label"] ## Global MAC_label
        MAC_label = mac_input[:2]+":"+ mac_input[2:4]+":"+ mac_input[4:6]+":"+ mac_input[6:8]+":"+ mac_input[8:10]+":"+ mac_input[10:12]
        rc1,text = self.dut.execute_command("perso erase_all_settings",4000)
        rc1,text = self.dut.execute_command("trace off",4000)
        mac_file = configget("PERSO","MAC_FILE")
        secret = ""
        ## read mac file, search for secret
        with open(mac_file,"r") as f:
            temp = f.readlines()
        for line in temp:
            if MAC_label in line:
                secret = line.split('\t')[1]
        if not secret:
            self.logger.debug("This MAC %s is not in the file!!"%MAC_label)
            self.logger.info("CSVFILE set_mac_secret ok no_secret fail")
            return False
        else:
            self.logger.debug("The MAC is %s, and the secret has been found!!"%MAC_label)
            rc1,text = self.dut.execute_command("perso %s %s"%("set_mac",MAC_label),5000)
            rc2,text = self.dut.execute_command("perso %s %s"%("set_secret",secret),5000)
            if rc1 != 0 or rc2 != 0:
                self.logger.info("CSVFILE set_mac_secret ok NG fail")
                return False
            else:
                self.logger.info("CSVFILE set_mac_secret ok ok pass")
                return True