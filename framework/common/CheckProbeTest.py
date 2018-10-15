from framework.common.testing import Test
from framework.tools.device import CommandResult
from framework.tools.config import configget

class CheckProbeTest(Test):
    def __init__(self, dut):
        super().__init__(dut, "check probe")

    def test(self): 
        rc, text = self.dut.execute_command("probe")
        res_data = CommandResult.parse(text)
        list_check = ["mfg_id",
                      "bl_version",
                      "soft_version",
                      "mac",
                      "mcu_id",
                      "secret"]

        for item in list_check:
            try:
                oitem = configget("PERSO", item).strip()
            except:
                oitem = None
            if item in res_data.data:
                item_value = res_data.data[item]
                self.dut.prop[item] = item_value
                if oitem:
                    if item_value.lower() == oitem.lower():
                        self.logger.info( "CSVFILE probe_%s_checking "%item + oitem + " " + item_value + " pass")
                    else:
                        self.logger.info( "CSVFILE probe_%s_checking "%item + oitem + " " + item_value + " fail")
                        return False # value unexpected
                else:
                    self.logger.info( "CSVFILE probe_%s_checking not_in_config "%item  + item_value + " pass")
            else:
                self.logger.info( "CSVFILE probe_%s_checking not_in_probe_data "%item  + "not_in_probe_data" + " fail")
                return False

        return True
