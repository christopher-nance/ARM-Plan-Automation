# Chris Nance
# Mass ARM Plan Modification Script
# Version 1.0

## Constants
PLAN_STATUS_TO_DROP = ['Discontinued', 'Terminated', 'Discontinuing', 'CC Pending', 'CC Declined', 'CC Expired', 'CC Unpaid', 'Rchrg Error'] # Avoid these ARM Accts.


## Import Modules
from logging import raiseExceptions
from multiprocessing.connection import wait
import pandas as pd
import mouse
import keyboard
import time
import os
import colorama

from pandas.core.dtypes.missing import notnull
from os.path import exists
from colorama import Fore
from colorama import init
init(convert=True)

print('\n'*2)
print(Fore.LIGHTMAGENTA_EX + '*********************************************')
print(Fore.LIGHTMAGENTA_EX + 'Mass ARM Plan Modification Script - Version 2')
print(Fore.LIGHTMAGENTA_EX + '        NASCAR Car Wash (Chris Nance)')
print(Fore.LIGHTMAGENTA_EX + '*********************************************' + Fore.RESET)
print('\n'*2)

print(Fore.LIGHTYELLOW_EX + "[INFO]: Before proceeding, please input the path to your Customer List CSV File.", Fore.RESET)
customerListCSV_path = input(Fore.WHITE + "Customer List Path: ")
#customerListCSV_path = int(input("Employee ID: "))
#customerListCSV_path = int(input("Employee Password: "))



############################################################################################################################################################################



## Validate that the file is CSV
while os.path.splitext(r'' + customerListCSV_path)[1].lower() != '.csv': # Check file extension with that neat little line.
    print(Fore.LIGHTRED_EX + '[ERROR]: The file you input was not a CSV file. Save the file as a Comma Seperated CSV file then input it into the program.\n         If you need help, please visit this link: https://support.microsoft.com/en-us/office/save-a-workbook-to-text-format-txt-or-csv-3e9a9d6c-70da-4255-aa28-fcacf1f081e6 \n         Please use the comma delimited CSV version.\n')
    customerListCSV_path = input(Fore.WHITE + "Customer List Path: ")


## Import CSV Customer Data File
print(Fore.WHITE + "[INFO]: Importing customer list...", Fore.RESET)
cust_df = pd.read_csv(customerListCSV_path, header=0)
time.sleep(1)

## CSV Content Validation
print(Fore.WHITE + "[INFO]: Validating CSV data & dropping null (missing) values...", Fore.RESET)
removedValues = 0
peopleRemoved = [['NON-MODIFIED FASTPASS PLANS']]
peopleRemoved.append(['Customer Name (Last Name,FirstName)', 'Customer Code', 'Plan Status', 'Plan Name'])
for idx, row in cust_df.iterrows():
    # Generate a dictionary for the table.
    customerName = row['CustomerName']
    customerCode = row['CustomerCode']
    planName = row['PlanName']
    planStatus = row['StatusStr']
    customerCC = row['Credit Card']
    # Append and Drop 'bad' status customers.
    if planStatus in PLAN_STATUS_TO_DROP:
        print(Fore.WHITE + "---->>> Dropping", customerName, 'because they have plan status:', planStatus + Fore.RESET)
        removedValues += 1
        peopleRemoved.append([customerName, customerCode, planStatus, planName]) # Append bad customers to list for exporting.\
        cust_df = cust_df.drop(idx)

pd.DataFrame(peopleRemoved).to_csv(r'C:\NCWAutomation\Output\Discontinue\PlansThatWereNotDiscontinued.csv') # Export the 'bad' customer list to ..\Output\Discontined.
cust_df = cust_df.dropna() # Drop null values.

print(Fore.WHITE + "[INFO]: In total,", Fore.RED + str(removedValues) + Fore.WHITE + "people have been unmodified.")
print(Fore.LIGHTBLACK_EX + r"[INFO]: To view a complete list of untouched FastPasses, go to C:\NCWAutomation\Output\Discontinue\PlansThatWereNotDiscontinued.csv")
print()
print()

############################################################################################################################################################################


# Button Location (X,Y) Dictionary
buttonLocationsDictionary = {
    # Lookup: Customer Code (FastPass Number)
    'LookupFastPassX': 1312,
    'LookupFastPassY': 389,
    # Lookup: Customer Search Name (LastName,FirstName)
    'LookupSearchNameX': 1314,
    'LookupSearchNameY': 344,

    # Discontinue
    'DiscontinueX': 1415,
    'DiscontinueY': 853,
    # Terminate
    'TerminateX': 1412,
    'TerminateY': 801,
    # Switch
    'SwitchX': 1408,
    'SwitchY': 742,
    
    # Starter FastPass
    'StarterFastPassX': 1415,
    'StarterFastPassY': 396,
    # Pro FastPass
    'ProFastPassX': 1418,
    'ProFastPassY': 444,
    # Legend FastPass
    'LegendFastPassX': 1416,
    'LegendFastPassY': 493,

    # Cash ($0) Tender
    'CashTenderX': 1416,
    'CashTenderY': 648,
    # ARM CC Tender
    'ARMCCTenderX': 1416,
    'ARMCCTenderY': 595,
    
    # Open New Sale
    'OpenNewSaleX': 885,
    'OpenNewSaleY': 897,

    # Std. Cust. Promo pkg. Added Prompt
    'PromoPkgX': 100,
    'PromoPkgY': 100,
}


############################################################################################################################################################################

## Modular Functions
# This should be useful for building main functions quicker and much easier debugging.

def lookup_customer(method, customerInformation): # Lookup Customers; return 0 (Good); return 1 (Error)
    if method == 'customerCode':
        print(Fore.WHITE + "Looking up via customer code...")
        mouse.move(buttonLocationsDictionary['LookupSearchNameX'], buttonLocationsDictionary['LookupSearchNameY'])
    elif method == 'searchName':
        print(Fore.WHITE + "Looking up via search name...")
        mouse.move(buttonLocationsDictionary['LookupFastPassX'], buttonLocationsDictionary['LookupFastPassY'])
    else: return 1

    mouse.click('left')
    time.sleep(0.1)
    keyboard.write(str(customerInformation), 0.1)
    keyboard.press_and_release('enter')
    time.sleep(1)
    keyboard.press_and_release('enter')

    return 0 # Exit clean
    
def discontinueCurrentCustomer(): # Assumes account open and prompts closed.
    mouse.move(buttonLocationsDictionary['DiscontinueX'], buttonLocationsDictionary['DiscontinueY'])
    mouse.click('left')
    time.sleep(0.1)
    mouse.move(buttonLocationsDictionary['CashTenderX'], buttonLocationsDictionary['CashTenderY'])
    mouse.click('left')
    time.sleep(0.2)
    keyboard.press_and_release('enter')
    return 0

def terminateCurrentCustomer():
    print(Fore.WHITE + "Terminating with refund.")
    mouse.move(buttonLocationsDictionary['TerminateX'], buttonLocationsDictionary['TerminateY'])
    mouse.click('left')
    mouse.move(buttonLocationsDictionary['ARMCCTenderX'], buttonLocationsDictionary['ARMCCTenderY'])
    time.sleep(0.1)
    # Move mouse to terminate without charging.
    
    mouse.click('left')
    return 0

def switchCurrentCustomer(planName):
    if planName == 'StarterFastPass' or planName == 'LegendFastPass' or planName == 'ProFastPass':
        mouse.move(buttonLocationsDictionary['SwitchX'], buttonLocationsDictionary['SwitchY'])
        mouse.click('left')
        mouse.move(buttonLocationsDictionary[planName + 'X'], buttonLocationsDictionary[planName + 'Y'])
        time.sleep(0.1)
        mouse.click('left')
        mouse.move(buttonLocationsDictionary['ARMCCTenderX'], buttonLocationsDictionary['ARMCCTenderY'])
        time.sleep(0.1)
        mouse.click('left')
        return 0
    else: return 1

def openNewSale():
    mouse.move(buttonLocationsDictionary['ProFastPassX'], buttonLocationsDictionary['ProFastPassY'])
    mouse.click('left')

def printCustomerSummary(customerName, customerCode, planName, planStatus, customerCC, monthlyCharge, originLocation):
    customer_summary = [
                [Fore.LIGHTCYAN_EX + "Customer Name", str(customerName)],
                [Fore.LIGHTGREEN_EX + "Customer Code", str(customerCode)],
                [Fore.WHITE + "Plan Name", Fore.WHITE + str(planName) + " @ $" + str(monthlyCharge) + "/month"],
                [Fore.WHITE + "Plan Status", Fore.WHITE + str(planStatus)],
                [Fore.WHITE + "Credit Card",  Fore.WHITE + str(customerCC)],
                [Fore.WHITE + "Origin Location", Fore.WHITE + str(originLocation)],
            ]
    print(Fore.LIGHTBLACK_EX + "="*56)
    for item in customer_summary: print("{: <20}{: >30}".format(*item))
    print(Fore.LIGHTBLACK_EX + "="*56)


############################################################################################################################################################################


def mainMenu():
    print("\n"*2)
    print(Fore.WHITE + "Main Menu")
    print(Fore.WHITE + "="*25)
    print(Fore.BLUE + "1.) Discontinue FastPasses...")
    print(Fore.YELLOW + "2.) Terminate FastPasses...")
    print(Fore.RED + "3.) Switch FastPasses...")
    print(Fore.MAGENTA + "4.) Compile Customer Information Summary")
    print()
    print(Fore.WHITE + "5.) Exit this CLI")
    print()
    print(Fore.WHITE + "Selecting options 1, 2, or 3 will result in further menu options.")
    print()
    menuOption = input(Fore.WHITE + "Please make your selection: ")
    menuOptions = [1,2,3,4,5]
    while menuOption in menuOptions == False:
        print(Fore.RED + 'You need to select a valid menu option.' + Fore.WHITE)
        menuOption = input(Fore.WHITE + "Please make your selection: ")

    if menuOption == 5:
        print(Fore.LIGHTBLUE_EX + "Goodbye!")
        time.sleep(2)
        exit()
    elif menuOption == 4:
        for idx, row in cust_df.iterrows():
            customerName = row['CustomerName']
            customerCode = row['CustomerCode']
            planName = row['PlanName']
            planStatus = row['StatusStr']
            customerCC = row['Credit Card']
            monthlyCharge = row['LastDollars']
            originLocation = row['PlanSoldAt']
            customer_summary = [
                [Fore.LIGHTCYAN_EX + "Customer Name", str(customerName)],
                [Fore.LIGHTGREEN_EX + "Customer Code", str(customerCode)],
                [Fore.WHITE + "Plan Name", Fore.WHITE + str(planName) + " @ $" + str(monthlyCharge) + "/month"],
                [Fore.WHITE + "Plan Status", Fore.WHITE + str(planStatus)],
                [Fore.WHITE + "Credit Card",  Fore.WHITE + str(customerCC)],
                [Fore.WHITE + "Origin Location", Fore.WHITE + str(originLocation)],
            ]
            print(Fore.LIGHTBLACK_EX + "="*56)
            for item in customer_summary: print("{: <20}{: >30}".format(*item))
            print(Fore.LIGHTBLACK_EX + "="*56)
            input(Fore.WHITE + 'Press ENTER to continue...')
        input(Fore.WHITE + "List complete. Press ENTER to go back to the Main Menu.")
        mainMenu()
    elif menuOption == 3:
        print('\n'*3)
        passToSwitchTo = input(Fore.WHITE + "Which FastPass are ee switching to? (S)tarter, (P)ro or (L)egend: ")
        while passToSwitchTo[1].lower() != 's' or passToSwitchTo[1].lower() != 'p' or passToSwitchTo[1].lower() != 'l':
            print(Fore.RED + "Oops, you need to type 's' for the starter fastpass, 'p' for the pro fastpass or 'l' for the legend fastpass.")
            passToSwitchTo = input(Fore.WHITE + "Which FastPass are ee switching to? (S)tarter, (P)ro or (L)egend: ")
        print(Fore.LIGHTGREEN_EX, "Looks like you're in good shape.\n", Fore.RESET)
        input(Fore.WHITE + "Press ENTER to start the script...\n")
        
        for idx, row in cust_df.iterrows():
            customerName = row['CustomerName']
            customerCode = row['CustomerCode']
            planName = row['PlanName']
            planStatus = row['StatusStr']
            customerCC = row['Credit Card']
            monthlyCharge = row['LastDollars']
            originLocation = row['PlanSoldAt']
            
            lookup_customer('customerCode', customerCode) # Lookup the customer
            print(Fore.LIGHTYELLOW_EX + "SWITCHING CUSTOMER: " + Fore.WHITE)
            printCustomerSummary(customerName, customerCode, planName, planStatus, customerCC, monthlyCharge, originLocation)
            if passToSwitchTo[1] == 's': switchCurrentCustomer('StarterFastPass') # Switch customer: Starter Pass
            if passToSwitchTo[1] == 'p': switchCurrentCustomer('ProFastPass') # Switch customer: Pro Pass
            if passToSwitchTo[1] == 'l': switchCurrentCustomer('LegendFastPass') # Switch customer: Legend Pass
            openNewSale() # Open a new sale
            time.sleep(0.1)
        
        print(Fore.WHITE + "Done switching customer's plans!\nA new CSV file needs to be created in order for the changes to be refelcted in this script.")
        time.sleep(6)
        mainMenu()
    elif menuOption == 2:
        print('\n'*3)
        for idx, row in cust_df.iterrows():
            customerName = row['CustomerName']
            customerCode = row['CustomerCode']
            planName = row['PlanName']
            planStatus = row['StatusStr']
            customerCC = row['Credit Card']
            monthlyCharge = row['LastDollars']
            originLocation = row['PlanSoldAt']

            lookup_customer('customerCode', customerCode) # Lookup the customer
            print(Fore.LIGHTRED_EX + "TERMINATING CUSTOMER: " + Fore.WHITE)
            printCustomerSummary(customerName, customerCode, planName, planStatus, customerCC, monthlyCharge, originLocation)    
            terminateCurrentCustomer() # Terminate the customer
            time.sleep(0.1)
            openNewSale() # Open a new sale

        time.sleep(6)
        mainMenu()
    
    elif menuOption == 1:
        print('\n'*3)
        for idx, row in cust_df.iterrows():
            customerName = row['CustomerName']
            customerCode = row['CustomerCode']
            planName = row['PlanName']
            planStatus = row['StatusStr']
            customerCC = row['Credit Card']
            monthlyCharge = row['LastDollars']
            originLocation = row['PlanSoldAt']
            
            lookup_customer('customerCode', customerCode) # Lookup the customer
            print(Fore.LIGHTRED_EX + "DISCONTINUING CUSTOMER: " + Fore.WHITE)
            printCustomerSummary(customerName, customerCode, planName, planStatus, customerCC, monthlyCharge, originLocation)    
            discontinueCurrentCustomer() # Discontinue the Customer
            time.sleep(0.1)
            openNewSale() # Open a new Sale

        time.sleep(6)
        mainMenu()
    else:
        print(Fore.RED + "That was not a valid menu option. Please choose a different option.")
        time.sleep(3)
        mainMenu()



mainMenu()        
exit()

## NOTES


'''
>> Need to add x,y for std promo pkg prompt
    >> OR probably use enter on keyboard to eliminate prompt.

>> Maybe use short cuts on the python tab for keyboard to better code in the future.




'''




