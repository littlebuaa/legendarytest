#! /usr/bin/python3
# -*- coding:utf-8 -*-


try:
    import configparser as CP
except:
    import ConfigParser as CP

config = None

# Find hardcoded information within the config.ini file
# Store the configuration in a global variable. Use _reload to
# force a rereading of the config file.
#
# Input:
#   - section : EINK,WSB,...
#   - key : str of piece of information wanted
#------------------------------------------------------------

import platform
osystem = platform.system()
if osystem == "Windows":
    default_config = "./config.ini"
else:
    import getpass
    default_config = '/home/{}/config.ini'.format(getpass.getuser())


def configget(section, key=None, _reload = False,configfile = default_config):
    global config

    if config is None or _reload:
        config = CP.ConfigParser()
        try:
            with open(configfile,'r') as cfg:
                config.readfp(cfg)
        except IOError as error:
            print("No Config file found!!")
            return -1

    if key is None:
        return [ [option, config.get(section, option)] for option in config.options(section) ]

    else:
        return config.get(section,key, fallback = -1)


def configset(section,key,value, _reload = False,configfile = default_config):
    global config

    if config is None or _reload:
        config = CP.ConfigParser()
        config.optionform = str
        try:
            with open(configfile,'r') as cfg:
                config.readfp(cfg)
        except IOError as error:
            print("No Config file found!!")

    config.set(section,key,value)

    with open(configfile,'w') as cfg:
        config.write(cfg, space_around_delimiters=False)
