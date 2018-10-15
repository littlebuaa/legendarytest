"""T30 station (semi-finished product test)"""

from framework.tools.device import DUT
import framework.tools.utils as TOOL
from framework.common import *
from framework.tools.config import configget
from framework.tools import logger as logtool



def main():
    """Define code in main to avoid execution if it is imported."""
    ######################  init test       ######################
    time_begin = TOOL.init_test()
    test_result = True
    ######################  scan MAC address    ######################
    mac_scan = TOOL.scan_mac("Please scan the MAC label:")

    ######################  create log handler  ######################
    log_file_name = logtool.log_name_gen("txt", mac_scan)
    logtool.init_logger(log_file_name)

    ######################  ready to power on   ######################
    print("Power on the device under test, then press ENTER to continue...")
    input()
    ######################  create DUT          ######################
    dut = DUT("DUT", configget("COM", "dut"))
    if not dut.open():
        print("ERROR","Failed to open COM port!")
        exit()
    ######################  create test sequence ######################
    TOOL.flush_input()

    tests = [
        Reset(dut),
        WaitShell(dut),
        # CheckWiFiPER(dut)
        # CheckMicrophone(dut)
    ]

    ######################      RUN the test     ######################
    for test in tests:
        if not test.run():
            test_result = False
            break

    ######################      Closing          ######################
    dut.close()
    TOOL.flush_input()
    csvinfo = logtool.get_csv_info(test_result, mac_scan, time_begin)
    logtool.csvmaker(log_file_name, csvinfo)
    TOOL.show_result(test_result)

if __name__ == "__main__":
    main()
