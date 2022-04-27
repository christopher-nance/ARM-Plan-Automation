info = '''
#==============================================================================#
title               :ARM_Manager.py
description         :Allows lite-weight management of ARM accounts.
author              :Chris Nance
date                :2022-09-04
version             :1.0
usage               :python ARM_Manager.py
notes               :See requirments.txt for list of dependencies.
python_version      :3.10
#==============================================================================#
'''

## MODULES
from time import sleep
import TerminalControllerAPI as tc
import PySimpleGUI as sg
from colorama import Fore, init
init(convert=True)
for num in range(1,100): print('\n')
print(Fore.MAGENTA + "Output Window Loaded. Hello! :)" + Fore.RESET)


numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
notProcessed = []
numberOfCustomersInFile = 0
processing = False

def createWindow():

    elements = [
        [sg.Text('Please select the Customer CSV File you wish to use', key='info')],

        [sg.Input(), sg.FileBrowse(file_types=(("CSV Files", "*.csv"),), key="CSV_IN"), sg.Button("Submit")],
    ]

    return sg.Window('Test App', elements)

def createSecondWindow():
    listElements = ['Discontinue', 'Terminate', 'Enable 1-Time Message', 'Disable 1-Time Message']
    elements = [
        [sg.Text('What would you like to do?', key='info'), sg.DropDown(listElements, size=(20,50), key='menuofstuff')],

        [sg.ProgressBar(numberOfCustomersInFile, key='progress')],
        [sg.Text('FastPass Accounts Queued for Modification: '+str(numberOfCustomersInFile), key='status', justification='c')],

        [sg.Submit()],
    ]

    return sg.Window('Test App', elements)

window = createWindow()

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event=="Exit":
        exit()
    elif event == "Submit":
        print(values["CSV_IN"])
        dataframeValid, dataframe = tc.validate_input(values['CSV_IN'])
        if dataframeValid == True:
            if dataframe.empty == False:
                print()
                window['info'].update('FILE HAS BEEN VALIDATED')
                numberOfCustomersInFile = len(dataframe.index)
                break
            else:
                print('Dataframe was returned empty...')
        else: 
            print("No dataframe was returned... So bad file or no file.")

window.close()
window = createSecondWindow()

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event=="Exit":
        print("The following customer codes were not processed...\n", notProcessed)
        exit()
    elif event == "Submit" and processing != True and values['menuofstuff'] == 'Enable 1-Time Message':
        processing = True
        print(Fore.LIGHTYELLOW_EX + 'Starting script... Please click on the Python tab and keep the Terminal Controller in-focus.')
        sleep(5)
        for index, row in dataframe.iterrows():
            tc.openNewSale()

            window['status'].update('Modifying fastpass accounts...' + str(index) + '/' + str(numberOfCustomersInFile))
            window['progress'].update(index)

            customerCode = tc.convertFPN(row['CustomerCode'])

            if customerCode[0] in numbers:
                tc.lookupAccount(customerCode)
                tc.enableOneTimeMessage(customerCode)
            else:
                print(Fore.RED + "[SKIPPING]\t account with code:", str(customerCode) + Fore.RESET)
                notProcessed.append(customerCode)

            sleep(1)
        print(Fore.LIGHTYELLOW_EX + 'Script has completed. Press any key to close this window.' + Fore.RESET)
        input()
        exit()
    elif event == "Submit" and processing != True and values['menuofstuff'] == 'Discontinue':
        print(Fore.RED + "Not Supported." + Fore.RESET)
    else:
        print(Fore.RED + "Not Supported." + Fore.RESET)

