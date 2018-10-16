#! /usr/bin/python3
# -*- coding:utf-8 -*-


from colorama import init
from colorama import Fore, Back, Style
import time,sys
import re
import sys
import logging

pass_art = """
 .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. |
| |   ______     | || |      __      | || |    _______   | || |    _______   | |
| |  |_   __ \   | || |     /  \     | || |   /  ___  |  | || |   /  ___  |  | |
| |    | |__) |  | || |    / /\ \    | || |  |  (__ \_|  | || |  |  (__ \_|  | |
| |    |  ___/   | || |   / ____ \   | || |   '.___`-.   | || |   '.___`-.   | |
| |   _| |_      | || | _/ /    \ \_ | || |  |`\____) |  | || |  |`\____) |  | |
| |  |_____|     | || ||____|  |____|| || |  |_______.'  | || |  |_______.'  | |
| |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------' 
"""
fail_art = """
 .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. |
| |  _________   | || |      __      | || |     _____    | || |   _____      | |
| | |_   ___  |  | || |     /  \     | || |    |_   _|   | || |  |_   _|     | |
| |   | |_  \_|  | || |    / /\ \    | || |      | |     | || |    | |       | |
| |   |  _|      | || |   / ____ \   | || |      | |     | || |    | |   _   | |
| |  _| |_       | || | _/ /    \ \_ | || |     _| |_    | || |   _| |__/ |  | |
| | |_____|      | || ||____|  |____|| || |    |_____|   | || |  |________|  | |
| |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------' 
"""
pass_ = """
########     ###     ######   ######  
##     ##   ## ##   ##    ## ##    ## 
##     ##  ##   ##  ##       ##       
########  ##     ##  ######   ######  
##        #########       ##       ## 
##        ##     ## ##    ## ##    ## 
##        ##     ##  ######   ######  
"""
fail_ = """
########    ###      ####   ##       
##         ## ##      ##    ##       
##        ##   ##     ##    ##       
######   ##     ##    ##    ##       
##       #########    ##    ##       
##       ##     ##    ##    ##       
##       ##     ##   ####   ######## 
"""



def init_test():
    init()
    time_begin = time.time()
    return time_begin


def colorprint(text,back_color="RED",fore_color="WHITE"):
    f_fore = Fore.__dict__[fore_color]
    f_back = Back.__dict__[back_color]

    print(f_fore + f_back + Style.BRIGHT + text)
    print(Fore.RESET + Back.RESET + Style.RESET_ALL)

    
def question_timeout(question,timeout_sec):
    import msvcrt
    '''#input:
    - question: target question to ask
    - timeout: timeout in second. if no input within timeout, then return True
        output:
    - answer: input from keyboard
    - timeout: If no answer with timeout then'''
    key_timeout = True
    keyboard_str = ""
    times = 100
    loop = timeout_sec*times
    while(loop>=0):
        line = question  + " -- Timeout: %s seconds:  %s"%(str(int(loop/times)),keyboard_str)
        sys.stdout.write(line)
        sys.stdout.flush()
        time.sleep(1/times) #wait for 1/times second
        while msvcrt.kbhit():
            curr = msvcrt.getch().decode("ascii","ignore")
            if curr == "\b":#if want to delete the previous character
                sys.stdout.write("\r")
                sys.stdout.flush()
                sys.stdout.write(" "*(len(line)))
                sys.stdout.flush()
                keyboard_str = keyboard_str[0:-1] #remove last character
            else:
                keyboard_str += curr
        sys.stdout.write("\r")
        sys.stdout.flush()
        if keyboard_str == "" or keyboard_str.find("\r") == -1:
            loop = loop -1
            continue
        else:
            print(keyboard_str)
            key_timeout = True
            break
    print()
    return(key_timeout,keyboard_str)

## to share MAC label as global variable outside this file 


def scan_mac(msg):
    #scan mac from mac label
    timeout = 180
    colorprint(msg)
    timeout,mac_input = question_timeout("",timeout)#timeout 180 seconds if no input
    if timeout:
        mac_label = "mac_none" # default value for bad input
        return(mac_label)
    else:
        return(check_mac_valid(mac_input))


def check_mac_valid(mac_input):
    mac_input = mac_input.replace(":","")
    mac_input = mac_input.strip()
    mac_input = mac_input.lower()
    return mac_input if re.match("^0024e4([0-9a-f]){6}$", mac_input) else "mac_none"

def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

def show_result(result):
    if result:
        colorprint(pass_, "GREEN")
    else:

        colorprint(fail_art, "RED")

def compare_value(item,target,minvalue,maxvalue):
    ''' return 0 if 	 : minvalue <= target <= maxvalue
        return -1 if not : minvalue <= target <= maxvalue
        generate CSVFILE info:  item + range + value + result
        input is:
                1) the name of item
                2) value to compare
                3) minvalue
                4) maxvalue'''
    target = float(target)
    minvalue = float(minvalue)
    maxvalue = float(maxvalue)
    global_logger = logging.getLogger()
    if(target >= minvalue)and(target <= maxvalue):
        global_logger.info("CSVFILE %s [%.2f;%.2f] %.3f pass"%(item,minvalue,maxvalue,target))
        return 0
    else:
        global_logger.info( "CSVFILE %s [%.2f;%.2f] %.3f fail"%(item,minvalue,maxvalue,target))
        return -1


def check_value_in(target,source,separator):
    '''#this function will check if target string value is in source string \
    if yes, return True, else return False\
    mainly to check whether in the config file, multi-value '''
    key_exist = False
    source_l = source.split(separator)
    for item in source_l:
        if target == item:
            key_exist = True
            break
    return key_exist
