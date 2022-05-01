info = '''
#========================================================================================#
title               :TerminalControllerAPI
description         :Library for controlling Terminal Controller via python.
author              :Chris Nance
date                :2022-05-01
version             :1.0
usage               :import TerminalControllerAPI
notes               :visit https://github.com/christopher-nance/ARM-Plan-Automation
python_version      :3.10
#========================================================================================#
'''

##############################################################
################## MODULES & DICTIONARIES ####################
##############################################################

import mouse, keyboard
from colorama import Fore, init
init(convert=True)
import pandas as pd
from time import sleep
import clipboard as cb


keystrokeDictionary = {

    '''
    This dictionary houses all the 'Hot Keys' or 'Key Shortcuts' (in SiteManager) and links
    them to proper descriptions of the button. Please ensure that the screen called
    '2022 Python Screen' is properly setup and if any changes need to be made they shopuld
    be done in this script, NOT in SiteManager. 

    '''


    'FastPass_Lite':        ['Alt', 'a'], # Lite FastPass
    'FastPass_Starter':     ['Alt', 'b'], # Starter FastPass
    'FastPass_Pro':         ['Alt', 'c'], # Pro FastPass
    'FastPass_Legend':      ['Alt', 'd'], # Legend FastPass

    'FindAccount_Name':     ['Alt', 'e'], # Find Account with Search Name (Last,First)
    'FindAccount_FPcode':   ['Alt', 'f'], # Find Account with FastPass Number
    'FindAccount_PCcode':   ['Alt', 'g'], # Find Account with PC Code
    'FindAccount_CC':       ['Alt', 'h'], # Find Account with Credit Card Number
    'FastPass_Phone':       ['Alt', 'i'], # Find Account with Phone Number

    'Tender_ARM_CC':        ['Alt', 'j'], # Tender Current Sale w/ ARM CC on File
    'Tender_Cash':          ['Alt', 'k'], # Tender Current Sale w/ CASH

    'Discontinue':          ['Alt', 'l'], # Add 'Discontinue' item to the current sale
    'Terminate':            ['Alt', 'm'], # Add 'Terminate' item to the current sale
    'Switch':               ['Alt', 'n'], # Add 'Switch' item to the current sale

    'OneTimeMsg_Enable':    ['Alt', 'o'], # Enable the one-time message to show up for the customer. 
    'OneTimeMsg_Disable':   ['Alt', 'p'], # Disable the one-time message to show up for the customer. (This should not be used, the customer will disable it via transitions in SiteManager)

    'OpenNewSale':          ['Alt', 'q'], # Opens a new sale
    'ReleaseSale':          ['Alt', 'r'], # Releases the current sale

    'ARMContract':          ['Alt', 's'], # Prints the ARM Contract for the current customer

}


##############################################################
################### CONTROLLER  FUNCTIONS ####################
##############################################################

def ETA(total_passes, progress, time_per_customer):
    seconds = ((total_passes-progress)*time_per_customer) % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d Hours %02d Minutes %02d Seconds" % (hour, minutes, seconds)
    
def convertFPN(FPN):
    splitStr = FPN.split('+')
    if len(splitStr) == 2:
        returnableStr = splitStr[0]+splitStr[1]
        return returnableStr
    else:
        splitStr = FPN.split('-')
        returnableStr = splitStr[0]+splitStr[1]
        return returnableStr

def validate_input(file):
    try:
        dataframe = pd.read_csv(file)
        for index, row in dataframe.iterrows():
            try:
                customerCodeTest = row['CustomerCode']
            except:
                return [False, None]
        return [True, pd.read_csv(file)]
    except UnicodeDecodeError:
        print("Validation error")
        return [False, None]
    except FileNotFoundError:
        print("Validation error")
        return [False, None]
    except Exception:
        print("Validation error")
        return [False, None]



##############################################################
############# TERMINAL CONTROLLER API FUNCTIONS ##############
##############################################################
'''
Instructions: 
Import this module using: import TerminalControllerAPI
After the module is imported you may use any of the following functions: 

Name: openNewSale()
Args: none
Desc: Opens a new sale

Name: lookupAccount(customerCode)
Args: <str:customerCode - FastPass number to lookup> 
Desc: Looks up the account associated with the FastPass number <customerCode> 

Name: enableOneTimeMessage(customerCode)
Args: Pass the same argument as you did for lookupAccount
Desc: Turns on the one-time message club plan for the account that is looked up.

Name: ETA(total_passes, progress, time_per_customer)
Args: <num:total_passes total customers that will be iterated>; <num:progress number of customers already iterated through (usually the index)>; <num:time_per_customer amount of time per customer for each function>
Desc: Turns on the one-time message club plan for the account that is looked up.




'''

def openNewSale():
    keyboard.press(keystrokeDictionary['OpenNewSale'][0])
    keyboard.press(keystrokeDictionary['OpenNewSale'][1])
    sleep(0.5)
    keyboard.press(keystrokeDictionary['OpenNewSale'][0])
    keyboard.press(keystrokeDictionary['OpenNewSale'][1])
    sleep(0.5)

def lookupAccount(customerCode):
    if customerCode == False:
        print(Fore.RED + "[SKIPPING]\t account with code:", str(customerCode) + Fore.RESET)  
    else:
        print(Fore.LIGHTBLUE_EX + "[LOADING]\t Account with code:", customerCode + Fore.RESET)
        openNewSale()
        keyboard.press(keystrokeDictionary['FindAccount_FPcode'][0])
        keyboard.press(keystrokeDictionary['FindAccount_FPcode'][1])
        sleep(0.5)
        keyboard.release(keystrokeDictionary['FindAccount_FPcode'][0])
        keyboard.release(keystrokeDictionary['FindAccount_FPcode'][1])
        cb.copy(customerCode)
        keyboard.press_and_release('menu')
        for i in range(0,4):
            keyboard.press_and_release('down')
            sleep(0.3)
        for i in range(0,5):
            keyboard.press_and_release('enter')
            sleep(0.5)

def enableOneTimeMessage():
    print(Fore.YELLOW + '[PROCESSING]\t Enabling One-Time-Message for account'+ Fore.RESET)
    keyboard.press(keystrokeDictionary['OneTimeMsg_Enable'][0])
    keyboard.press(keystrokeDictionary['OneTimeMsg_Enable'][1])
    sleep(0.5)
    keyboard.press(keystrokeDictionary['OneTimeMsg_Enable'][0])
    keyboard.press(keystrokeDictionary['OneTimeMsg_Enable'][1])
    sleep(0.5)
    keyboard.press(keystrokeDictionary['Tender_Cash'][0])
    keyboard.press(keystrokeDictionary['Tender_Cash'][1])
    print(Fore.GREEN + '[ENABLED]\t One-Time-Message for account' + Fore.RESET)
    sleep(0.5)
    openNewSale()

def printARMContract():
    print(Fore.YELLOW + '[DEMO][PROCESSING]\t Printing ARM Recharge Receipt for account' + Fore.RESET)
    keyboard.press(keystrokeDictionary['ARMContract'][0])
    keyboard.press(keystrokeDictionary['ARMContract'][1])
    print(Fore.YELLOW + '[DEMO][COMPLETE]\t ARM Recharge Receipt PRINTED for account' + Fore.RESET)
    openNewSale()




# Copyright (c) Chris Nance 2022
# Terminal Contoller, SiteWatch, TunnelWatch, and FastPass are trademarks of DRB Systems
# Do Not Redistribute

print(Fore.GREEN + 'TerminalControllerAPI Version 1.0 has loaded.' + Fore.RESET)