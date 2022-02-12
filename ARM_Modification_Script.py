# Chris Nance
# Mass ARM Plan Modification Script
# Version 2.0

## Constants
PLAN_STATUS_TO_DROP = ['Discontinued', 'Terminated', 'Discontinuing', 'CC Pending', 'CC Declined', 'CC Expired', 'CC Unpaid', 'Rchrg Error'] # Avoid these ARM Accts.


## Import Modules
from logging import raiseExceptions
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
customerListCSV_path = input("Customer List Path: ")
#customerListCSV_path = int(input("Employee ID: "))
#customerListCSV_path = int(input("Employee Password: "))



############################################################################################################################################################################



## Validate that the file is CSV
while os.path.splitext(r'' + customerListCSV_path)[1].lower() != '.csv': # Check file extension with that neat little line.
    print(Fore.LIGHTRED_EX + '[ERROR]: The file you input was not a CSV file. Save the file as a Comma Seperated CSV file then input it into the program.\n         If you need help, please visit this link: https://support.microsoft.com/en-us/office/save-a-workbook-to-text-format-txt-or-csv-3e9a9d6c-70da-4255-aa28-fcacf1f081e6 \n         Please use the comma delimited CSV version.\n')
    customerListCSV_path = input(Fore.WHITE + "Customer List Path: ")


## Import CSV Customer Data File
print(Fore.LIGHTYELLOW_EX + "[INFO]: Importing customer list...", Fore.RESET)
cust_df = pd.read_csv(customerListCSV_path, header=0)
time.sleep(1)

## CSV Content Validation
print(Fore.LIGHTYELLOW_EX + "[INFO]: Validating CSV data & dropping null (missing) values...", Fore.RESET)
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

print(Fore.LIGHTYELLOW_EX + "[INFO]: In total,", str(removedValues), "people have been unmodified.")
print(Fore.LIGHTYELLOW_EX + r"[INFO]: To view a complete list of untouched FastPasses, go to C:\NCWAutomation\Output\Discontinue\PlansThatWereNotDiscontinued.csv")
print()
print()

############################################################################################################################################################################


# Button Location (X,Y) Dictionary
buttonLocationsDictionary = {
    # Lookup: Customer Code (FastPass Number)
    'LookupFastPassX': 100,
    'LookupFastPassY': 100,
    # Lookup: Customer Search Name (LastName,FirstName)
    'LookupSearchNameX': 100,
    'LookupSearchNameY': 100,

    # Discontinue
    'DiscontinueX': 100,
    'DiscontinueY': 100,
    # Terminate
    'TerminateX': 100,
    'TerminateY': 100,
    # Switch
    'SwitchX': 100,
    'SwitchY': 100,
    
    # Starter FastPass
    'StarterFastPassX': 100,
    'StarterFastPassY': 100,
    # Pro FastPass
    'ProFastPassX': 100,
    'ProFastPassY': 100,
    # Legend FastPass
    'LegendFastPassX': 100,
    'LegendFastPassY': 100,

    # Cash ($0) Tender
    'CashTenderX': 100,
    'CashTenderY': 100,
    # ARM CC Tender
    'ARMCCTenderX': 100,
    'ARMCCTenderY': 100,
    
    # Open New Sale
    'OpenNewSaleX': 100,
    'OpenNewSaleY': 100,

    # Std. Cust. Promo pkg. Added Prompt
    'PromoPkgX': 100,
    'PromoPkgY': 100,
}


############################################################################################################################################################################

## Modular Functions
# This should be useful for building main functions quicker and much easier debugging.

def lookup_customer(method, customerInformation): # Lookup Customers; return 0 (Good); return 1 (Error)
    if method == 'customerCode':
        print("Looking up via customer code...")
        mouse.move(buttonLocationsDictionary['LookupSearchNameX'], buttonLocationsDictionary['LookupSearchNameY'])
    elif method == 'searchName':
        print("Looking up via search name...")
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

def terminateCurrentCustomer(giveRefund):
    if giveRefund == True:
        print("Terminating with refund.")
        mouse.move(buttonLocationsDictionary['TerminateX'], buttonLocationsDictionary['TerminateY'])
        mouse.click('left')
        mouse.move(buttonLocationsDictionary['ARMCCTenderX'], buttonLocationsDictionary['ARMCCTenderY'])
        time.sleep(0.1)
    else:
        print("Terminating without refund.")
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


############################################################################################################################################################################


def mainMenu():
    print("="*10)
    print("Main Menu")
    print("="*10)
    print("1.) Discontinue FastPasses...")
    print("2.) Terminate FastPasses...")
    print("3.) Switch FastPasses...")
    print("4.) Compile Customer Information Summary")
    print()
    print("5.) Exit this CLI")
    print()
    print("Selecting options 1, 2, or 3 will result in further menu options.")
    print()
    menuOption = int(input("Please make your selection: "))

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
            input('Press ENTER to continue...')
        input("List complete. Press ENTER to go back to the Main Menu.")
        mainMenu()
    elif menuOption == 3:
        print('\n'*3)
        passToSwitchTo = input("Which FastPass are ee switching to? (S)tarter, (P)ro or (L)egend: ")
        while passToSwitchTo[1].lower() != 's' or passToSwitchTo[1].lower() != 'p' or passToSwitchTo[1].lower() != 'l':
            print("Oops, you need to type 's' for the starter fastpass, 'p' for the pro fastpass or 'l' for the legend fastpass.")
            passToSwitchTo = input("Which FastPass are ee switching to? (S)tarter, (P)ro or (L)egend: ")
        print(Fore.LIGHTGREEN_EX, "Looks like you're in good shape.\n", Fore.RESET)
        input("Press ENTER to start to script...\n")
        
        for idx, row in cust_df.iterrows():
            customerName = row['CustomerName']
            customerCode = row['CustomerCode']
            planName = row['PlanName']
            planStatus = row['StatusStr']
            customerCC = row['Credit Card']
            monthlyCharge = row['LastDollars']
            originLocation = row['PlanSoldAt']
            
            print("Switching", customerName + "...")
            lookup_customer('customerCode', customerCode)
            if passToSwitchTo[1] == 's': switchCurrentCustomer('StarterFastPass')
            if passToSwitchTo[1] == 'p': switchCurrentCustomer('ProFastPass')
            if passToSwitchTo[1] == 'l': switchCurrentCustomer('LegendFastPass')
            openNewSale()
            time.sleep(0.1)
        
        print("Done switching customer's plans!\nA new CSV file needs to be created in order for the changes to be refelcted in this script.")
        mainMenu()
    elif menuOption == 2:
        print('\n'*3)
        giveRefundBool = input("Which FastPass are ee switching to? (S)tarter, (P)ro or (L)egend: ")
        while passToSwitchTo[1].lower() != 'y' or passToSwitchTo[1].lower() != 'n':
            print("Please type Y for yes or N for no for refuns to be given out on termination.\nWARNING: If firing this script on a massive amount of customers, this will cause a lot of money to be processed.")
            passToSwitchTo = input("Would you like to give out refunds? (Y)es or (N)o: ")
        lookup_customer('customerCode', customerCode)
        customer_summary = [
                    [Fore.LIGHTCYAN_EX + "Customer Name", str(customerName)],
                    [Fore.LIGHTGREEN_EX + "Customer Code", str(customerCode)],
                    [Fore.WHITE + "Plan Name", Fore.WHITE + str(planName) + " @ $" + str(monthlyCharge) + "/month"],
                    [Fore.WHITE + "Plan Status", Fore.WHITE + str(planStatus)],
                    [Fore.WHITE + "Credit Card",  Fore.WHITE + str(customerCC)],
                    [Fore.WHITE + "Origin Location", Fore.WHITE + str(originLocation)],
                ]
        print(Fore.LIGHTBLACK_EX + "="*56)
        print("TERMINATING CUSTOMER: ")
        for item in customer_summary: print("{: <20}{: >30}".format(*item))
        print(Fore.LIGHTBLACK_EX + "="*56)    
        if giveRefundBool == True:
            terminateCurrentCustomer(True)
        else:
            terminateCurrentCustomer(False)
        time.sleep(0.1)
        openNewSale()
    elif menuOption == 1:
        print('\n'*3)
    else:
        print("That was not a valid menu option. Please choose a different option.")
        time.sleep(3)
        mainMenu()



mainMenu()        
exit()

## NOTES


'''
>> Add option to iterate through a decide per person to switch or terminate etc.




'''



