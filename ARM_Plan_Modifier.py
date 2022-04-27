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

sg.PopupOK("Instructions", "Please have a CSV (Comma Seperated) File ready to go containing a header called CustomerCode and a list of FastPass Numbers under it. Each cell should contain only one singluar FastPass Code.\n\nDo not use a Microsoft Excel (.xslx) sheet.\n\nSave a DRB Customer Analysis report to a text file and then copy the entire text file to the first cell of the spreadsheet in Excel. The other cells will populate accordingly, and then save as a CSV (comma seperated) file.\n\nCall Chris (630) 995-6758 if there are any issues.")

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
notProcessed = []
numberOfCustomersInFile = 0
processing = False

time_per_customer = 6.7

def createWindow():
    sg.theme('Topanga')
    elements = [
        [sg.Text('Please select the Customer CSV File you wish to use', key='info')],

        [sg.Input(), sg.FileBrowse(file_types=(("CSV Files", "*.csv"),), key="CSV_IN"), sg.Button("Submit")],
    ]

    return sg.Window('Auto Arm Modifier', elements)

def createSecondWindow():
    sg.theme('Topanga')
    listElements = ['Discontinue', 'Terminate', 'Enable 1-Time Message', 'Disable 1-Time Message']
    elements = [
        [sg.Text('What would you like to do?', key='info'), sg.DropDown(listElements, size=(20,50), key='menuofstuff')],

        [sg.ProgressBar(numberOfCustomersInFile, key='progress')],
        [sg.Text('FastPass Accounts Queued for Modification: '+str(numberOfCustomersInFile)+' | ETA: '+ tc.ETA(numberOfCustomersInFile, 0, time_per_customer), key='status', justification='c')],

        [sg.Submit()],
    ]

    return sg.Window('Auto ARM Modifier', elements)

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
                sg.PopupOK('Validation Complete', 'The file as been loaded into memory. Press OK to continue.')
                numberOfCustomersInFile = len(dataframe.index)
                break
            else:
                sg.PopupError('Validation Error', 'Sorry, there seems to be a problem with the returned dataframe. Are you sure this is a valid, non-empty CSV file containing a CustomerCode header?')
        else: 
            sg.PopupError("Validation Error", 'There is a problem with the CSV file you are uploading. Please ensure you follow these instructions for obtaining the properly formatted CSV file: \n1.) Save a list of ARM customers as a text document\n2.) In the text document, press Ctrl+A and then Ctrl+C to copy everything\n3.) In a blank excel sheet, click in the top left most cell and press Ctrl+V\n4.) Save this file as a comma seperated CSV file via Save As. DO NOT USE AN EXCEL FILE. ')

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

            window['status'].update(('Modifying fastpass accounts...' + str(index) + '/' + str(numberOfCustomersInFile)) + ' | ETA: ' + tc.ETA(numberOfCustomersInFile, index, time_per_customer))
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
        sg.PopupOK('Complete', 'The script is complete. It is recommended that additional reports are run to verify no customers were skipped during this process.')
        processing = False
        exit()
    elif event == "Submit" and processing != True and values['menuofstuff'] == 'Discontinue':
        sg.PopupError("Error", "Sorry, but the operation you selected is not yet supported.")
    else:
        sg.PopupError("Error", "Sorry, but the operation you selected is not yet supported.")

