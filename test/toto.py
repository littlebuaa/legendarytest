"""T30 station (semi-finished product test)"""

import sys
sys.path.insert(0,'../')
from framework.tools.device import Zoovstation as Zoov
import framework.tools.utils as TOOL
from framework.common import *
from framework.tools.config import configget
from framework.tools import logger as logtool



def main():
    """Define code in main to avoid execution if it is imported."""
    ######################  init test       ######################
    time_begin = TOOL.init_test()
    test_result = True
    ######################  create log handler  ######################
    log_file_name = logtool.log_name_gen("txt", "FFFFFFFFFFFF")
    logtool.init_logger(log_file_name)

    ######################  ready to power on   ######################
    print("Power on the device under test, then press ENTER to continue...")
    input()
    ######################  create DUT          ######################
    comport = configget("COM", "zoovstation")
    print(comport)
    dut = Zoov(comport)
    if not dut.open():
        print("ERROR","Failed to open COM port!")
        exit()
    ######################  create test sequence ######################
    dut.execute_command('version')
    TOOL.flush_input()

    """     tests = [
        Reset(dut),
        WaitShell(dut),
    ] """

    ######################      RUN the test     ######################
    """     for test in tests:
        if not test.run():
            test_result = False
            break """

    ######################      Closing          ######################
    # dut.close()
    TOOL.flush_input()
    csvinfo = logtool.get_csv_info(test_result, "FFFFFFFFFFFF", time_begin)
    logtool.csvmaker(log_file_name, csvinfo)
    TOOL.show_result(test_result)

if __name__ == "__main__":
    main()
