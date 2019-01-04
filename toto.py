# -*- coding: utf-8 -*-

import sys
sys.path.insert(0,'../../')
from framework.tools.device import Zoovstation as Zoov
import framework.tools.utils as TOOL
from framework.zoov import *
from framework.tools.config import configget
from framework.tools import logger as logtool
from framework.tools.utils import ENCODING, get_encoding


def print_test_summary(oklist, nglist):
    ''' list all the result of test items'''
    print('\n\n')
    print('{:#^80}\n'.format("   Summary   "))
    for item in oklist:
        if item.__class__.__name__ == "ExecuteCommand":
            name = TOOL.colortext(item.command, "RED")
        else:
            name = TOOL.colortext(item.__class__.__name__, "GREEN")
        res = TOOL.colortext('PASS', "GREEN")
        txtprint = "{:50}:\t{}".format(name,res)
        print(txtprint)
    print('{:<80}'.format("---------------------------------"))
    for item in nglist:
        if item.__class__.__name__ == "ExecuteCommand":
            name = TOOL.colortext(item.command, "RED")
        else:
            name = TOOL.colortext(item.__class__.__name__, "RED")
        res = TOOL.colortext('FAIL', "RED")
        txtprint = "{:50}:\t{}".format(name,res)
        print(txtprint)
    print('\n')
    print('{:#^80}\n'.format("   End of Summary   "))


def main (isProd = True):
    """Define code in main to avoid execution if it is imported."""
    ######################  init test       ######################
    time_begin = TOOL.init_test()
    test_result = True

    ######################  create log handler  ######################
    serialID = TOOL.scan_serial_id("請掃描或輸入車身QR二維碼，Please scan the bike QR code:")

    log_file_name = logtool.log_name_gen("txt", serialID)
    logtool.init_logger(log_file_name)

    ######################  create DUT          ######################
    comport = configget("COM", "zoovstation")
    print(comport, serialID)
    dut = Zoov(comport,serialID)
    if not dut.open():
        print("ERROR","Failed to open COM port!")
        exit()
    ######################  create test sequence ######################

    TOOL.flush_input()

    tests = [
        WaitShellConnect(dut),
        # CheckBoardID_A100(dut),
        # SetSerialID(dut),
        # CheckBrake(dut),
        # CheckBatteryDetect(dut),
        CheckPowerLED(dut),
        # ExecuteCommand(dut,'low_power_check'),
        # CheckLight(dut),
        # ExecuteCommand(dut,'torque_calibration'),
        # MotorCalibration(dut),
        # ExecuteCommand(dut,"factory_mode_set --mode 3"),
        # ExecuteCommand(dut,"reboot")
		SetGateway(dut),
    ]

    ######################      RUN the test     ######################
    ## Production mode and Dianostic mode
    if isProd:
        for test in tests:
            if not test.run():
                test_result = False
                break
    else:
        oklist =[]
        nglist = []
        for test in tests:
            if not test.run():
                nglist.append(test)
            else:
                oklist.append(test)
        if len(nglist) != 0:
            test_result = False

    ######################      Closing          ######################
    # dut.close()
    TOOL.flush_input()
    csvinfo = logtool.get_csv_info(test_result, serialID, time_begin)
    logtool.csvmaker(log_file_name, csvinfo)


    ######################      Display Result    #####################
    TOOL.show_result(test_result,pop = isProd)
    if not isProd:
        print_test_summary(oklist, nglist)



if __name__ == "__main__":
    main()
