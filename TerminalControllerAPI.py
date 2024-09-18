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
from PIL import Image, UnidentifiedImageError
import pytesseract
import re
import os


keystrokeDictionary = {

    '''
    This dictionary houses all the 'Hot Keys' or 'Key Shortcuts' (in SiteManager) and links
    them to proper descriptions of the button. Please ensure that the screen called
    '2022 Python Screen' is properly setup and if any changes need to be made they shopuld
    be done in this script, NOT in SiteManager. 

    '''


    'FastPass_Express':     ['Alt', 'a'], # Lite FastPass
    'FastPass_Clean':       ['Alt', 'b'], # Starter FastPass
    'FastPass_Protect':     ['Alt', 'c'], # Pro FastPass
    'FastPass_UShine':      ['Alt', 'd'], # Legend FastPass

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

    'SwitchRechargeSite':   ['Alt', 't'],

    'PAGE_Python':          ['Ctrl', 'Alt', 'c'], # Moves to the Python tab
    'PAGE_History':         ['Ctrl', 'Alt', 'b'], # Moves to the History tab

}

locationDictionary = {
    "wash*u - Plainfie":    "WSHUIL-001 - wash*u - Plainfield",
    "wash*u - Villa Pa":    "WSHUIL-002 - wash*u - Villa Park",
    "wash*u - Burbank":     "WSHUIL-003 - wash*u - Burbank",
    "wash*u - Carol St":    "WSHUIL-004 - wash*u - Carol Stream",
    "wash*u - Des Plai":    "WSHUIL-011 - wash*u - Des Plaines",
    "wash*u - Berwyn":      "WSHUIL-007 - wash*u - Berwyn",
    "wash*u - Joliet":      "WSHUIL-008 - wash*u - Joliet",
    "wash*u - Napervil":    "WSHUIL-010 - wash*u - Naperville",
    "wash*u - Evergree":    "WSHUIL-009 - wash*u - Evergreen",
    "Query Server":         "WSHUIL-HQ2 - Query Server"
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

def extract_location_from_image(path_to_image):
    # Check if the file exists
    if not os.path.exists(path_to_image):
        print(f"Error: The file '{path_to_image}' does not exist.")
        return None

    try:
        # Load the image using PIL
        image = Image.open(path_to_image)

        # Extract text from the image using pytesseract
        extracted_text = pytesseract.image_to_string(image)

        # Extract location from the text using regex matching
        def extract_location(text, location_dict):
            for key in location_dict.keys():
                # Using regular expressions to match partial location names
                pattern = re.escape(key)
                match = re.search(pattern, text)
                if match:
                    return location_dict[key]
            return None

        # Find the location
        location = extract_location(extracted_text, locationDictionary)

        # Output the result
        if location:
            print(f"Location found: {location}")
            return location
        else:
            print("Location not found in the extracted text.")
            return None

    except UnidentifiedImageError:
        print(f"Error: The file '{path_to_image}' is not a valid image file or the format is unsupported.")
    except pytesseract.TesseractError as e:
        print(f"Error: Tesseract encountered an issue: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



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

def switchCustomerRechargeSite(newLocation):
    if locationDictionary.get(newLocation, False) == False:
        print(Fore.YELLOW + '[PROCESSING]\t Migrating customer to the specified location' + Fore.RESET)
    else:
        print(Fore.YELLOW + '[PROCESSING]\t Migrating customer to the specified location' + Fore.RESET)
        keyboard.press(keystrokeDictionary['PAGE_History'])
        ## CAPTURE PROPER IMAGE ##
        ## DO IMAGE OCR ##
        ## RETURN PROPER SITE CODE ##
        sleep(0.2)
        keyboard.press(keystrokeDictionary['SwitchRechargeSite'][0])
        keyboard.press(keystrokeDictionary['SwitchRechargeSite'][1])
        sleep(0.2)
        keyboard.press('tab')
        sleep(0.2)
        cb.copy(locationDictionary[newLocation])
        keyboard.press_and_release('menu')
        for i in range(0,4):
            keyboard.press_and_release('down')
            sleep(0.3)
        for i in range(0,5):
            keyboard.press_and_release('enter')
            sleep(0.5)
        sleep(0.3)
        keyboard.press_and_release("enter")
        print(Fore.YELLOW + '[COMPLETE]\t Migration complete! Customer is now apart of {newLocation}' + Fore.RESET)
        openNewSale()




# Copyright (c) Chris Nance 2022
# Terminal Contoller, SiteWatch, TunnelWatch, and FastPass are trademarks of DRB Systems
# Do Not Redistribute

print(Fore.GREEN + 'TerminalControllerAPI Version 1.0 has loaded.' + Fore.RESET)