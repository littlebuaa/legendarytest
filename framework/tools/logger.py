#! /usr/bin/python3
# -*- coding:utf-8 -*-

import logging
from .config import configget,configset
import os
import time
import shutil
import filecmp
import csv


def init_logger(log_name):
    global global_logger
    ## remove all the old logging handlers 
    handler_list = logging.getLogger().handlers
    print(handler_list)
    if len(handler_list)==0:
        print("ooooooooooooooooooooooooooooooooooooooooooooo")
        pass
    else:
        print("============================================")
        for handler in handler_list[:]:  # make a copy of the list, attention: change/remove things in list while iteration
                global_logger.removeHandler(handler)
                print("xxxxxxxxxxxxxxxxxxxxxxxxxxx")

    global_logger = logging.getLogger()
    global_logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(log_name)
    fmt = '%(asctime)s %(name)s %(levelname)s %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    global_logger.addHandler(fh)

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(asctime)s %(name)-8s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    global_logger.addHandler(console)
    console = None
    formatter = None

    return log_name

def log_name_gen(logtype, mac_label):
    try:
        project = configget("INFO", "PROJECT")
        factory = configget("INFO", "FACTORY")
        stationName = configget("TEST_STATION", "STATION_NAME")
        stationNumber = configget("TEST_STATION", "STATION_NUMBER")
        current_path_txt = configget("TEST_STATION", "LOCAL_LOG") + os.sep + "text"
        current_path_csv = configget("TEST_STATION", "LOCAL_LOG") + os.sep + "csv"
    except:
        print("No config file, or simple test no need!")
        project = ""
        factory = "withings"
        stationName = "myPC"
        stationNumber = "1"
        current_path_txt = "./txt_log"
        current_path_csv = "./csv_log"

    full_station_name = stationName+ "_" + stationNumber
    day = time.strftime("20%y%m%d", time.localtime())
    shift_time = int(time.time())


    if not os.path.exists(current_path_txt):
        try:
            os.makedirs(current_path_txt)
            print("new Local TXT Log folder Created!")
        except:
            print("\n Error! Unable to creat Local TXT log folder")
            raise
    if not os.path.exists(current_path_csv):
        try:
            os.makedirs(current_path_csv)
            print("new Local CSV Log folder Created!")
        except:
            print("\n Error! Unable to creat Local CSV log folder")
            raise

    if logtype == 'txt':
        log_time = time.strftime("20%y%m%d_%H%M%S",time.localtime(shift_time))
        path__ = current_path_txt + os.sep + day
        if not os.path.exists(path__):
            try:
                os.makedirs(path__)
                print("new Local Log Date folder Created!")
            except:
                print("\n Error! Unable to creat Local Date log folder")
                raise
        textlogname = project+ '_' +factory +'_log_' + full_station_name + '_' + log_time + '_' + mac_label.replace(":","")
        txt_logname = path__ + os.sep + textlogname + '.log'
        print(txt_logname)
        return txt_logname

    else:
        path__ = current_path_csv + os.sep + day
        if not os.path.exists(path__):
            try:
                os.makedirs(path__)
                print("new Local CSV Date folder Created!")
            except:
                print("\n Error! Unable to creat Local CSV Date folder")
                raise
        ################################   Shift and Day  #########################
        shift_last_time = int(configget("INFO","LAST_CSV_CREATE_TIME_SEC"))
        csv_create_interval = int(configget("INFO","CSV_CREATE_INTERVAL_MINUTE"))*60

        last_shift = time.strftime("%H%M%S",time.localtime(shift_last_time))
        last_csv_date = time.strftime("20%y%m%d",time.localtime(shift_last_time))
        last_path = configget("TEST_STATION","LOCAL_LOG") + os.sep + "csv" + os.sep + last_csv_date
        last_samba = configget("TEST_STATION","REMOTE_SERVER") + os.sep + last_csv_date
        last_logname =  project+ '_' +factory +'_log_' + full_station_name + '_' + last_csv_date + '_' + last_shift

        ## compare the time stamp
        if (shift_time - shift_last_time) > csv_create_interval:
            ##  change old wip to csv and copy it to samba
            if os.path.exists(last_path + os.sep + last_logname+".csv.wip"):
                os.renames(last_path+os.sep+last_logname+".csv.wip", last_path+os.sep+last_logname+".csv") # change .csv.wip to .csv
                copy_to_samba(last_path, last_samba, last_logname+".csv")  ## copy .csv to samba_to_upload

            ## Prepare new csv wip file
            shift = time.strftime("%H%M%S",time.localtime(shift_time))		# new csv with %H%M%S
            new_date = time.strftime("20%y%m%d",time.localtime(shift_time))
            logname = project+ '_' +factory +'_log_' + full_station_name + '_' + new_date + '_' + shift + ".csv.wip"
            csv_logname = path__ + os.sep + logname

            ## write new time stamp to config file
            configset("INFO","LAST_CSV_CREATE_TIME_SEC",str(shift_time))
        else:
            ## keep writing data to old file, in old folder
            logname = last_logname + ".csv.wip"
            csv_logname = last_path + os.sep + logname
        return csv_logname




def csvmaker(log_name, csvinfo):
    with open(log_name,"r") as f:
        lines = f.readlines()
    test_item = []
    test_qty_proceeded = 0
    for line in lines:
        line = line.replace("\r","")
        line = line.replace("\n","")
        #print("csv line raw: " + line)
        if line.find("CSVFILE") != -1:
            test_list = line.split(" ")
            inde = test_list.index("CSVFILE")
            test_list = test_list[(inde+1):]
            tmp = [test_list[0],test_list[2],test_list[1],test_list[3]]
            test_item  += tmp
            test_qty_proceeded += 1

    csvline = csvinfo[1] + test_item
    stationName = configget("TEST_STATION","STATION_NAME")
    today = time.strftime("20%y%m%d",time.localtime())
    # csv_path ="Flex_%s_%s.csv"%(stationName,today)
    csv_path = log_name_gen("csv", None)
    file_exist = os.path.exists(csv_path)
    with open(csv_path, "a",newline='') as f:
        csvwriter = csv.writer(f, delimiter=',',quoting=csv.QUOTE_MINIMAL)
        ## check new csv file, if yes, need write header
        if not file_exist :
            print("new write header")
            csv_header = csvinfo[0] + ["test_item", "value","range","result"]*test_qty_proceeded
            csvwriter.writerow(csv_header)
        ## write csv item
        csvwriter.writerow(csvline)
    return 0

def get_csv_info(status, mac_label, time_begin):
    mac_label_ = mac_label.replace(":","").lower() #avoid making error during creating the log file

    #get station name info
    stationName = configget("TEST_STATION","STATION_NAME")
    stationNumber = configget("TEST_STATION","STATION_NUMBER")
    full_station_name = stationName+ "_" + stationNumber
    test_version = configget("TEST_STATION","TEST_VERSION")

    #get local time
    time_log = time.strftime("20%y%m%d_%H%M%S",time.localtime())
    # microsecond = datetime.now().microsecond
    time_end = time.time()
    time_total = round((time_end - time_begin),2)
    time_begin_= time.strftime("20%y%m%dt%H%M%S",time.localtime(time_begin))
    day = time.strftime("20%y%m%d",time.localtime())
    today = time.strftime("20%y%m%d",time.localtime())

    factory = configget("INFO","FACTORY")
    project = configget("INFO","PROJECT") #PROJECT values: 'ws30','ws50','hwa01'

    #get dut info
    #for info: mac_label = mac_label_ #20141215:changed from mac_dut to mac_lable. In order to adapt to platform requirement.

    #standard: model,station,station number,program version,mac,start time,duration,station result | test item,value,range,result
    #csvinfo = "CSVINFO MP " + project_name + " " + stationName + " " + station_version + " " +  mac_label + " " + dut_secret + " " + dut_mfgid + " " + dut_bootloader_version + " " + dut_firmware_version + " " + time_begin_ + " " + str(time_total) + " final_" + station_result + "\r\n"
    #script: model | station | station number | program version | mac | secret | mfgid | bl version | fw version | start time | duration | station result
    csv_title = "model,station,station number,program version,mac,mfgid,bl version,fw version,start time,duration,station result"
    station_result = "PASS" if status else "FAIL"
    csv_header = ["PROJECT","STATION_NAME","STATION_NUMBER","TEST_VERSION","MAC","TIME_BEGIN","DURATION","RESULT"]
    csv_fix_column =[project, stationName, stationNumber, test_version, mac_label, time_begin_, str(time_total), station_result]
    return (csv_header, csv_fix_column)

def copy_to_samba(src,dst,file):
    if not os.path.exists(dst):
        try:
            os.makedirs(dst)
            print("New Samba Log Folder Created!")
        except:
            print("Error! Unable to creat samba log folder")
            raise
    good_copy = False
    copy_count = 0
    while(not good_copy):
        if copy_count> 3:
            print("Sever connection problem!!!!! check the network!!")
            raise
        src_file = src + os.sep + file
        dst_file = dst + os.sep + file
        shutil.copy(src_file, dst_file)
        copy_count +=1
        if filecmp.cmp(src_file,dst_file):
            good_copy = True
            print("File copy to server by %d time!!"% copy_count)

